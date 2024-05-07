from s1_cns_cli.s1graph.common.models.enums import CheckResult, CheckCategories
from s1_cns_cli.s1graph.terraform.checks.resource.base_resource_value_check import BaseResourceCheck
from typing import List


class PostgreSQLServerConnectionThrottlingEnabled(BaseResourceCheck):
    def __init__(self):
        name = "Ensure server parameter 'connection_throttling' is set to 'ON' for PostgreSQL Database Server"
        id = "CKV_AZURE_32"
        supported_resources = ['azurerm_postgresql_configuration']
        categories = [CheckCategories.NETWORKING]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        if conf['name'][0] == 'connection_throttling' and conf['value'][0] == 'off':
            return CheckResult.FAILED
        return CheckResult.PASSED

    def get_evaluated_keys(self) -> List[str]:
        return ['name', 'value']


check = PostgreSQLServerConnectionThrottlingEnabled()
