from dataclasses import dataclass

from classes.auth.user import User
from classes.decks.game_deck import GameDeck
from classes.enums.directions import Directions


@dataclass
class Game:
    users: list[User]
    deck: GameDeck
    cur_user_index: int = 0
    direction: Directions = Directions.CLOCKWISE

    def append_user(self, user: User):
        if len(self.users) <= 4:
            print(self.users)
            self.users.append(user)
        else:
            raise ValueError("Слишком много пользователей")

    @property
    def is_started(self) -> bool:
        return True if len(self.users) == 4 else False

    def next_player(self):
        if self.direction == Directions.CLOCKWISE:
            if self.cur_user_index != 3:
                self.cur_user_index += 1
            else:
                self.cur_user_index = 0
        elif self.direction == Directions.COUNTER_CLOCKWISE:
            if self.cur_user_index != 0:
                self.cur_user_index -= 1
            else:
                self.cur_user_index = 3
