from __future__ import annotations

from typing import Any

from s1_cns_cli.s1graph.common.models.enums import CheckCategories, CheckResult
from s1_cns_cli.s1graph.terraform.checks.resource.base_resource_check import BaseResourceCheck


class AzureDefenderOnKubernetes(BaseResourceCheck):
    def __init__(self) -> None:
        name = "Ensure that Azure Defender is set to On for Kubernetes"
        id = "CKV_AZURE_85"
        supported_resources = ("azurerm_security_center_subscription_pricing",)
        categories = (CheckCategories.GENERAL_SECURITY,)
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf: dict[str, list[Any]]) -> CheckResult:
        return (
            CheckResult.PASSED
            if conf.get("resource_type", [None])[0] != "KubernetesService" or conf.get("tier", [None])[0] == "Standard"
            else CheckResult.FAILED
        )

    def get_evaluated_keys(self) -> list[str]:
        return ["resource_type", "tier"]


check = AzureDefenderOnKubernetes()
