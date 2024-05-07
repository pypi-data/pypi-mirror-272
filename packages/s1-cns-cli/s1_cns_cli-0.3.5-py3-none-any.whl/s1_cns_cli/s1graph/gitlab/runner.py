from __future__ import annotations

from typing import TYPE_CHECKING
from s1_cns_cli.s1graph.common.s1cns.check_type import CheckType
from s1_cns_cli.s1graph.gitlab.dal import Gitlab
from s1_cns_cli.s1graph.json_doc.runner import Runner as JsonRunner
from s1_cns_cli.s1graph.runner_filter import RunnerFilter

if TYPE_CHECKING:
    from s1_cns_cli.s1graph.common.checks.base_check_registry import BaseCheckRegistry
    from s1_cns_cli.s1graph.common.output.report import Report


class Runner(JsonRunner):
    check_type = CheckType.GITLAB_CONFIGURATION  # noqa: CCE003  # a static attribute

    def __init__(self) -> None:
        self.gitlab = Gitlab()
        super().__init__()

    def run(
        self,
        root_folder: str | None = None,
        external_checks_dir: list[str] | None = None,
        files: list[str] | None = None,
        runner_filter: RunnerFilter | None = None,
        collect_skip_comments: bool = True
    ) -> Report | list[Report]:
        runner_filter = runner_filter or RunnerFilter()
        if not runner_filter.show_progress_bar:
            self.pbar.turn_off_progress_bar()

        self.prepare_data()

        report = super().run(
            root_folder=self.gitlab.gitlab_conf_dir_path,
            external_checks_dir=external_checks_dir,
            files=None,  # ignore file scans
            runner_filter=runner_filter,
            collect_skip_comments=collect_skip_comments,
        )
        JsonRunner._change_files_path_to_relative(report)  # type:ignore[arg-type]  # report can only be of type Report, not a list
        return report

    def prepare_data(self) -> None:
        self.gitlab.persist_all_confs()

    def require_external_checks(self) -> bool:
        # default json runner require only external checks. Gitlab runner brings build in checks
        return False

    def import_registry(self) -> BaseCheckRegistry:
        from s1_cns_cli.s1graph.gitlab.registry import registry
        return registry
