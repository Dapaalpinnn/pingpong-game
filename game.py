import pygame
import sys

# Initialize Pygame
pygame.init()

# Colors
COLORS = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 127, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "green": (34, 139, 34)
}

# Screen and Court Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COURT_MARGIN = 50  # Margin from screen edges
COURT_WIDTH = SCREEN_WIDTH - (2 * COURT_MARGIN)
COURT_HEIGHT = SCREEN_HEIGHT - (2 * COURT_MARGIN)
WINNING_SCORE = 5

# Initialize Game Screen
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Table Tennis")
font = pygame.font.SysFont("monospace", 50)
small_font = pygame.font.SysFont("monospace", 30)

class GameObject:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface):
        raise NotImplementedError

class Paddle(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, color)
        self.width = width
        self.height = height

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def move(self, dy):
        self.y += dy
        # Membatasi paddle agar tetap dalam area lapangan
        self.y = max(COURT_MARGIN, min(self.y, SCREEN_HEIGHT - COURT_MARGIN - self.height))

class Ball(GameObject):
    def __init__(self, x, y, radius, color, xv, yv):
        super().__init__(x, y, color)
        self.radius = radius
        self.xv = xv
        self.yv = yv
        self.initial_speed = (xv, yv)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        self.x += self.xv
        self.y += self.yv

        # Benturan dengan batas atas dan bawah lapangan
        if self.y - self.radius <= COURT_MARGIN:  # Batas atas lapangan
            self.y = COURT_MARGIN + self.radius
            self.yv *= -1
        elif self.y + self.radius >= SCREEN_HEIGHT - COURT_MARGIN:  # Batas bawah lapangan
            self.y = SCREEN_HEIGHT - COURT_MARGIN - self.radius
            self.yv *= -1

    def reset(self, going_left=False):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.xv = -self.initial_speed[0] if going_left else self.initial_speed[0]
        self.yv = self.initial_speed[1]

class Game:
    def __init__(self, is_single_player=True):
        self.is_single_player = is_single_player
        # Menyesuaikan posisi paddle dengan batas lapangan
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
        # Collision with paddles
        if self.ball.x - self.ball.radius <= self.paddle1.x + self.paddle1.width and \
           self.paddle1.y <= self.ball.y <= self.paddle1.y + self.paddle1.height:
            self.ball.x = self.paddle1.x + self.paddle1.width + self.ball.radius
            self.ball.xv *= -1.1  # Sedikit percepatan setiap kali memantul

        if self.ball.x + self.ball.radius >= self.paddle2.x and \
           self.paddle2.y <= self.ball.y <= self.paddle2.y + self.paddle2.height:
            self.ball.x = self.paddle2.x - self.ball.radius
            self.ball.xv *= -1.1  # Sedikit percepatan setiap kali memantul

        # Scoring
        if self.ball.x <= COURT_MARGIN:  # Bola melewati batas kiri lapangan
            self.player2_score += 1
            self.ball.reset(going_left=False)
        elif self.ball.x >= SCREEN_WIDTH - COURT_MARGIN:  # Bola melewati batas kanan lapangan
            self.player1_score += 1
            self.ball.reset(going_left=True)

        # Check for winner
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
            # Improved AI movement
            if self.ball.xv > 0:  # Only move when ball is coming towards AI
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
        # Draw black background
        game_screen.fill(COLORS["black"])
        
        # Draw green court
        pygame.draw.rect(game_screen, COLORS["green"], 
                        (COURT_MARGIN, COURT_MARGIN, 
                         COURT_WIDTH, COURT_HEIGHT))
        
        # Draw center line
        pygame.draw.line(game_screen, COLORS["white"],
                        (SCREEN_WIDTH // 2, COURT_MARGIN),
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT - COURT_MARGIN), 2)
        
        # Draw court border
        pygame.draw.rect(game_screen, COLORS["white"],
                        (COURT_MARGIN, COURT_MARGIN,
                         COURT_WIDTH, COURT_HEIGHT), 2)

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

            # Draw scores and player names
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
                            # Reset game
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

if __name__ == "__main__":
    while True:
        is_single_player = show_menu()
        if is_single_player is None:
            break
        
        result = Game(is_single_player).run()
        if result == "quit":
            break
            
    pygame.quit()
    sys.exit()