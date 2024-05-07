from s1_cns_cli.s1graph.common.models.enums import CheckCategories, CheckResult
from s1_cns_cli.s1graph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck


class IoTNoPublicNetworkAccess(BaseResourceValueCheck):
    def __init__(self):
        name = "Ensure that Azure IoT Hub disables public network access"
        id = "CKV_AZURE_108"
        supported_resources = ['azurerm_iothub']
        categories = [CheckCategories.NETWORKING]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources,
                         missing_block_result=CheckResult.PASSED)

    def get_inspected_key(self):
        return 'public_network_access_enabled'

    def get_expected_value(self):
        return False


check = IoTNoPublicNetworkAccess()
