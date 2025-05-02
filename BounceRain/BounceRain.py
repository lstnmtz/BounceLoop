import pygame
import random
import math

# Initialisation
pygame.init()
pygame.mixer.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 720, 1280
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bounce Rain")

# Couleurs douces
SOFT_COLORS = [
    (173, 216, 230), # Light Blue
    (255, 182, 193), # Light Pink
    (144, 238, 144), # Light Green
    (255, 255, 224), # Light Yellow
    (221, 160, 221), # Plum
]

# Sons
BOUNCE_SOUND = pygame.mixer.Sound("bounce.mp3")  # Met un petit 'pop' discret
BOUNCE_SOUND.set_volume(0.2)  # Réduit le volume à 20%
RAIN_SOUND = pygame.mixer.Sound("rain_loop.mp3")  # Bruit de pluie en boucle
RAIN_SOUND.play(loops=-1)

# Gravité paramétrable
GRAVITY = 0.3

# Balles
balls = []

# FPS
CLOCK = pygame.time.Clock()
FPS = 30

# Classe Balle
class Ball:
    def __init__(self):
        self.radius = random.randint(10, 30)
        self.x = random.uniform(self.radius, WIDTH - self.radius)
        self.y = -self.radius
        self.color = random.choice(SOFT_COLORS)
        self.vx = 0.1
        self.vy = 0.1
        self.elasticity = 0.8 + random.uniform(0, 0.2)  # Coefficient de rebond
        self.stretch = 1.0  # Pour squash and stretch
        self.lifetime = random.randint(300, 600)  # Durée de vie en frames (5 à 10 secondes)

    def update(self):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1  # Réduire la durée de vie à chaque frame

        # Collisions avec les murs
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -self.elasticity
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx *= -self.elasticity

        # Collision avec le sol
        if self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy *= -self.elasticity
            # Squash effect
            self.stretch = max(0.6, 1 - abs(self.vy) * 0.015)

        # Rétablir progressivement le stretch
        if self.stretch < 1.0:
            self.stretch += (1.0 - self.stretch) * 0.2

    def draw(self, surface):
        stretch_y = self.radius * self.stretch
        stretch_x = self.radius * (2 - self.stretch)
        pygame.draw.ellipse(surface, self.color, (self.x - stretch_x, self.y - stretch_y, stretch_x * 2, stretch_y * 2))

# Gérer collisions entre balles
def handle_collisions():
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            b1 = balls[i]
            b2 = balls[j]
            dx = b2.x - b1.x
            dy = b2.y - b1.y
            distance = math.hypot(dx, dy)
            min_dist = b1.radius + b2.radius

            if distance < min_dist and distance > 0:
                overlap = min_dist - distance
                nx = dx / distance
                ny = dy / distance

                # Pousser les balles pour éviter la superposition
                b1.x -= nx * overlap / 2
                b1.y -= ny * overlap / 2
                b2.x += nx * overlap / 2
                b2.y += ny * overlap / 2

                # Jouer le son de rebond
                BOUNCE_SOUND.play()

                # Calcul des vitesses après collision (simplifié)
                tx, ty = -ny, nx
                dpTan1 = b1.vx * tx + b1.vy * ty
                dpTan2 = b2.vx * tx + b2.vy * ty

                dpNorm1 = b1.vx * nx + b1.vy * ny
                dpNorm2 = b2.vx * nx + b2.vy * ny

                # Conservation de la quantité de mouvement
                m1 = m2 = 1  # Même masse pour simplification
                new_dpNorm1 = (dpNorm1 * (m1 - m2) + 2 * m2 * dpNorm2) / (m1 + m2)
                new_dpNorm2 = (dpNorm2 * (m2 - m1) + 2 * m1 * dpNorm1) / (m1 + m2)

                b1.vx = tx * dpTan1 + nx * new_dpNorm1
                b1.vy = ty * dpTan1 + ny * new_dpNorm1
                b2.vx = tx * dpTan2 + nx * new_dpNorm2
                b2.vy = ty * dpTan2 + ny * new_dpNorm2

# Boucle principale
running = True
spawn_timer = 0

while running:
    CLOCK.tick(FPS)
    SCREEN.fill((0, 0, 0))  # Fond très sombre

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Générer une nouvelle balle toutes les X frames
    spawn_timer += 1
    if spawn_timer > 30:
        balls.append(Ball())
        spawn_timer = 0

    # Update et collisions
    for ball in balls:
        ball.update()
    handle_collisions()

    # Supprimer les balles dont la durée de vie est écoulée
    balls = [ball for ball in balls if ball.lifetime > 0]

    # Dessin
    for ball in balls:
        ball.draw(SCREEN)

    pygame.display.flip()

pygame.quit()
