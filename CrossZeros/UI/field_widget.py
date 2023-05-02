import pygame
from time import sleep
from CrossZeros.UI.config import *
from CrossZeros.definition import Cell


class GameFieldView:
    def __init__(self, field, texts):
        self.field = field
        self.texts = texts

        pygame.init()
        pygame.font.SysFont(FONT_NAME, TEXTS_FONT_SIZE)

        self.font = pygame.font.Font(None, TEXTS_FONT_SIZE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(self.texts['title'])

        self.display_new_field()

    def display_new_field(self):
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, WIDTH, CELL_SIZE):

                pygame.draw.rect(
                    self.screen,
                    FIELD_COLOR,
                    (
                     x + LINE_WIDTH,
                     BUTTON_ZONE_SIZE + y + LINE_WIDTH,
                     CELL_SIZE - LINE_WIDTH*2,
                     CELL_SIZE - LINE_WIDTH*2
                     )
                )

        for x in 0, WIDTH // 2:

            pygame.draw.rect(
                self.screen,
                BUTTONS_COLOR,
                (
                 LINE_WIDTH + x,
                 LINE_WIDTH, WIDTH // 2 - LINE_WIDTH*2,
                 BUTTON_ZONE_SIZE - LINE_WIDTH*2
                 )
            )

        button_text = [self.texts['new game with cross'], self.texts['new game with zeros']]

        for n in 0, 1:
            self.text_out(
                text=button_text[n],
                color=COLOR_OF_BUTTONS_LABELS,
                coordinates=(
                    n * WIDTH // 2 + WIDTH // 4,
                    BUTTON_ZONE_SIZE // 2
                )
            )

    def draw_cell(self, i, j):
        if self.field.cells[i][j] == Cell.CROSS:
            text = 'X'
        elif self.field.cells[i][j] == Cell.ZERO:
            text = 'O'
        else:
            text = ''

        self.text_out(
            text=text,
            color=FIGURE_COLOR,
            coordinates=(
                i * CELL_SIZE + CELL_SIZE // 2,
                j * CELL_SIZE + CELL_SIZE // 2 + BUTTON_ZONE_SIZE
            )
        )

    def draw_congratulation(self, player):
        self.text_out(
            text=f'{self.texts["congratulation"]} {player.name}',
            color=CONGRATULATION_COLOR,
            coordinates=(
                WIDTH // 2,
                BUTTON_ZONE_SIZE + WIDTH // 2
            )
        )

        pygame.display.flip()
        sleep(DURATION_CONGRATULATION)

    def text_out(self, text, color, coordinates):
        text = self.font.render(text, True, color)

        text_rect = text.get_rect()
        text_rect.center = coordinates

        self.screen.blit(text, text_rect)

    @staticmethod
    def check_coords_correct(x, y):
        if BUTTON_ZONE_SIZE <= y <= HEIGHT and 0 <= x <= WIDTH:
            return True
        return False

    def pressed_button_is_one(self, x):
        return x < self.field.size * CELL_SIZE // 2

    @staticmethod
    def get_coords(x, y):
        i = x // CELL_SIZE
        j = (y - BUTTON_ZONE_SIZE) // CELL_SIZE
        return i, j
