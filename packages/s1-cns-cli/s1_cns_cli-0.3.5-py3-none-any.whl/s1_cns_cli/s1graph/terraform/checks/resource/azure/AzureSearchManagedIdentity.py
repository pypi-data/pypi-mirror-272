from typing import Any

from s1_cns_cli.s1graph.common.models.enums import CheckCategories
from s1_cns_cli.s1graph.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck


class AzureSearchManagedIdentity(BaseResourceValueCheck):
    def __init__(self) -> None:
        # Connections to Azure resources is required to use some features including indexing and customer managed-keys.
        # Cognitive Search can use managed identities to authenticate to Azure resource without storing credentials.
        # Using Azure managed identities have the following benefits:
        # - You don't need to store or manage credentials. Azure automatically generates tokens and performs rotation.
        # - You can use managed identities to authenticate to any Azure service that supports Azure AD authentication.
        # Managed identities can be used without any additional cost.
        name = "Ensure Azure Cognitive Search service uses managed identities to access Azure resources"
        id = "CKV_AZURE_207"
        supported_resources = ("azurerm_search_service",)
        categories = (CheckCategories.IAM,)
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self) -> str:
        return "identity/[0]/type"

    def get_expected_values(self) -> Any:
        return "SystemAssigned"


check = AzureSearchManagedIdentity()
