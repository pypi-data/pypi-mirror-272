from s1_cns_cli.s1graph.common.models.enums import CheckCategories
from s1_cns_cli.s1graph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck


class GoogleStorageBucketUniformAccess(BaseResourceValueCheck):
    def __init__(self) -> None:
        name = "Ensure that Cloud Storage buckets have uniform bucket-level access enabled"
        id = "CKV_GCP_29"
        supported_resources = ["google_storage_bucket"]
        categories = [CheckCategories.GENERAL_SECURITY]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self) -> str:
        return "uniform_bucket_level_access"


check = GoogleStorageBucketUniformAccess()
