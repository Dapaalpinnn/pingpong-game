# game.py
import pygame
from config import *
from game_objects import Paddle
from ball import Ball

class Game:
    def __init__(self, is_single_player=True):
        self.is_single_player = is_single_player
        self.paddle1 = Paddle(COURT_MARGIN + 10, SCREEN_HEIGHT // 2 - 50, 25, 100, COLORS["red"])
        self.paddle2 = Paddle(SCREEN_WIDTH - COURT_MARGIN - 35, SCREEN_HEIGHT // 2 - 50, 25, 100, COLORS["blue"])
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 15, COLORS["white"], 7, 7)
        self.player1_score = 0
        self.player2_score = 0
        self.running = True
        self.player1_name = "Player 1"
        self.player2_name = "Player 2" if not is_single_player else "CPU"
        self.winner = None

    def check_collision(self):
        if self.ball.x - self.ball.radius <= self.paddle1.x + self.paddle1.width and \
           self.paddle1.y <= self.ball.y <= self.paddle1.y + self.paddle1.height:
            self.ball.x = self.paddle1.x + self.paddle1.width + self.ball.radius
            self.ball.xv *= -1.1

        if self.ball.x + self.ball.radius >= self.paddle2.x and \
           self.paddle2.y <= self.ball.y <= self.paddle2.y + self.paddle2.height:
            self.ball.x = self.paddle2.x - self.ball.radius
            self.ball.xv *= -1.1

        if self.ball.x <= COURT_MARGIN:
            self.player2_score += 1
            self.ball.reset(going_left=False)
        elif self.ball.x >= SCREEN_WIDTH - COURT_MARGIN:
            self.player1_score += 1
            self.ball.reset(going_left=True)

        if self.player1_score >= WINNING_SCORE:
            self.winner = self.player1_name
        elif self.player2_score >= WINNING_SCORE:
            self.winner = self.player2_name

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.paddle1.move(-8)
        if keys[pygame.K_s]:
            self.paddle1.move(8)

        if self.is_single_player:
            if self.ball.xv > 0:
                if self.ball.y < self.paddle2.y + self.paddle2.height / 2:
                    self.paddle2.move(-7)
                elif self.ball.y > self.paddle2.y + self.paddle2.height / 2:
                    self.paddle2.move(7)
        else:
            if keys[pygame.K_UP]:
                self.paddle2.move(-8)
            if keys[pygame.K_DOWN]:
                self.paddle2.move(8)

    def draw_table_tennis_background(self):
        # Gambar background hitam
        game_screen.fill(COLORS["black"])
        
        # Gambar lapangan hijau
        pygame.draw.rect(game_screen, COLORS["green"], 
                        (COURT_MARGIN, COURT_MARGIN, 
                         COURT_WIDTH, COURT_HEIGHT))
        
        # Gambar garis tepi lapangan
        pygame.draw.rect(game_screen, COLORS["white"],
                        (COURT_MARGIN, COURT_MARGIN,
                         COURT_WIDTH, COURT_HEIGHT), 2)
        
        # Garis tengah vertikal (net)
        pygame.draw.line(game_screen, COLORS["white"],
                        (SCREEN_WIDTH // 2, COURT_MARGIN),
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT - COURT_MARGIN),
                        2)
        
        # Garis tengah horizontal
        pygame.draw.line(game_screen, COLORS["white"],
                        (COURT_MARGIN, SCREEN_HEIGHT // 2),
                        (SCREEN_WIDTH - COURT_MARGIN, SCREEN_HEIGHT // 2),
                        2)

    def draw_victory_screen(self):
        game_screen.fill(COLORS["black"])
        victory_text = font.render(f"{self.winner} MENANG!", True, COLORS["yellow"])
        play_again_text = small_font.render("Tekan SPACE untuk main lagi", True, COLORS["white"])
        menu_text = small_font.render("Tekan ESC untuk ke menu", True, COLORS["white"])

        game_screen.blit(victory_text,
            (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        game_screen.blit(play_again_text,
            (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        game_screen.blit(menu_text,
            (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

    def draw(self):
        if self.winner:
            self.draw_victory_screen()
        else:
            self.draw_table_tennis_background()
            self.paddle1.draw(game_screen)
            self.paddle2.draw(game_screen)
            self.ball.draw(game_screen)

            p1_text = small_font.render(f"{self.player1_name}: {self.player1_score}", True, COLORS["white"])
            p2_text = small_font.render(f"{self.player2_name}: {self.player2_score}", True, COLORS["white"])
            
            game_screen.blit(p1_text, (20, 10))
            game_screen.blit(p2_text, (SCREEN_WIDTH - p2_text.get_width() - 20, 10))

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if self.winner:
                        if event.key == pygame.K_SPACE:
                            self.player1_score = 0
                            self.player2_score = 0
                            self.winner = None
                            self.ball.reset()
                        elif event.key == pygame.K_ESCAPE:
                            return "menu"

            if not self.winner:
                self.handle_input()
                self.ball.update()
                self.check_collision()
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        return "quit"