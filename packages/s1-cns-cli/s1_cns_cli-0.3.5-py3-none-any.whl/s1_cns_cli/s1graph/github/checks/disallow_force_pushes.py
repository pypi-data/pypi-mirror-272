from __future__ import annotations

from s1_cns_cli.s1graph.github.base_github_branch_security import BranchSecurity


class GithubBranchDisallowForcePushes(BranchSecurity):
    def __init__(self) -> None:
        name = "Ensure GitHub branch protection rules does not allow force pushes"
        id = "CKV_GITHUB_5"
        super().__init__(
            name=name,
            id=id
        )

    def get_evaluated_keys(self) -> list[str]:
        return ['allow_force_pushes/enabled']

    def get_expected_value(self) -> bool:
        return False


check = GithubBranchDisallowForcePushes()
