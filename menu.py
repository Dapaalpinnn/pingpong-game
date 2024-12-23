import pygame
from config import *

def show_menu():
    running = True

    while running:
        game_screen.fill(COLORS["black"])

        title_text = font.render("Table Tennis", True, COLORS["white"])
        single_player_text = small_font.render("Single Player", True, COLORS["white"])
        two_player_text = small_font.render("Two Player", True, COLORS["white"])
        quit_text = small_font.render("Quit", True, COLORS["white"])

        title_x = SCREEN_WIDTH // 2 - title_text.get_width() // 2
        single_player_x = SCREEN_WIDTH // 2 - single_player_text.get_width() // 2
        two_player_x = SCREEN_WIDTH // 2 - two_player_text.get_width() // 2
        quit_x = SCREEN_WIDTH // 2 - quit_text.get_width() // 2

        title_y = 100
        single_player_y = 200
        two_player_y = 250
        quit_y = 300

        single_player_rect = pygame.Rect(single_player_x, single_player_y,
                                       single_player_text.get_width(), single_player_text.get_height())
        two_player_rect = pygame.Rect(two_player_x, two_player_y,
                                    two_player_text.get_width(), two_player_text.get_height())
        quit_rect = pygame.Rect(quit_x, quit_y,
                              quit_text.get_width(), quit_text.get_height())

        game_screen.blit(title_text, (title_x, title_y))
        game_screen.blit(single_player_text, (single_player_x, single_player_y))
        game_screen.blit(two_player_text, (two_player_x, two_player_y))
        game_screen.blit(quit_text, (quit_x, quit_y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if single_player_rect.collidepoint(mouse_pos):
                    return True
                if two_player_rect.collidepoint(mouse_pos):
                    return False
                if quit_rect.collidepoint(mouse_pos):
                    return None