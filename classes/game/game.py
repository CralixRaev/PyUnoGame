from dataclasses import dataclass
from classes.auth.user import User


@dataclass
class Game:
    users: list[User]

    def append_user(self, user: User):
        if len(self.users) <= 4:
            print(self.users)
            self.users.append(user)
        else:
            raise ValueError("Слишком много пользователей")

    @property
    def is_started(self) -> bool:
        return True if len(self.users) == 4 else False