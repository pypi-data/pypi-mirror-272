from typing import Optional, Any, Dict

from s1_cns_cli.s1graph.common.graph.checks_infra.enums import Operators
from .is_empty_attribute_solver import IsEmptyAttributeSolver


class IsNotEmptyAttributeSolver(IsEmptyAttributeSolver):
    operator = Operators.IS_NOT_EMPTY  # noqa: CCE003  # a static attribute

    def _get_operation(self, vertex: Dict[str, Any], attribute: Optional[str]) -> bool:
        return not super()._get_operation(vertex, attribute)
