import random

from CrossZeros.definition import Cell, TEMPLATE


class AI:
    def __init__(self, field, players_cell_type, blunt=False, template=TEMPLATE):
        self.field = field
        self.cell_type = players_cell_type

        if players_cell_type == Cell.CROSS:
            self.opponent_cell_type = Cell.ZERO
        else:
            self.opponent_cell_type = Cell.CROSS

        self.blunt = blunt
        self.template = template

        self.possibles_move = []

    def _template_reconciliation(self, s):
        if self.blunt:
            return 1

        weight = 0

        for k in self.template:
            if k in s:
                weight += self.template[k]

        return weight

    def _variant_evaluation(self, i, j, cell_type):
        s = ['' for _ in range(4)]

        for deviation in range(-4, 5):
            for n, xy in enumerate([
                                    (i + deviation, j),
                                    (i, j + deviation),
                                    (i + deviation, j + deviation),
                                    (i + deviation, j - deviation)
                                  ]):
                cur_x, cur_y = xy

                if cur_x == i and cur_y == j:
                    s[n] += 'x'
                else:
                    if 0 <= min(cur_x, cur_y) and max(cur_x, cur_y) < self.field.size:

                        if self.field.cells[cur_x][cur_y] == Cell.VOID:
                            s[n] += '0'
                        elif self.field.cells[cur_x][cur_y] == cell_type:
                            s[n] += 'x'
                        else:
                            s[n] += '1'

        return sum(map(self._template_reconciliation, s))

    def _variant_choosing(self, cell_type):
        max_weight = 0
        i, j = random.choice(self.possibles_move)

        for cur_x, cur_y in self.possibles_move:
            current_weight = self._variant_evaluation(cur_x, cur_y, cell_type)

            if max_weight < current_weight:
                max_weight = current_weight
                i, j = cur_x, cur_y

        return [max_weight, (i, j)]

    def choosing_move(self):
        self.possibles_move = []

        for x in range(self.field.size):
            for y in range(self.field.size):
                if self.field.cells[x][y] != Cell.VOID:

                    for cur_x in range(x - 2, x + 3):
                        for cur_y in range(y - 2, y + 3):

                            if 0 <= min(cur_x, cur_y) and max(cur_x, cur_y) < self.field.size:
                                if self.field.cells[cur_x][cur_y] == Cell.VOID:
                                    self.possibles_move.append((cur_x, cur_y))

        if not self.possibles_move:
            i = self.field.size // 2
            j = self.field.size // 2
        else:
            attack = self._variant_choosing(self.cell_type)
            defense = self._variant_choosing(self.opponent_cell_type)
            if attack[0] >= defense[0]:
                i, j = attack[1]
            else:
                i, j = defense[1]

        return i, j
