from __future__ import annotations

from abc import abstractmethod
from collections.abc import Iterable
from typing import Any, TYPE_CHECKING

from s1_cns_cli.s1graph.common.checks.base_check import BaseCheck
from s1_cns_cli.s1graph.common.models.enums import CheckCategories
from s1_cns_cli.s1graph.github_actions.checks.registry import registry

if TYPE_CHECKING:
    from s1_cns_cli.s1graph.common.models.enums import CheckResult


class BaseGithubActionsCheck(BaseCheck):
    def __init__(
        self, name: str, id: str, supported_entities: Iterable[str], block_type: str, path: str | None = None
    ) -> None:
        categories = (CheckCategories.SUPPLY_CHAIN,)

        super().__init__(
            name=name,
            id=id,
            categories=categories,
            supported_entities=supported_entities,
            block_type=block_type,
        )
        self.path = path
        registry.register(self)

    def scan_entity_conf(self, conf: dict[str, Any], entity_type: str) -> tuple[CheckResult, dict[str, Any]]:  # type:ignore[override]  # multi_signature decorator is problematic
        self.entity_type = entity_type

        return self.scan_conf(conf)

    @abstractmethod
    def scan_conf(self, conf: dict[str, Any]) -> tuple[CheckResult, dict[str, Any]]:
        pass
