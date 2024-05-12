import json

import pulumi
import pulumi_aws as aws
import pulumi_docker as docker

from .ContainerImages import Image
from .Naming import Naming
from .StackInfo import StackInfo


class LambdaFunction:
    def __init__(
        self,
        lambda_config: dict,
        image_config: dict,
    ):
        self.image_config: dict = image_config
        self.lambda_config: dict = lambda_config
        self.lambda_fn_name = lambda_config["lambda_fn_name"]
        self.fn_purpose: str = lambda_config["fn_purpose"]
        self.lambda_env_vars: dict = lambda_config["lambda_env_vars"]
        self.tags = lambda_config["tags"]
        self.tags["fn_purpose"] = lambda_config["fn_purpose"]
        self.iam_policy_document: dict = lambda_config["iam_policy_document"]

        self._lambda_assume_role = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }

        pulumi.debug(
            f"{__name__}: image_config, lambda_config: {self.image_config}, {self.lambda_config}"
        )

        self._resource_name: str = self.lambda_fn_name.replace("-", "_")

    def lambda_function(
        self,
        auth_token: str,
    ):
        """
        Creates a containerized Lambda function, and builds the image for it, calling on the ContainerImages class.
        """
        image = Image(
            image_config=self.image_config,
            auth_token=auth_token,
        )
        image.create_image()
        self._container_build_image = image._container_build_image.image_name

        self.lambda_iam_role = aws.iam.Role(
            resource_name=f"{self._resource_name}_lambda_iam_role",
            name=f"{self.lambda_fn_name}-lambda",
            assume_role_policy=json.dumps(self._lambda_assume_role),
            tags=self.tags,
        )

        self.lambda_iam_policy = aws.iam.Policy(
            resource_name=f"{self._resource_name}_lambda_iam_policy",
            name=f"{self.lambda_fn_name}-lambda",
            description="policy",
            policy=json.dumps(self.iam_policy_document),
            tags=self.tags,
        )

        self.lambda_iam_attach = aws.iam.RolePolicyAttachment(
            resource_name=f"{self._resource_name}_lambda_iam_attach",
            role=self.lambda_iam_role.name,
            policy_arn=self.lambda_iam_policy.arn,
        )

        self.throwaway_env_vars: dict = {
            "IaC": "Pulumi",
        }

        lambda_function = aws.lambda_.Function(
            resource_name=f"{self._resource_name}_lambda_function",
            name=f"{self.lambda_fn_name}",
            timeout=45,
            package_type="Image",
            image_uri=self._container_build_image,
            role=self.lambda_iam_role.arn.apply(lambda arn: arn),
            environment=aws.lambda_.FunctionEnvironmentArgs(
                variables={**self.lambda_env_vars, **self.throwaway_env_vars},
            ),
            tags=self.tags,
        )
        return lambda_function
