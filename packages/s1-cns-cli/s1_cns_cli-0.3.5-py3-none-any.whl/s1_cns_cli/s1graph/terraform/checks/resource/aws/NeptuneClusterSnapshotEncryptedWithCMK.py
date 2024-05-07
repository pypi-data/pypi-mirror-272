from typing import Any

from s1_cns_cli.s1graph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck
from s1_cns_cli.s1graph.common.models.enums import CheckCategories
from s1_cns_cli.s1graph.common.models.consts import ANY_VALUE


class NeptuneClusterSnapshotEncrypted(BaseResourceValueCheck):
    def __init__(self) -> None:
        name = "Ensure Neptune snapshot is encrypted by KMS using a customer managed Key (CMK)"
        id = "CKV_AWS_280"
        supported_resources = ("aws_neptune_cluster_snapshot",)
        categories = (CheckCategories.ENCRYPTION,)
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self) -> str:
        return "kms_key_id"

    def get_expected_value(self) -> Any:
        return ANY_VALUE


check = NeptuneClusterSnapshotEncrypted()
