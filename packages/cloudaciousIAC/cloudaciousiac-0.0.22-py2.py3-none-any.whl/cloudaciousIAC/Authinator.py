import base64

import boto3


class Authening:
    def __init__(
        self,
    ):
        return

    def ecr_token(session, aws_account_id):
        f"""
        {__name__} ecr_token() uses boto3 to get the ECR registry auth token, which it base64 decodes, splits after the colon (it comes in username:password format), and returns the password.
        """
        client = session.client("ecr")
        response = client.get_authorization_token(
            registryIds=[
                aws_account_id,
            ]
        )
        print(response)
        token = response["authorizationData"][0]["authorizationToken"]
        password = base64.b64decode(token).decode("utf-8").split(":")[1]
        return password
