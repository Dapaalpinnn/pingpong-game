# main.py
import pygame
import sys
from game import Game
from menu import show_menu

def main():
    while True:
        is_single_player = show_menu()
        if is_single_player is None:
            break
        
        result = Game(is_single_player).run()
        if result == "quit":
            break
            
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()