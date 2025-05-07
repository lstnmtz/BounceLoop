import pygame
import sys
import math
import random

# Config écran
WIDTH, HEIGHT = 360, 640
FPS = 60
LOOP_DURATION = 30
TOTAL_FRAMES = LOOP_DURATION * FPS
BALL_RADIUS = 20
SPEED = 3.5
MAX_BALLS = 200  # Sécurité anti-explosion

# Couleur dynamique
def get_color(t):
    r = 127 + 127 * math.sin(t * 0.02)
    g = 127 + 127 * math.sin(t * 0.02 + 2)
    b = 127 + 127 * math.sin(t * 0.02 + 4)
    return (int(r), int(g), int(b))

# Initialisation Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Bounce Loop")
clock = pygame.time.Clock()

# Son
bounce_sound = pygame.mixer.Sound("pop.mp3")

# Classe Balle
class Ball:
    def __init__(self, x=None, y=None):
        angle = random.uniform(0, 2 * math.pi)
        self.vx = SPEED * math.cos(angle)
        self.vy = SPEED * math.sin(angle)
        self.x = x if x is not None else random.randint(100, WIDTH - 100)
        self.y = y if y is not None else random.randint(100, HEIGHT - 100)
        self.color_offset = random.random() * 10

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.x - BALL_RADIUS < 0 or self.x + BALL_RADIUS > WIDTH:
            self.vx *= -1
            bounce_sound.play()

        if self.y - BALL_RADIUS < 0 or self.y + BALL_RADIUS > HEIGHT:
            self.vy *= -1
            bounce_sound.play()

    def draw(self, surface, frame):
        color = get_color(frame + self.color_offset * 60)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), BALL_RADIUS)

    def check_collision(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.hypot(dx, dy)
        return distance < BALL_RADIUS * 2

# Création des balles
balls = [Ball() for _ in range(2)]
initial_state = [(b.x, b.y, b.vx, b.vy) for b in balls]

# Historique des traînées
trail_length = 10
trail_history = [[] for _ in range(len(balls))]

# Boucle principale
frame = 0
running = True
while running:
    screen.fill((10, 10, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mise à jour
    for i, ball in enumerate(balls):
        ball.update()

        if len(trail_history) < len(balls):
            trail_history.append([])

        trail = trail_history[i]
        trail.append((ball.x, ball.y))
        if len(trail) > trail_length:
            trail.pop(0)

        # Traînée
        for j, (tx, ty) in enumerate(trail):
            alpha = int(255 * (j + 1) / trail_length)
            trail_color = (*get_color(frame + j * 2), alpha)
            s = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, trail_color, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
            screen.blit(s, (tx - BALL_RADIUS, ty - BALL_RADIUS))

        ball.draw(screen, frame)

    # Détection des collisions entre balles
    new_balls = []
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if balls[i].check_collision(balls[j]):
                if len(balls) + len(new_balls) < MAX_BALLS:
                    # Crée une nouvelle balle au centre des deux
                    mid_x = (balls[i].x + balls[j].x) / 2 + random.randint(-10, 10)
                    mid_y = (balls[i].y + balls[j].y) / 2 + random.randint(-10, 10)
                    new_balls.append(Ball(mid_x, mid_y))
                    bounce_sound.play()

    balls.extend(new_balls)

    pygame.display.flip()
    clock.tick(FPS)
    frame += 1

    if frame >= TOTAL_FRAMES:
        # Reset complet
        balls = [Ball(x, y) for x, y, _, _ in initial_state]
        trail_history = [[] for _ in range(len(balls))]
        frame = 0

pygame.quit()
sys.exit()
