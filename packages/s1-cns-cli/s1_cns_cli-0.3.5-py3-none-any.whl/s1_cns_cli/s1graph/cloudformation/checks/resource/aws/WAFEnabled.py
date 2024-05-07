from s1_cns_cli.s1graph.common.models.enums import CheckCategories
from s1_cns_cli.s1graph.cloudformation.checks.resource.base_resource_value_check import BaseResourceValueCheck
from s1_cns_cli.s1graph.common.models.consts import ANY_VALUE


class WAFEnabled(BaseResourceValueCheck):
    def __init__(self):
        name = "CloudFront Distribution should have WAF enabled"
        id = "CKV_AWS_68"
        supported_resources = ['AWS::CloudFront::Distribution']
        categories = [CheckCategories.ENCRYPTION]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self):
        return 'Properties/DistributionConfig/WebACLId'

    def get_expected_value(self):
        return ANY_VALUE


check = WAFEnabled()
