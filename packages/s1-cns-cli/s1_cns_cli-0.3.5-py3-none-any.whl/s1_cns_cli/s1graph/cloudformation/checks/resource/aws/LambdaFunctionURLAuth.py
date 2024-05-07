from s1_cns_cli.s1graph.cloudformation.checks.resource.base_resource_negative_value_check import BaseResourceNegativeValueCheck
from s1_cns_cli.s1graph.common.models.enums import CheckCategories


class LambdaFunctionURLAuth(BaseResourceNegativeValueCheck):

    def __init__(self):
        name = "Ensure that Lambda function URLs AuthType is not None"
        id = "CKV_AWS_258"
        supported_resources = ['AWS::Lambda::Url']
        categories = [CheckCategories.GENERAL_SECURITY]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self):
        return "Properties/AuthType"

    def get_forbidden_values(self):
        return ["NONE"]


check = LambdaFunctionURLAuth()
