from __future__ import annotations

from typing import TYPE_CHECKING

from s1_cns_cli.s1graph.common.models.enums import CheckCategories, CheckResult
from s1_cns_cli.s1graph.dockerfile.base_dockerfile_check import BaseDockerfileCheck

if TYPE_CHECKING:
    from dockerfile_parse.parser import _Instruction

install_commands = (
    "install",
    "source-install",
    "reinstall",
    "groupinstall",
    "localinstall",
    "add",
)
update_commands = (
    "update",
    "--update",
)


class UpdateNotAlone(BaseDockerfileCheck):
    def __init__(self) -> None:
        name = "Ensure update instructions are not use alone in the Dockerfile"
        id = "CKV_DOCKER_5"
        supported_instructions = ("RUN",)
        categories = (CheckCategories.APPLICATION_SECURITY,)
        super().__init__(name=name, id=id, categories=categories, supported_instructions=supported_instructions)

    def scan_resource_conf(self, conf: list[_Instruction]) -> tuple[CheckResult, list[_Instruction] | None]:
        update_instructions = []
        update_cnt = 0
        i = 0
        for instruction in conf:
            content = instruction["content"]
            if instruction["instruction"] in self.supported_instructions:

                if any(x in content for x in update_commands):
                    update_cnt = update_cnt + 1
                    update_instructions.append(i)
                if any(x in content for x in install_commands):
                    update_cnt = update_cnt - 1
            i = i + 1

        if update_cnt <= 0:
            return CheckResult.PASSED, None
        output = []
        for i in update_instructions:
            output.append(conf[i])

        return CheckResult.FAILED, output


check = UpdateNotAlone()
