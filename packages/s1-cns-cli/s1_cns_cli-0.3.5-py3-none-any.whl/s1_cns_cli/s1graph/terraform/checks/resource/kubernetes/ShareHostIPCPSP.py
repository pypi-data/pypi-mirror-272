from typing import Any, List

from s1_cns_cli.s1graph.common.models.enums import CheckCategories
from s1_cns_cli.s1graph.terraform.checks.resource.base_resource_negative_value_check import BaseResourceNegativeValueCheck


class ShareHostIPCPSP(BaseResourceNegativeValueCheck):

    def __init__(self):
        # CIS-1.3 1.7.3
        # CIS-1.5 5.2.3
        name = "Do not admit containers wishing to share the host IPC namespace"
        id = "CKV_K8S_3"
        supported_resources = ["kubernetes_pod_security_policy"]
        categories = [CheckCategories.GENERAL_SECURITY]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self):
        return "spec/[0]/host_ipc"

    def get_forbidden_values(self) -> List[Any]:
        return [True]


check = ShareHostIPCPSP()
