from s1_cns_cli.s1graph.common.models.enums import CheckCategories
from s1_cns_cli.s1graph.common.models.consts import ANY_VALUE
from s1_cns_cli.s1graph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck


class AKSNetworkPolicy(BaseResourceValueCheck):
    def __init__(self):
        name = "Ensure AKS cluster has Network Policy configured"
        id = "CKV_AZURE_7"
        supported_resources = ['azurerm_kubernetes_cluster']
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self):
        return 'network_profile/[0]/network_policy'

    def get_expected_value(self):
        return ANY_VALUE


check = AKSNetworkPolicy()
