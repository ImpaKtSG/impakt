from functools import update_wrapper
from typing import Any


class classproperty:
    def __init__(self, fget: Any) -> None:
        self.fget = fget
        update_wrapper(self, fget)

    def __get__(self, obj, cls=None) -> Any:
        if cls is None:
            cls = type(obj)
        return self.fget(cls)
