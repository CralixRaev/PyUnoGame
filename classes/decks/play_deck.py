from collections import deque

from classes.cards.card import Card


class PlayDeck:
    """
    Игровая стопка карт.
    """

    def __init__(self, maxsize: int = 1):
        """
        Инициализация поля
        :param maxsize: Количество последних карт, которые будут хранится
        """
        # для чего хранить N последних карт?
        # помним, что мы хотим реализовать максимально универсальную реализацию
        # к примеру, мы можем сделать такую колоду, где если три последние карты
        # одинакового номинала, и человек кидает особую карту, то он скидывает все карты
        # этого номинала
        self.cards = deque([], maxsize)

    def append_card(self, card: Card) -> None | bool:
        if card.possible_move(self.cards[0]):
            self.cards.appendleft(card)
        else:
            return False  # почему не исключение?
            # т.к. эта вещь будет проверяться при каждой попытке добавить карту игроком, то тут
            # не было бы очень приятно замедлять работу программы тонной исключений