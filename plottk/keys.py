from dataclasses import dataclass


@dataclass(frozen=True)
class Keys:
    x: str
    y: str

    task: str
    group: str
    unit: str
