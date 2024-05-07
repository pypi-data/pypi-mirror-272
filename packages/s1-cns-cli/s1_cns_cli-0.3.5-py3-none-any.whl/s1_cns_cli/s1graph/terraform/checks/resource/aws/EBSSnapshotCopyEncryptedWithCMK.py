from s1_cns_cli.s1graph.common.models.consts import ANY_VALUE
from s1_cns_cli.s1graph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck
from s1_cns_cli.s1graph.common.models.enums import CheckCategories


class EBSSnapshotCopyEncryptedWithCMK(BaseResourceValueCheck):
    def __init__(self):
        name = "Ensure EBS Snapshot Copy is encrypted by KMS using a customer managed Key (CMK)"
        id = "CKV_AWS_183"
        supported_resources = ['aws_ebs_snapshot_copy']
        categories = [CheckCategories.ENCRYPTION]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self):
        return "kms_key_id"

    def get_expected_value(self):
        return ANY_VALUE


check = EBSSnapshotCopyEncryptedWithCMK()
