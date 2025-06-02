import functools
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    def __init__(self):
        self._registry: dict[str, T] = {}

    def register(self, name: str) -> Callable[[T], T]:
        return functools.partial(self.register_item, name)

    def register_item(self, name: str, item: T) -> T:
        if name in self._registry:
            raise ValueError(f"Item with name '{name}' already registered.")
        self._registry[name] = item
        return item

    def get(self, name: str) -> T:
        if name not in self._registry:
            raise KeyError(f"Item with name '{name}' not found.")
        return self._registry[name]
