import inspect
from functools import wraps
from typing import Callable, Dict


def default_injection(params: Dict[str, Callable]):
    def decorate(cls):
        original_init = cls.__init__
        sig = inspect.signature(original_init)
        @wraps(original_init)
        def __init__(self, *args, **kwargs):
            bound = sig.bind_partial(self, *args, **kwargs)

            # inject only if not provided
            for pname, pvalue in params.items():
                if pname not in bound.arguments:
                    bound.arguments[pname] = pvalue()

            original_init(*bound.args, **bound.kwargs)

        cls.__init__ = __init__
        return cls

    return decorate