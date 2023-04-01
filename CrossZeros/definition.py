from enum import Enum


class Cell(Enum):
    VOID = 0
    CROSS = 1
    ZERO = 2


FPS = 60
FIELD_SIZE = 15
CELL_SIZE = 40
BUTTON_ZONE_SIZE = 60

TEXTS = {
    'new game with zeros': 'Начать игру, крестиками',
    'new game with cross': 'Начать игру, ноликами',
    'congratulation': 'победил ',
    'human player name': 'Человек',
    'ai player name': 'ИИ'
}

TEMPLATE = {
    'xxxxx': 10000,
    '0xxxx0': 1000,
    '0xxxx': 500,
    'xxxx0': 500,
    'xxx0x': 400,
    'x0xxx': 400,
    'xx0xx': 400,
    '000xxx00': 100,
    '00xxx000': 100,
    '00xxx00': 80,
    '00xxx0': 75,
    '0xxx00': 75,
    '0xxx0': 50,
    '00xxx': 50,
    'xxx00': 50,
    '0xx0x': 25,
    'x0xx0': 25,
    '0x0xx': 25,
    'xx0x0': 25,
    'xx00x': 25,
    'x00xx': 25,
    '000xx000': 10,
    '0xx0': 5
}
