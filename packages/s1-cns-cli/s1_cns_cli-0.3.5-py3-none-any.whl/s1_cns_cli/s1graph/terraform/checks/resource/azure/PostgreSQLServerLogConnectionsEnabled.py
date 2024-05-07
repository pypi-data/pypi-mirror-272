from s1_cns_cli.s1graph.common.models.enums import CheckResult, CheckCategories
from s1_cns_cli.s1graph.terraform.checks.resource.base_resource_value_check import BaseResourceCheck
from typing import List


class PostgreSQLServerLogConnectionsEnabled(BaseResourceCheck):
    def __init__(self):
        name = "Ensure server parameter 'log_connections' is set to 'ON' for PostgreSQL Database Server"
        id = "CKV_AZURE_31"
        supported_resources = ['azurerm_postgresql_configuration']
        categories = [CheckCategories.LOGGING]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        if conf['name'][0] == 'log_connections' and conf['value'][0] == 'off':
            return CheckResult.FAILED
        return CheckResult.PASSED

    def get_evaluated_keys(self) -> List[str]:
        return ['name', 'value']


check = PostgreSQLServerLogConnectionsEnabled()
