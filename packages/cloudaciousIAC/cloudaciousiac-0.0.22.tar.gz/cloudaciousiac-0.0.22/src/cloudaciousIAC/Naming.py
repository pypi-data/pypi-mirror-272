class Naming:
    """
    Naming standards for the Webhook handler stack.

    As we add more stacks, this should adapt along with `StackInfo.py` to become the defacto standard.
    """

    def __init__(
        self,
        stack_info: dict,
    ):
        self.stack_info: dict = stack_info

        self.stack_name: str = self.stack_info["stack_name"].replace("_", "-")
        self.client: str = self.stack_info["client_config"]["client"]

        return

    def image_name(self, fn_purpose: str) -> str:
        """
        Given a properly formatted `stack_info` and the specified `fn_purpose` of the container, this method returns the image name that follows naming convention.
        """
        image_name: str = f"{self.stack_name}-{self.client}-{fn_purpose}"
        return image_name

    def lambda_function_name(self, fn_purpose: str) -> str:
        """
        Takes the Lambda function config for the indicated `fn_purpose` and returns the proper name for the Lambda function.
        """
        lambda_function_name: str = f"{self.stack_name}-{self.client}-{fn_purpose}"
        return lambda_function_name

    def resource_base_name(self) -> str:
        """
        Creates the base name of the resources for the stack.
        """
        resource_base_name: str = f"{self.stack_name}-{self.client}"
        return resource_base_name
