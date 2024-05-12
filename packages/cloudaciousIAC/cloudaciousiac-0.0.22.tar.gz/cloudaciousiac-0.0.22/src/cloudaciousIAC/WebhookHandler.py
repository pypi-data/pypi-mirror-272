import json
import os

import boto3
import pulumi
import pulumi_aws as aws
import pulumi_std as std

from .Authinator import Authening
from .LambdaFunction import LambdaFunction
from .Naming import Naming
from .StackInfo import StackInfo


class WebhookHandler:
    def __init__(
        self,
        stack_info=dict,
    ):
        self.stack_info = stack_info

        self.stack_name = stack_info["stack_name"]
        self.client = stack_info["client_config"]["client"]
        self.aws_region = stack_info["cloud_config"]["aws_region"]
        self.aws_account_id = stack_info["cloud_config"]["aws_account_id"]
        self.tags = stack_info["client_config"]["tags"]

        # AWS boto3
        aws_region_name = os.getenv("AWS_REGION")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_session_token = os.getenv("AWS_SESSION_TOKEN")
        # session
        self.session = boto3.Session(
            region_name=aws_region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
        )

        # init classes
        self.stack_info_class = StackInfo(self.stack_info)
        self.naming = Naming(self.stack_info)

        self.resource_base_name = self.naming.resource_base_name()
        self.pulumi_resource_name = self.resource_base_name.replace("-", "_")
        self.dynamodb_table_name = f"{self.resource_base_name}"

        self.lambda_functions = self.stack_info["lambda_functions"]

    def meep_morp(self):
        """
        Creates Pulumi infrastructure for Meep Morp's message handler infrastructure.
        """
        ######################################################################
        ## IAM
        ######################################################################
        ## api gateway logging role
        self.api_gateway_assume_role = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "apigateway.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }

        self.api_gateway_iam_role = aws.iam.Role(
            resource_name=f"{self.pulumi_resource_name}_api_gateway_iam_role",
            name=f"{self.resource_base_name}-api-gateway-role",
            assume_role_policy=json.dumps(self.api_gateway_assume_role),
            managed_policy_arns=[
                "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs",
            ],
            tags=self.tags,
        )

        ######################################################################
        ## lambda + container images
        ######################################################################
        ecr_auth_token = Authening.ecr_token(
            session=self.session, aws_account_id=self.aws_account_id
        )

        self.lambda_message_handler = None

        for fn_purpose, config in self.lambda_functions.items():
            pulumi.debug(f"{__name__}: fn_purpose, config: {fn_purpose}, {config}")

            image_config = self.stack_info_class.image_config(fn_purpose=fn_purpose)
            lambda_config: dict = self.stack_info_class.lambda_config(
                fn_purpose=fn_purpose,
                config=config,
            )

            lambda_config["lambda_env_vars"]["TABLE_NAME"] = self.dynamodb_table_name

            lambda_function_class = LambdaFunction(
                image_config=image_config,
                lambda_config=lambda_config,
            )
            lambda_function = lambda_function_class.lambda_function(
                auth_token=ecr_auth_token,
            )
            if fn_purpose == "webhook-handler":
                self.lambda_webhook_handler = lambda_function

        ######################################################################
        ## log groups
        ######################################################################
        self.api_gateway_log_group = aws.cloudwatch.LogGroup(
            resource_name=f"{self.pulumi_resource_name}_api_gateway_log_group",
            name=f"/aws/api-gateway/{self.stack_name}/{self.client}",
            retention_in_days=7,
            tags=self.tags,
        )
        ######################################################################
        ## api gateway
        ######################################################################
        self.api_gateway_rest_api = aws.apigateway.RestApi(
            resource_name=f"{self.pulumi_resource_name}_api_gw_rest_api",
            name=f"{self.resource_base_name}",
            endpoint_configuration=aws.apigateway.RestApiEndpointConfigurationArgs(
                types="REGIONAL",
            ),
            tags=self.tags,
        )

        self.api_gateway_method = aws.apigateway.Method(
            resource_name=f"{self.pulumi_resource_name}_api_gw_method",
            rest_api=self.api_gateway_rest_api.id,
            authorization="NONE",
            http_method="ANY",
            resource_id=self.api_gateway_rest_api.root_resource_id,
        )

        self.api_gateway_integration = aws.apigateway.Integration(
            resource_name=f"{self.pulumi_resource_name}_api_gw_integration",
            opts=pulumi.ResourceOptions(
                depends_on=[self.lambda_webhook_handler, self.api_gateway_method]
            ),
            rest_api=self.api_gateway_rest_api.id,
            resource_id=self.api_gateway_rest_api.root_resource_id,
            integration_http_method="POST",
            http_method=self.api_gateway_method.http_method,
            type="AWS_PROXY",
            uri=self.lambda_webhook_handler.arn.apply(
                lambda arn: f"arn:aws:apigateway:{self.aws_region}:lambda:path/2015-03-31/functions/{arn}/invocations"
            ),
        )

        self.api_gateway_deployment = aws.apigateway.Deployment(
            resource_name=f"{self.pulumi_resource_name}_api_gw_deployment",
            opts=pulumi.ResourceOptions(
                depends_on=[self.api_gateway_method, self.api_gateway_integration]
            ),
            rest_api=self.api_gateway_rest_api.id,
            triggers={
                "redeployment": std.sha1_output(
                    input=pulumi.Output.json_dumps(self.api_gateway_rest_api.body)
                ).apply(lambda invoke: invoke.result),
            },
        )

        self.api_gateway_stage = aws.apigateway.Stage(
            resource_name=f"{self.pulumi_resource_name}_api_gw_stage",
            deployment=self.api_gateway_deployment.id,
            rest_api=self.api_gateway_rest_api.id,
            stage_name="call",
            access_log_settings={
                "destination_arn": self.api_gateway_log_group.arn,
                "format": 'Format: $context.extendedRequestId $context.identity.sourceIp $context.identity.caller $context.identity.user [$context.requestTime] "$context.httpMethod $context.resourcePath $context.protocol" $context.status $context.responseLength $context.requestId',
            },
            tags=self.tags,
        )

        self.api_gateway_account = aws.apigateway.Account(
            resource_name=f"{self.pulumi_resource_name}_api_gateway_account",
            cloudwatch_role_arn=self.api_gateway_iam_role.arn,
        )

        self.lambda_api_gateway_permission = aws.lambda_.Permission(
            resource_name=f"{self.pulumi_resource_name}_api_gw_lambda_permission",
            opts=pulumi.ResourceOptions(
                depends_on=[self.lambda_webhook_handler, self.api_gateway_method]
            ),
            action="lambda:InvokeFunction",
            function=self.lambda_webhook_handler.id,
            principal="apigateway.amazonaws.com",
            source_arn=self.api_gateway_rest_api.execution_arn.apply(
                lambda execution_arn: f"{execution_arn}/call/ANY/"
            ),
        )

        self.api_gateway_rest_api.id.apply(
            lambda id: print(
                f"https://{id}.execute-api.{self.aws_region}.amazonaws.com/call"
            )
        )

        ######################################################################
        ## dynamodb
        ######################################################################
        self.dynamodb_table_message_handler = aws.dynamodb.Table(
            resource_name=f"{self.pulumi_resource_name}_dynamodb_table",
            name=f"{self.dynamodb_table_name}",
            billing_mode="PROVISIONED",
            read_capacity=1,
            write_capacity=1,
            hash_key="client_id",
            range_key="message_timestamp",
            attributes=[
                aws.dynamodb.TableAttributeArgs(
                    name="client_id",
                    type="S",
                ),
                aws.dynamodb.TableAttributeArgs(
                    name="message_timestamp",
                    type="N",
                ),
                aws.dynamodb.TableAttributeArgs(
                    name="message_id",
                    type="S",
                ),
            ],
            ttl=aws.dynamodb.TableTtlArgs(
                attribute_name="TimeToExist",
                enabled=False,
            ),
            global_secondary_indexes=[
                aws.dynamodb.TableGlobalSecondaryIndexArgs(
                    name="client_id",
                    hash_key="client_id",
                    range_key="message_timestamp",
                    write_capacity=1,
                    read_capacity=1,
                    projection_type="ALL",
                ),
                aws.dynamodb.TableGlobalSecondaryIndexArgs(
                    name="message_id",
                    hash_key="message_id",
                    write_capacity=1,
                    read_capacity=1,
                    projection_type="ALL",
                ),
            ],
            tags=self.tags,
        )

        self.dynamodb_table_message_handler_read_target = aws.appautoscaling.Target(
            resource_name="self.dynamodb_table_message_handler_read_target",
            opts=pulumi.ResourceOptions(
                depends_on=[
                    self.dynamodb_table_message_handler,
                ]
            ),
            max_capacity=10,
            min_capacity=1,
            resource_id=f"table/{self.dynamodb_table_name}",
            scalable_dimension="dynamodb:table:ReadCapacityUnits",
            service_namespace="dynamodb",
            tags=self.tags,
        )

        self.dynamodb_table_message_handler_write_target = aws.appautoscaling.Target(
            resource_name="self.dynamodb_table_message_handler_write_target",
            opts=pulumi.ResourceOptions(
                depends_on=[
                    self.dynamodb_table_message_handler_read_target,
                ]
            ),
            max_capacity=10,
            min_capacity=1,
            resource_id=f"table/{self.dynamodb_table_name}",
            scalable_dimension="dynamodb:table:WriteCapacityUnits",
            service_namespace="dynamodb",
            tags=self.tags,
        )

        self.dynamodb_index_message_handler_read_target_client_wha_id = aws.appautoscaling.Target(
            resource_name="self.dynamodb_index_message_handler_read_target_client_id",
            opts=pulumi.ResourceOptions(
                depends_on=[
                    self.dynamodb_table_message_handler_write_target,
                ]
            ),
            max_capacity=10,
            min_capacity=1,
            resource_id=f"table/{self.dynamodb_table_name}/index/client_id",
            scalable_dimension="dynamodb:index:ReadCapacityUnits",
            service_namespace="dynamodb",
            tags=self.tags,
        )

        self.dynamodb_index_message_handler_write_target_client_wha_id = aws.appautoscaling.Target(
            resource_name="self.dynamodb_index_message_handler_write_target_client_id",
            opts=pulumi.ResourceOptions(
                depends_on=[
                    self.dynamodb_index_message_handler_read_target_client_wha_id,
                ]
            ),
            max_capacity=10,
            min_capacity=1,
            resource_id=f"table/{self.dynamodb_table_name}/index/client_id",
            scalable_dimension="dynamodb:index:WriteCapacityUnits",
            service_namespace="dynamodb",
            tags=self.tags,
        )

        self.dynamodb_index_message_handler_read_target_message_id = aws.appautoscaling.Target(
            resource_name="self.dynamodb_index_message_handler_read_target_message_id",
            opts=pulumi.ResourceOptions(
                depends_on=[
                    self.dynamodb_index_message_handler_write_target_client_wha_id,
                ]
            ),
            max_capacity=10,
            min_capacity=1,
            resource_id=f"table/{self.dynamodb_table_name}/index/message_id",
            scalable_dimension="dynamodb:index:ReadCapacityUnits",
            service_namespace="dynamodb",
            tags=self.tags,
        )

        self.dynamodb_index_message_handler_write_target_message_id = (
            aws.appautoscaling.Target(
                resource_name="dynamodb_index_write_target_message_id",
                opts=pulumi.ResourceOptions(
                    depends_on=[
                        self.dynamodb_index_message_handler_read_target_message_id,
                    ]
                ),
                max_capacity=10,
                min_capacity=1,
                resource_id=f"table/{self.dynamodb_table_name}/index/message_id",
                scalable_dimension="dynamodb:index:WriteCapacityUnits",
                service_namespace="dynamodb",
                tags=self.tags,
            )
        )
