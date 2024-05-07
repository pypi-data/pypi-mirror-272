from typing import Optional, Any, Dict
from collections.abc import Sized
from s1_cns_cli.s1graph.common.checks_infra.solvers.attribute_solvers.base_attribute_solver import BaseAttributeSolver
from s1_cns_cli.s1graph.common.graph.checks_infra.enums import Operators
from s1_cns_cli.s1graph.common.util.type_forcers import force_int


class LengthGreaterThanAttributeSolver(BaseAttributeSolver):
    operator = Operators.LENGTH_GREATER_THAN  # noqa: CCE003  # a static attribute

    def _get_operation(self, vertex: Dict[str, Any], attribute: Optional[str]) -> bool:
        attr = vertex.get(attribute)  # type:ignore[arg-type]  # due to attribute can be None
        if attr is None:
            return False

        value_int = force_int(self.value)

        if value_int is None:
            return False
        if isinstance(attr, Sized):
            # this resolver assumes the attribute is a string or a list.
            # if a dict is received, default the length to 1.
            if isinstance(attr, dict):
                return 1 > value_int
            return len(attr) > value_int

        return False
