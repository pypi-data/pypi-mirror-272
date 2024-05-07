from typing import Dict, List, Any

from s1_cns_cli.s1graph.common.models.enums import CheckResult, CheckCategories
from s1_cns_cli.s1graph.terraform.checks.resource.base_resource_check import BaseResourceCheck


class EMRClusterKerberosAttributes(BaseResourceCheck):
    def __init__(self) -> None:
        name = "Ensure that EMR clusters with Kerberos have Kerberos Realm set"
        id = "CKV_AWS_114"
        supported_resources = ["aws_emr_cluster"]
        categories = [CheckCategories.GENERAL_SECURITY]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf: Dict[str, List[Any]]) -> CheckResult:
        if "kerberos_attributes" not in conf:
            return CheckResult.UNKNOWN
        kerberos_attributes = conf["kerberos_attributes"][0]
        if kerberos_attributes and "realm" in kerberos_attributes:
            return CheckResult.PASSED
        return CheckResult.FAILED

    def get_evaluated_keys(self) -> List[str]:
        return ["kerberos_attributes/[0]/realm"]


check = EMRClusterKerberosAttributes()
