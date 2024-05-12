import base64


class AWS:
    def __init__(
        self,
        session,
    ):
        """
        AWS class init accepts `session`, a boto3 session.
        """
        self.session = session

    def ecr_token(
        self,
        aws_account_id: str,
    ) -> str:
        f"""
        {__name__} ecr_token() uses boto3 to get the ECR registry auth token, which it base64 decodes, splits after the colon (it comes in username:password format), and returns the password.
        """
        client = self.session.client("ecr")
        response = client.get_authorization_token(
            registryIds=[
                aws_account_id,
            ]
        )
        print(response)
        token = response["authorizationData"][0]["authorizationToken"]
        password = base64.b64decode(token).decode("utf-8").split(":")[1]
        return password

    def update_lambda_function(
        self,
        base_image_name: str,
    ) -> None:
        f"""
        {__name__} update_lambda_function() takes the base_image_name pulumi export, extracts the image name (following the colon) which should always be the same as the Lambda function name, and uses boto3 to update the function to the latest image in ECR with the same tag as before.
        """
        # separate image name, which should match fn name
        lambda_fn_name = base_image_name.split(":")[1]
        print(
            f"{__name__}: base_image_name: {base_image_name}; type: {type(base_image_name)}"
        )

        # update lambda function
        try:
            client = self.session.client("lambda")
            response = client.update_function_code(
                FunctionName=lambda_fn_name,
                ImageUri=base_image_name,
            )
            print(f"{__name__}: response: {response}")
            return
        except Exception as e:
            print(f"{__name__}: exception updating lambda image uri, e: {e}")
            return
