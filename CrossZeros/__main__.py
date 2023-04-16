from CrossZeros.game import GameWindow
from pathlib import Path


def main():
    window = GameWindow()
    window.main_loop()
    print('Game over!')


if __name__ == '__main__':
    main()
