from classes.enums.directions import Directions


def next_player_index(cur_index: int, direction: Directions) -> int:
    if direction == Directions.CLOCKWISE:
        if cur_index != 3:
            return cur_index + 1
        else:
            return 0
    elif direction == Directions.COUNTER_CLOCKWISE:
        if cur_index != 0:
            return cur_index - 1
        else:
            return 3
