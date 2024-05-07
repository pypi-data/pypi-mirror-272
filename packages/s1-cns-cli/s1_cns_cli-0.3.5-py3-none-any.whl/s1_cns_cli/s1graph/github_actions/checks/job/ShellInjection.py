from __future__ import annotations

import re
from typing import Any

from s1_cns_cli.s1graph.common.models.enums import CheckResult
from s1_cns_cli.s1graph.github_actions.checks.base_github_action_check import BaseGithubActionsCheck
from s1_cns_cli.s1graph.github_actions.common.shell_injection_list import terms as bad_inputs
from s1_cns_cli.s1graph.yaml_doc.enums import BlockType


class DontAllowShellInjection(BaseGithubActionsCheck):
    def __init__(self) -> None:
        name = "Ensure run commands are not vulnerable to shell injection"
        id = "CKV_GHA_2"
        super().__init__(
            name=name,
            id=id,
            block_type=BlockType.ARRAY,
            supported_entities=('jobs', 'jobs.*.steps[]')
        )

    def scan_conf(self, conf: dict[str, Any]) -> tuple[CheckResult, dict[str, Any]]:
        if not isinstance(conf, dict):
            return CheckResult.UNKNOWN, conf

        if "run" not in conf:
            return CheckResult.PASSED, conf
        run = conf.get("run", "")
        for term in bad_inputs:
            if re.search(term, run):
                return CheckResult.FAILED, conf

        return CheckResult.PASSED, conf


check = DontAllowShellInjection()
