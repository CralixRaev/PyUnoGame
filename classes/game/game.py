from dataclasses import dataclass
from classes.auth.user import User


@dataclass
class Game:
    users: list[User]
