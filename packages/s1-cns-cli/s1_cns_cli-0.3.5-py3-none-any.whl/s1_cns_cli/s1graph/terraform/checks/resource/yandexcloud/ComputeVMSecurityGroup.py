from typing import Any

from s1_cns_cli.s1graph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck
from s1_cns_cli.s1graph.common.models.enums import CheckCategories
from s1_cns_cli.s1graph.common.models.consts import ANY_VALUE


class ComputeVMSecurityGroup(BaseResourceValueCheck):
    def __init__(self) -> None:
        name = "Ensure security group is assigned to network interface."
        id = "CKV_YC_11"
        supported_resources = ("yandex_compute_instance",)
        categories = (CheckCategories.NETWORKING,)
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self) -> str:
        return "network_interface/[0]/security_group_ids"

    def get_expected_value(self) -> Any:
        return ANY_VALUE


check = ComputeVMSecurityGroup()
