from typing import List, Callable, Any
from .model import (
    Context,
    Action,
    Observation,
    FunctionSignature,
    ToolExposition,
    NO_DEFAULT,
)


def extract_function_signature(cls) -> FunctionSignature:
    # actually the signature of the __call__ method
    # args = [(name, type, default), ...], e.g. [('path', str, ''), ('with_line_numbers', bool, False)]

    method = cls.__call__

    args = list(method.__annotations__.items())
    defaults = method.__defaults__ or []
    defaults = (len(args) - len(defaults)) * [NO_DEFAULT] + list(defaults)

    def safedefault(index):
        try:
            return defaults[index]
        except:
            return ""

    names_types_defaults = [
        (name, type.__name__, safedefault(index))
        for index, (name, type) in enumerate(args)
    ]

    def safetype(type):
        try:
            return type.__name__
        except:
            return str(type)

    return FunctionSignature(name=cls.__name__, args=names_types_defaults)


def extract_tool_exposition(cls) -> ToolExposition:
    return ToolExposition(
        name=cls.__name__,
        description=cls.__doc__,
        signature=extract_function_signature(cls),
    )


def render_tool_exposition(tool_exposition: ToolExposition) -> str:
    signature = tool_exposition.signature

    # signature
    # """description"""
    # examples
    opt_default_s = lambda default: f"={default}" if default is not NO_DEFAULT else ""
    parameter_s = ", ".join(
        [
            f"{name}: {type}{opt_default_s(default)}"
            for name, type, default in signature.args
        ]
    )
    # return f'{tool_exposition.name}({parameter_s.strip()})\n' + f'"""{tool_exposition.description}"""' + '\nexamples:\n'
    return (
        f"{tool_exposition.name}({parameter_s.strip()})\n"
        + f'"""{tool_exposition.description}"""\n'
    )


def render_tools_prompt(tool_classes: List[type]) -> str:
    tool_expositions = [
        extract_tool_exposition(tool_class) for tool_class in tool_classes
    ]
    return "\n".join(
        [
            render_tool_exposition(tool_exposition)
            for tool_exposition in tool_expositions
        ]
    )


class ToolNotFoundError(Exception):
    pass


def get_tool(
    tool_classes: List[type], tool_cls_name: str, context: Context
) -> Callable:
    for tool_cls in tool_classes:
        if tool_cls.__name__ == tool_cls_name:
            return tool_cls(context)
    raise ToolNotFoundError(f"Tool {tool_cls_name} not found.")


def marshall_args(action: Action) -> Any:
    # replace any arg which has type string and value HEREDOC with the heredoc string
    def transform_arg(arg):
        if arg == "HEREDOC":
            return action.function_call.heredoc
        else:
            try:
                return eval(arg)
            except:
                return arg

    args = [transform_arg(arg) for arg in action.function_call.args]
    kwargs = {k: transform_arg(v) for k, v in action.function_call.kwargs.items()}
    # pprint([(arg, type(arg)) for arg in args])
    # pprint([(k, arg, type(arg)) for k, arg in kwargs.items()])
    return args, kwargs


def execute_action(action: Action, context: Context, tools: List[type]) -> Observation:
    try:
        tool = get_tool(tools, action.function_call.function_name, context)
    except ToolNotFoundError as e:
        return Observation(f"Error: {e}")
    args, kwargs = marshall_args(action)
    return tool(*args, **kwargs)
