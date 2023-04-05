import time
import pygame
from CrossZeros.ai import AI
from CrossZeros.definition import *


class Player:
    def __init__(self, name, cell_type):
        self.name = name
        self.cell_type = cell_type


class GameField:
    def __init__(self):
        self.height = FIELD_SIZE
        self.width = FIELD_SIZE
        self.cells = [[Cell.VOID] * self.width for _ in range(self.height)]


class GameFieldView:
    def __init__(self, field):
        pygame.init()
        pygame.font.SysFont('arial', 32)
        self.font = pygame.font.Font(None, 32)

        self.field = field
        self.width = FIELD_SIZE * CELL_SIZE
        self.height = self.width + BUTTON_ZONE_SIZE
        self.title = 'Crosses & Zeroes'

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.display_the_initial_field()

    def display_the_initial_field(self):
        for x in range(0, self.width, CELL_SIZE):
            for y in range(0, self.width, CELL_SIZE):

                pygame.draw.rect(
                    self.screen,
                    (125, 125, 125),
                    (x + 2, BUTTON_ZONE_SIZE + y + 2, CELL_SIZE - 4, CELL_SIZE - 4)
                )

        for x in 0, self.width // 2:

            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                (2 + x, 2, self.width // 2 - 4, BUTTON_ZONE_SIZE - 4)
            )

        button_text = {0: TEXTS['new game with cross'], 1: TEXTS['new game with zeros']}

        for b in 0, 1:

            self.screen.blit(
                self.font.render(button_text[b], True, (125, 125, 125)),
                (b * (self.width // 2 + 10) + 15, BUTTON_ZONE_SIZE // 2 - 10)
            )

    def draw_cell(self, i, j):
        if self.field.cells[i][j] == Cell.CROSS:
            text = 'X'
        elif self.field.cells[i][j] == Cell.ZERO:
            text = 'O'
        else:
            text = ''

        font = pygame.font.Font(None, 38)
        text = font.render(text, True, (255, 255, 255))

        self.screen.blit(
            text,
            (i * CELL_SIZE + 11, j * CELL_SIZE + 8 + BUTTON_ZONE_SIZE)
        )

    def draw_congratulation(self, player):
        congratulation_text = f'{TEXTS["congratulation"]} {player.name}'

        self.screen.blit(
            self.font.render(congratulation_text, True, (200, 200, 255)),
            (self.width // 2 - 95, BUTTON_ZONE_SIZE + self.width // 2 + 10)
        )

        pygame.display.flip()
        time.sleep(2)

    def check_coords_correct(self, x, y):
        if BUTTON_ZONE_SIZE <= y <= self.height and 0 <= x <= self.width:
            return True
        return False

    @staticmethod
    def get_coords(x, y):
        i = x // CELL_SIZE
        j = (y - BUTTON_ZONE_SIZE) // CELL_SIZE
        return i, j


class GameRoundManager:
    def __init__(self, player1: Player, player2: Player):
        self.players = [player1, player2]
        self.current_player = 1 if player1.cell_type == Cell.CROSS else 0
        self.field = GameField()
        self.field_widget = GameFieldView(self.field)
        self.ai_player = AI(self.field.cells, player2.cell_type)

    def checking_ending(self, i, j):
        line = [[] for _ in range(4)]

        for deviation in range(-4, 5):
            for n, ij in enumerate([
                                    (i + deviation, j),
                                    (i, j + deviation),
                                    (i + deviation, j + deviation),
                                    (i + deviation, j - deviation)
                                   ]):

                if 0 <= min(ij) and max(ij) < FIELD_SIZE:
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
                    self.field_widget.draw_congratulation(self.players[self.current_player])
                    return True

        return False

    def checking_if_cell_is_empty(self, i, j):
        if self.field.cells[i][j] == Cell.VOID:
            return True
        return False

    def players_move(self, i, j):
        self.field.cells[i][j] = self.players[self.current_player].cell_type
        self.field_widget.draw_cell(i, j)

    def ai_move(self):
        self.current_player = 1 - self.current_player
        i, j = self.ai_player.choosing_move()
        self.players_move(i, j)
        return i, j

    def handle_click(self, x, y):
        i, j = self.field_widget.get_coords(x, y)

        if not self.checking_if_cell_is_empty(i, j):
            return False

        self.current_player = 1 - self.current_player
        self.players_move(i, j)

        if self.checking_ending(i, j):
            return True

        i, j = self.ai_move()

        return self.checking_ending(i, j)


class GameWindow:
    def __init__(self):
        player1 = Player(TEXTS['human player name'], Cell.CROSS)
        player2 = Player(TEXTS['ai player name'], Cell.ZERO)
        self.game_manager = GameRoundManager(player1, player2)

    def restart_game(self, x):
        if x < FIELD_SIZE * CELL_SIZE // 2:
            player1 = Player(TEXTS['human player name'], Cell.CROSS)
            player2 = Player(TEXTS['ai player name'], Cell.ZERO)
            self.game_manager = GameRoundManager(player1, player2)
        else:
            player1 = Player(TEXTS['human player name'], Cell.ZERO)
            player2 = Player(TEXTS['ai player name'], Cell.CROSS)
            self.game_manager = GameRoundManager(player1, player2)
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

                    if self.game_manager.field_widget.check_coords_correct(x, y):
                        if not end:
                            end = self.game_manager.handle_click(x, y)
                    else:
                        end = False
                        self.restart_game(x)

            pygame.display.flip()
            clock.tick(FPS)
