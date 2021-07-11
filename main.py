import sys
import arcade_game

def main():
    while True:
        if arcade_game.game() == "QUIT":
            return 0

if __name__ == "__main__":
    sys.exit(main())     