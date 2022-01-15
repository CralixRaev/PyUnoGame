from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    address: tuple[str, int] = None
