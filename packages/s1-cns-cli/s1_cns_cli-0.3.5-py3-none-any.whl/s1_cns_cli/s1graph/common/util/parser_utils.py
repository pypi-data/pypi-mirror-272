from __future__ import annotations

import json
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Tuple
from s1_cns_cli.s1graph.common.typing import TFDefinitionKeyType
import hcl2


_FUNCTION_NAME_CHARS = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

_ARG_VAR_PATTERN = re.compile(r"[a-zA-Z_]+(\.[a-zA-Z_]+)+")

TERRAFORM_NESTED_MODULE_PATH_PREFIX = '([{'
TERRAFORM_NESTED_MODULE_PATH_ENDING = '}])'
TERRAFORM_NESTED_MODULE_INDEX_SEPARATOR = '#*#'
TERRAFORM_NESTED_MODULE_PATH_SEPARATOR_LENGTH = 3


@dataclass
class VarBlockMatch:
    full_str: str  # Example: ${local.foo}
    var_only: str  # Example: local.fop

    def replace(self, original: str, replaced: str) -> None:
        self.full_str = self.full_str.replace(original, replaced)
        self.var_only = self.var_only.replace(original, replaced)

    def is_simple_var(self) -> bool:
        """
        Indicates whether or not the value of the var block matches a "simple" var pattern. For example:
        local.blah, var.foo, module.one.a_resource.
        """
        return _ARG_VAR_PATTERN.match(self.var_only) is not None


class ParserMode(Enum):
    # Note: values are just for debugging.
    EVAL = "${"
    MAP = "{"
    STRING_SINGLE_QUOTE = "'"
    STRING_DOUBLE_QUOTE = '"'
    PARAMS = "("
    ARRAY = "["
    BLANK = " "

    @staticmethod
    def is_string(mode: "ParserMode") -> bool:
        return mode == ParserMode.STRING_SINGLE_QUOTE or mode == ParserMode.STRING_DOUBLE_QUOTE

    def __repr__(self) -> str:
        return str(self.value)

    def __str__(self) -> str:
        return str(self.value)


def is_acceptable_module_param(value: Any) -> bool:
    """
    This function determines if a value should be passed to a module as a parameter. We don't want to pass
    unresolved var, local or module references because they can't be resolved from the module, so they need
    to be resolved prior to being passed down.
    """
    value_type = type(value)
    if value_type is dict:
        for k, v in value.items():
            if not is_acceptable_module_param(v) or not is_acceptable_module_param(k):
                return False
        return True
    if value_type is set or value_type is list:
        for v in value:
            if not is_acceptable_module_param(v):
                return False
        return True

    if value_type is not str:
        return True

    for vbm in find_var_blocks(value):
        if vbm.is_simple_var():
            return False
    return True


def find_var_blocks(value: str) -> List[VarBlockMatch]:
    """
    Find and return all the var blocks within a given string. Order is important and may contain portions of
    one another.
    """

    to_return: List[VarBlockMatch] = []

    mode_stack: List[ParserMode] = []
    eval_start_pos_stack: List[int] = []  # location of first char inside brackets
    param_start_pos_stack: List[int] = []  # location of open parens
    preceding_dollar = False
    preceding_string_escape = False
    # NOTE: function calls can be nested, but since param args are only being inspected for variables,
    #       it's alright to ignore outer calls.
    param_arg_start = -1
    for index, c in enumerate(value):
        current_mode = ParserMode.BLANK if not mode_stack else mode_stack[-1]

        # Print statement of power...
        # print(f"{str(index).ljust(3, ' ')} {c} {'$' if preceding_dollar else ' '} "
        #       f"{'`' if preceding_string_escape else ' '} "
        #       f"{current_mode.ljust(2)} - {mode_stack}")

        if c == "$":
            if preceding_dollar:  # ignore double $
                preceding_dollar = False
                continue

            preceding_dollar = True
            continue

        if c == "{" and preceding_dollar:
            mode_stack.append(ParserMode.EVAL)
            eval_start_pos_stack.append(index + 1)  # next char
            preceding_dollar = False
            continue
        elif c == "\\" and ParserMode.is_string(current_mode):
            preceding_string_escape = True
            continue

        preceding_dollar = False

        if c == "}":
            if current_mode == ParserMode.EVAL:
                mode_stack.pop()
                start_pos = eval_start_pos_stack.pop()
                eval_string = value[start_pos:index]
                to_return.append(VarBlockMatch("${" + eval_string + "}", eval_string))
            elif current_mode == ParserMode.MAP:
                mode_stack.pop()
        elif c == "]" and current_mode == ParserMode.ARRAY:
            mode_stack.pop()
        elif c == ")" and current_mode == ParserMode.PARAMS:
            if param_arg_start > 0:
                param_arg = value[param_arg_start:index].strip()
                if _ARG_VAR_PATTERN.match(param_arg):
                    to_return.append(VarBlockMatch(param_arg, param_arg))
                param_arg_start = -1

            mode_stack.pop()
            start_pos = param_start_pos_stack.pop()
            # See if these params are for a function call. Back up from the index to determine if there's
            # a function preceding.
            function_name_start_index = start_pos
            for function_index in range(start_pos - 1, 0, -1):
                if value[function_index] in _FUNCTION_NAME_CHARS:
                    function_name_start_index = function_index
                else:
                    break
            # We know now there's a function call here. But, don't call it out if it's directly wrapped
            # in eval markers.
            in_eval_markers = False
            if function_name_start_index >= 2:
                in_eval_markers = (
                    value[function_name_start_index - 2] == "$" and value[function_name_start_index - 1] == "{"
                )
            if function_name_start_index < start_pos and not in_eval_markers:
                to_return.append(
                    VarBlockMatch(
                        value[function_name_start_index : index + 1], value[function_name_start_index : index + 1]
                    )
                )
        elif c == '"':
            if preceding_string_escape:
                preceding_string_escape = False
                continue
            elif current_mode == ParserMode.STRING_DOUBLE_QUOTE:
                mode_stack.pop()
            else:
                mode_stack.append(ParserMode.STRING_DOUBLE_QUOTE)
        elif c == "'":
            if preceding_string_escape:
                preceding_string_escape = False
                continue
            elif current_mode == ParserMode.STRING_SINGLE_QUOTE:
                mode_stack.pop()
            else:
                mode_stack.append(ParserMode.STRING_SINGLE_QUOTE)
        elif c == "{":
            # NOTE: Can't be preceded by a dollar sign (that was checked earlier)
            if not ParserMode.is_string(current_mode):
                mode_stack.append(ParserMode.MAP)
        elif c == "[":  # do we care?
            if not ParserMode.is_string(current_mode):
                mode_stack.append(ParserMode.ARRAY)
        elif c == "(":  # do we care?
            if not ParserMode.is_string(current_mode):
                mode_stack.append(ParserMode.PARAMS)
                param_start_pos_stack.append(index)
                param_arg_start = index + 1
        elif c == ",":
            if current_mode == ParserMode.PARAMS and param_arg_start > 0:
                param_arg = value[param_arg_start:index].strip()
                if _ARG_VAR_PATTERN.match(param_arg):
                    to_return.append(VarBlockMatch(param_arg, param_arg))
                param_arg_start = index + 1
        elif c == "?" and current_mode == ParserMode.EVAL:  # ternary
            # If what's been processed in the ternary so far is "true" or "false" (boolean or string type)
            # then nothing special will happen here and only the full expression will be returned.
            # Anything else will be treated as an unresolved variable block.
            start_pos = eval_start_pos_stack[-1]  # DO NOT pop: there's no separate eval start indicator
            eval_string = value[start_pos:index].strip()

            # HACK ALERT: For the cases with the trailing quotes, see:
            #             test_hcl2_load_assumptions.py -> test_weird_ternary_string_clipping
            if eval_string not in {"true", "false", '"true"', '"false"', 'true"', 'false"'}:
                # REMINDER: The eval string is not wrapped in a eval markers since they didn't really
                #           appear in the original value. If they're put in, substitution doesn't
                #           work properly.
                to_return.append(VarBlockMatch(eval_string, eval_string))

        preceding_string_escape = False

    return to_return


def split_merge_args(value: str) -> list[str] | None:
    """
    Split arguments of a merge function. For example, "merge(local.one, local.two)" would
    call this function with a value of "local.one, local.two" which would return
    ["local.one", "local.two"]. If the value cannot be unpacked, None will be returned.
    """
    if not value:
        return None

    # There are a number of splitting scenarios depending on whether variables or
    # direct maps are used:
    #           merge({tag1="foo"},{tag2="bar"})
    #           merge({tag1="foo"},local.some_tags)
    #           merge(local.some_tags,{tag2="bar"})
    #           merge(local.some_tags,local.some_other_tags)
    # Also, the number of arguments can vary, things can be nested, strings are evil...
    # See tests/terraform/test_parser_var_blocks.py for many examples.

    to_return = []
    current_arg_buffer = ""
    processing_str_escape = False
    inside_collection_stack: List[str] = []  # newest at position 0, contains the terminator for the collection
    for c in value:
        if c == "," and not inside_collection_stack:
            current_arg_buffer = current_arg_buffer.strip()
            # Note: can get a zero-length buffer when there's a double comman. This can
            #       happen with multi-line args (see parser_internals test)
            if len(current_arg_buffer) != 0:
                to_return.append(current_arg_buffer)
            current_arg_buffer = ""
        else:
            current_arg_buffer += c

        processing_str_escape = _str_parser_loop_collection_helper(c, inside_collection_stack, processing_str_escape)

    current_arg_buffer = current_arg_buffer.strip()
    if len(current_arg_buffer) > 0:
        to_return.append(current_arg_buffer)

    if len(to_return) == 0:
        return None
    return to_return


def _str_parser_loop_collection_helper(c: str, inside_collection_stack: List[str], processing_str_escape: bool) -> bool:
    """
    This function handles dealing with tracking when a char-by-char state loop is inside a
    "collection" (map, array index, method args, string).

    :param c:       Active character
    :param inside_collection_stack:     Stack of terminators for collections. This will be modified by
                                        this function. The active terminator will be at position 0.


    :return: value to set for `processing_str_escape`
    """
    inside_a_string = False
    if inside_collection_stack:
        terminator = inside_collection_stack[0]

        if terminator == '"' or terminator == "'":
            if processing_str_escape:
                processing_str_escape = False
                return processing_str_escape
            elif c == "\\":
                processing_str_escape = True
                return processing_str_escape
            else:
                inside_a_string = True

        if c == terminator:
            del inside_collection_stack[0]
            return processing_str_escape

    if not inside_a_string:
        if c == '"':
            inside_collection_stack.insert(0, '"')
        elif c == "'":
            inside_collection_stack.insert(0, "'")
        elif c == "{":
            inside_collection_stack.insert(0, "}")
        elif c == "[":
            inside_collection_stack.insert(0, "]")
        elif c == "(":
            inside_collection_stack.insert(0, ")")

    return processing_str_escape


def eval_string(value: str) -> Any:
    try:
        value_string = value.replace("'", '"')
        parsed = hcl2.loads(f"eval = {value_string}\n")  # NOTE: newline is needed
        return parsed["eval"][0]
    except Exception:
        return None


def string_to_native(value: str) -> Any:
    try:
        value_string = value.replace("'", '"')
        return json.loads(value_string)
    except Exception:
        return None


def to_string(value: Any) -> str:
    if value is True:
        return "true"
    elif value is False:
        return "false"
    return str(value)


def get_current_module_index(full_path: str) -> Optional[int]:
    hcl_index = None
    tf_index = None
    if TERRAFORM_NESTED_MODULE_PATH_PREFIX not in full_path and TERRAFORM_NESTED_MODULE_INDEX_SEPARATOR not in full_path:
        return len(full_path)
    if f'.hcl{TERRAFORM_NESTED_MODULE_PATH_PREFIX}' in full_path:
        hcl_index = full_path.index(f'.hcl{TERRAFORM_NESTED_MODULE_PATH_PREFIX}') + 4  # len('.hcl')
    elif f'.hcl{TERRAFORM_NESTED_MODULE_INDEX_SEPARATOR}' in full_path:
        hcl_index = full_path.index(f'.hcl{TERRAFORM_NESTED_MODULE_INDEX_SEPARATOR}') + 4  # len('.hcl')
    if f'.tf{TERRAFORM_NESTED_MODULE_PATH_PREFIX}' in full_path:
        tf_index = full_path.index(f'.tf{TERRAFORM_NESTED_MODULE_PATH_PREFIX}') + 3    # len('.tf')
    elif f'.tf{TERRAFORM_NESTED_MODULE_INDEX_SEPARATOR}' in full_path:
        tf_index = full_path.index(f'.tf{TERRAFORM_NESTED_MODULE_INDEX_SEPARATOR}') + 3  # len('.tf')
    if hcl_index and tf_index:
        # returning the index of the first file
        return min(hcl_index, tf_index)
    if hcl_index:
        return hcl_index
    return tf_index


def is_nested(full_path: TFDefinitionKeyType) -> bool:
    from s1_cns_cli.s1graph.terraform.modules.module_objects import TFDefinitionKey
    if isinstance(full_path, str):
        return TERRAFORM_NESTED_MODULE_PATH_PREFIX in full_path
    if isinstance(full_path, TFDefinitionKey):
        return full_path.tf_source_modules is not None
    return False


def get_tf_definition_key(nested_module: str, module_name: str, module_index: Any, nested_key: str = '') -> str:
    return f"{nested_module}{TERRAFORM_NESTED_MODULE_PATH_PREFIX}{module_name}{TERRAFORM_NESTED_MODULE_INDEX_SEPARATOR}{module_index}{nested_key}{TERRAFORM_NESTED_MODULE_PATH_ENDING}"


def get_tf_definition_key_from_module_dependency(path: str, module_dependency: str, module_dependency_num: str) -> str:
    if not module_dependency:
        return path
    if not is_nested(module_dependency):
        return f"{path}{TERRAFORM_NESTED_MODULE_PATH_PREFIX}{module_dependency}{TERRAFORM_NESTED_MODULE_INDEX_SEPARATOR}{module_dependency_num}{TERRAFORM_NESTED_MODULE_PATH_ENDING}"
    module_index = get_current_module_index(module_dependency)
    return f"{path}{TERRAFORM_NESTED_MODULE_PATH_PREFIX}{module_dependency[:module_index]}{TERRAFORM_NESTED_MODULE_INDEX_SEPARATOR}{module_dependency_num}{module_dependency[module_index:]}{TERRAFORM_NESTED_MODULE_PATH_ENDING}"


def get_module_from_full_path(file_path: TFDefinitionKeyType) -> Tuple[Optional[str], Optional[str]]:
    from s1_cns_cli.s1graph.terraform.modules.module_objects import TFDefinitionKey
    if not is_nested(file_path):
        return None, None
    if isinstance(file_path, TFDefinitionKey):
        return file_path.tf_source_modules.path, None
    tmp_path = file_path[file_path.index(TERRAFORM_NESTED_MODULE_PATH_PREFIX) + TERRAFORM_NESTED_MODULE_PATH_SEPARATOR_LENGTH: -TERRAFORM_NESTED_MODULE_PATH_SEPARATOR_LENGTH]
    if is_nested(tmp_path):
        module = get_abs_path(tmp_path) + tmp_path[tmp_path.index(TERRAFORM_NESTED_MODULE_PATH_PREFIX):]
        index = tmp_path[tmp_path.index(TERRAFORM_NESTED_MODULE_INDEX_SEPARATOR) + TERRAFORM_NESTED_MODULE_PATH_SEPARATOR_LENGTH:tmp_path.index(TERRAFORM_NESTED_MODULE_PATH_PREFIX)]
    else:
        module = get_abs_path(tmp_path)
        index = tmp_path[tmp_path.index(TERRAFORM_NESTED_MODULE_INDEX_SEPARATOR) + TERRAFORM_NESTED_MODULE_PATH_SEPARATOR_LENGTH:]
    return module, index


def get_abs_path(file_path: TFDefinitionKeyType) -> str:
    return file_path[:get_current_module_index(file_path)] if isinstance(file_path, str) else str(file_path.file_path)
