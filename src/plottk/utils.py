from typing import TypeVar

T = TypeVar("T")


def remove_duplicates(values: list[T]) -> list[T]:
    return list(dict.fromkeys(values).keys())
