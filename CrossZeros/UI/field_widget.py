import pygame
from time import sleep
from CrossZeros.UI.config import *
from CrossZeros.definition import Cell


class GameFieldView:
    def __init__(self, field):
        pygame.init()
        pygame.font.SysFont(FONT_NAME, TEXTS_FONT_SIZE)
        self.font = pygame.font.Font(None, TEXTS_FONT_SIZE)
        self.field = field
        self.title = 'Crosses & Zeroes'

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(self.title)
        self.display_the_initial_field()

    def display_the_initial_field(self):
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

        button_text = [TEXTS['new game with cross'], TEXTS['new game with zeros']]

        for button in 0, 1:
            self.screen.blit(
                self.font.render(button_text[button], True, COLOR_OF_BUTTONS_LABELS),
                (
                  button * (WIDTH // 2 + DEFLECTION_BUTTON) + ALIGNMENT_BUTTON_BY_X,
                  BUTTON_ZONE_SIZE // 2 + ALIGNMENT_BUTTON_BY_Y
                )
            )

    def draw_cell(self, i, j):
        if self.field.cells[i][j] == Cell.CROSS:
            text = 'X'
        elif self.field.cells[i][j] == Cell.ZERO:
            text = 'O'
        else:
            text = ''

        font = pygame.font.Font(None, FIGURE_FONT_SIZE)
        text = font.render(text, True, FIGURE_COLOR)

        self.screen.blit(
            text,
            (
             i * CELL_SIZE + ALIGNMENT_FIGURE_BY_X,
             j * CELL_SIZE + ALIGNMENT_FIGURE_BY_Y + BUTTON_ZONE_SIZE
            )
        )

    def draw_congratulation(self, player):
        congratulation_text = f'{TEXTS["congratulation"]} {player.name}'

        self.screen.blit(
            self.font.render(congratulation_text, True, CONGRATULATION_COLOR),
            CONGRATULATION_COORDINATES
        )

        pygame.display.flip()
        sleep(DURATION_CONGRATULATION)

    def check_coords_correct(self, x, y):
        if BUTTON_ZONE_SIZE <= y <= HEIGHT and 0 <= x <= WIDTH:
            return True
        return False

    def pressed_button_is_one(self, x):
        return x < self.field.size * CELL_SIZE // 2

    def get_coords(self, x, y):
        i = x // CELL_SIZE
        j = (y - BUTTON_ZONE_SIZE) // CELL_SIZE
        return i, j
