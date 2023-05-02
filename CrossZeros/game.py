import pygame

from CrossZeros.ai import AI
from CrossZeros.UI.field_widget import GameFieldView

from CrossZeros.definition import *


class GameRoundManager:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player = 1 if player1.cell_type == Cell.CROSS else 0

        self.field = GameField()

        self._widget = GameFieldView(self.field, TEXTS)
        self._ai_player = AI(self.field, player2.cell_type)

    def checking_ending(self, i, j):
        line = [[] for _ in range(4)]

        for deviation in range(-4, 5):
            for n, ij in enumerate([
                                    (i + deviation, j),
                                    (i, j + deviation),
                                    (i + deviation, j + deviation),
                                    (i + deviation, j - deviation)
                                   ]):

                if 0 <= min(ij) and max(ij) < self.field.size:
                    line[n].append(ij)

        for n in range(4):
            count = 0

            for k in range(len(line[n])):
                x, y = line[n][k]

                if self.field.cells[x][y] == self.players[self.current_player].cell_type:
                    count += 1
                else:
                    count = 0

                if count > 4:
                    self._widget.draw_congratulation(self.players[self.current_player])
                    return True

        return False

    def checking_if_cell_is_empty(self, i, j):
        if self.field.cells[i][j] == Cell.VOID:
            return True
        return False

    def players_move(self, i, j):
        self.field.cells[i][j] = self.players[self.current_player].cell_type
        self._widget.draw_cell(i, j)

    def ai_move(self):
        self.current_player = 1 - self.current_player
        i, j = self._ai_player.choosing_move()
        self.players_move(i, j)
        return i, j

    def handle_click(self, x, y):
        i, j = self._widget.get_coords(x, y)

        if not self.checking_if_cell_is_empty(i, j):
            return False

        self.current_player = 1 - self.current_player
        self.players_move(i, j)

        if self.checking_ending(i, j):
            return True

        i, j = self.ai_move()

        return self.checking_ending(i, j)

    def check_coords_correct(self, x, y):
        return self._widget.check_coords_correct(x, y)

    def pressed_button_is_one(self, x):
        return self._widget.pressed_button_is_one(x)


class Game:
    def __init__(self, field_size=FIELD_SIZE, fps=FPS):
        self.field_size = field_size
        self.fps = fps
        self.restart_game(True)

    def restart_game(self, pressed_button_is_one):
        if pressed_button_is_one:
            self.game_manager = GameRoundManager(
                Player(HUMAN_PLAYER_NAME, Cell.CROSS),
                Player(AI_PLAYER_NAME, Cell.ZERO)
            )
        else:
            self.game_manager = GameRoundManager(
                Player(HUMAN_PLAYER_NAME, Cell.ZERO),
                Player(AI_PLAYER_NAME, Cell.CROSS)
            )
            self.game_manager.ai_move()

    def main_loop(self):
        finished = False
        end = False
        clock = pygame.time.Clock()

        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    if self.game_manager.check_coords_correct(x, y):
                        if not end:
                            end = self.game_manager.handle_click(x, y)
                    else:
                        end = False
                        self.restart_game(
                            self.game_manager.pressed_button_is_one(x)
                        )

            pygame.display.flip()
            clock.tick(self.fps)
