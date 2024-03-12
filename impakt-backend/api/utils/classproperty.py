from functools import update_wrapper
from typing import Any


class classproperty:
    """Decorator for creating class properties.

    This class is a decorator that can be used to create properties that are the same for all instances of a class.

    Args:
        fget (Any): The function for getting the property value.

    Attributes:
        fget (Any): The function for getting the property value.
    """

    def __init__(self, fget: Any) -> None:
        """Initializes the classproperty.

        Args:
            fget (Any): The function for getting the property value.
        """
        self.fget = fget
        update_wrapper(self, fget)

    def __get__(self, obj, cls=None) -> Any:
        """Gets the property value.

        This method is called when the property is accessed. It calls the function passed to the constructor with the class as the argument.

        Args:
            obj: The instance that the property was accessed through, or None if the property was accessed through the class.
            cls (optional): The class that the property was accessed through.

        Returns:
            Any: The property value.
        """
        if cls is None:
            cls = type(obj)
        return self.fget(cls)
