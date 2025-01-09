import pygame
from config import *
from game_objects import Paddle, Ball

class Game:
    def __init__(self, is_single_player=True):
        self.__is_single_player = is_single_player
        self.__paddle1 = Paddle(COURT_MARGIN + 10, SCREEN_HEIGHT // 2 - 50, 25, 100, COLORS["red"])
        self.__paddle2 = Paddle(SCREEN_WIDTH - COURT_MARGIN - 35, SCREEN_HEIGHT // 2 - 50, 25, 100, COLORS["blue"])
        self.__ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 15, COLORS["white"], 7, 7)
        self.__player1_score = 0
        self.__player2_score = 0
        self.__running = True
        self.__player1_name = "Player 1"
        self.__player2_name = "Player 2" if not is_single_player else "CPU"
        self.__winner = None

    @property
    def is_single_player(self):
        return self.__is_single_player
    
    @property
    def running(self):
        return self.__running
    
    @property
    def winner(self):
        return self.__winner

    @running.setter
    def running(self, value):
        self.__running = value
    
    @winner.setter
    def winner(self, value):
        self.__winner = value

    def __reset_game(self):
        """Method private untuk mereset game"""
        self.__player1_score = 0
        self.__player2_score = 0
        self.__winner = None
        self.__ball.reset()

    def __check_collision(self):
        """Method private untuk mengecek tabrakan"""
        if self.__ball.x - self.__ball.radius <= self.__paddle1.x + self.__paddle1.width and \
           self.__paddle1.y <= self.__ball.y <= self.__paddle1.y + self.__paddle1.height:
            self.__ball.x = self.__paddle1.x + self.__paddle1.width + self.__ball.radius
            self.__ball.xv *= -1.1

        if self.__ball.x + self.__ball.radius >= self.__paddle2.x and \
           self.__paddle2.y <= self.__ball.y <= self.__paddle2.y + self.__paddle2.height:
            self.__ball.x = self.__paddle2.x - self.__ball.radius
            self.__ball.xv *= -1.1

        if self.__ball.x <= COURT_MARGIN:
            self.__player2_score += 1
            self.__ball.reset(going_left=False)
        elif self.__ball.x >= SCREEN_WIDTH - COURT_MARGIN:
            self.__player1_score += 1
            self.__ball.reset(going_left=True)

        if self.__player1_score >= WINNING_SCORE:
            self.__winner = self.__player1_name
        elif self.__player2_score >= WINNING_SCORE:
            self.__winner = self.__player2_name

    def __handle_input(self):
        """Method private untuk menangani input"""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.__paddle1.move(-8)
        if keys[pygame.K_s]:
            self.__paddle1.move(8)

        if self.__is_single_player:
            self.__handle_cpu_movement()
        else:
            if keys[pygame.K_UP]:
                self.__paddle2.move(-8)
            if keys[pygame.K_DOWN]:
                self.__paddle2.move(8)

    def __handle_cpu_movement(self):
        """Method private untuk mengatur pergerakan CPU"""
        if self.__ball.xv > 0:
            paddle_center = self.__paddle2.y + self.__paddle2.height / 2
            if self.__ball.y < paddle_center:
                self.__paddle2.move(-7)
            elif self.__ball.y > paddle_center:
                self.__paddle2.move(7)

    def __draw_table_tennis_background(self):
        """Method private untuk menggambar latar belakang"""
        game_screen.fill(COLORS["black"])
        pygame.draw.rect(game_screen, COLORS["green"], 
                        (COURT_MARGIN, COURT_MARGIN, 
                         COURT_WIDTH, COURT_HEIGHT))
        pygame.draw.rect(game_screen, COLORS["white"],
                        (COURT_MARGIN, COURT_MARGIN,
                         COURT_WIDTH, COURT_HEIGHT), 2)
        pygame.draw.line(game_screen, COLORS["white"],
                        (SCREEN_WIDTH // 2, COURT_MARGIN),
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT - COURT_MARGIN),
                        2)
        pygame.draw.line(game_screen, COLORS["white"],
                        (COURT_MARGIN, SCREEN_HEIGHT // 2),
                        (SCREEN_WIDTH - COURT_MARGIN, SCREEN_HEIGHT // 2),
                        2)

    def __draw_victory_screen(self):
        """Method private untuk menggambar layar kemenangan"""
        game_screen.fill(COLORS["black"])
        victory_text = font.render(f"{self.__winner} MENANG!", True, COLORS["yellow"])
        play_again_text = small_font.render("Tekan SPACE untuk main lagi", True, COLORS["white"])
        menu_text = small_font.render("Tekan ESC untuk ke menu", True, COLORS["white"])

        game_screen.blit(victory_text,
            (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        game_screen.blit(play_again_text,
            (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        game_screen.blit(menu_text,
            (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

    def draw(self):
        """Method public untuk menggambar game"""
        if self.__winner:
            self.__draw_victory_screen()
        else:
            self.__draw_table_tennis_background()
            self.__paddle1.draw(game_screen)
            self.__paddle2.draw(game_screen)
            self.__ball.draw(game_screen)

            p1_text = small_font.render(f"{self.__player1_name}: {self.__player1_score}", True, COLORS["white"])
            p2_text = small_font.render(f"{self.__player2_name}: {self.__player2_score}", True, COLORS["white"])
            
            game_screen.blit(p1_text, (20, 10))
            game_screen.blit(p2_text, (SCREEN_WIDTH - p2_text.get_width() - 20, 10))

    def run(self):
        """Method public untuk menjalankan game"""
        clock = pygame.time.Clock()
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                if event.type == pygame.KEYDOWN:
                    if self.__winner:
                        if event.key == pygame.K_SPACE:
                            self.__reset_game()
                        elif event.key == pygame.K_ESCAPE:
                            return "menu"

            if not self.__winner:
                self.__handle_input()
                self.__ball.update()
                self.__check_collision()
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        return "quit"