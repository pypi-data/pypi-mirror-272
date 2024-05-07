from typing import Any

from s1_cns_cli.s1graph.common.models.enums import CheckCategories
from s1_cns_cli.s1graph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck
from s1_cns_cli.s1graph.common.models.consts import ANY_VALUE


class OSSBucketAccessLogs(BaseResourceValueCheck):
    def __init__(self) -> None:
        name = "Ensure the OSS bucket has access logging enabled"
        id = "CKV_ALI_12"
        supported_resources = ("alicloud_oss_bucket",)
        categories = (CheckCategories.LOGGING,)
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self) -> str:
        return "logging"

    def get_expected_value(self) -> Any:
        return ANY_VALUE


check = OSSBucketAccessLogs()
