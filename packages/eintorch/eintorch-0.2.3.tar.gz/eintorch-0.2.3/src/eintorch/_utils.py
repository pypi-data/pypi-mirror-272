from __future__ import annotations

import inspect
from inspect import signature
from typing import Any, Callable

SINGLE_POSITIONALS = frozenset(
    (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
)
try:
    from IPython import get_ipython

    ipy = get_ipython()
except ImportError:
    ipy = None


def is_autoreload_enabled():
    if ipy is not None:
        line = ipy.magics_manager.magics["line"]
        if "autoreload" in line:
            return line["autoreload"].__self__._reloader.enabled
    return False


def get_first_arg_name(fun: Callable[..., Any]) -> str:
    return inspect.getfullargspec(fun).args[0]


def count_positional_args(fun: Callable[..., Any]) -> int | None:
    sig = signature(fun)
    if not all(p.kind in SINGLE_POSITIONALS for p in sig.parameters.values()):
        return None
    return len(sig.parameters)
