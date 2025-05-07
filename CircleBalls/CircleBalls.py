import pygame
import random
import math
import os

# Initialisation
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial", 36, bold=True)
WIDTH, HEIGHT = 720, 1280  # Format 9:16 vertical
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TikTok Ball Animation")
clock = pygame.time.Clock()
FPS = 60

def draw_ball_counter(surface, count):
    challenge_text = font.render("How many balls?", True, (255, 255, 255))
    challenge_text_rect = challenge_text.get_rect(center=(circle_center[0], circle_center[1] - circle_radius - 60))
    surface.blit(challenge_text, challenge_text_rect)

    text = font.render(f"Balls : {count}", True, (255, 255, 255))
    text_rect = text.get_rect(center=(circle_center[0], circle_center[1] + circle_radius + 60))
    surface.blit(text, text_rect)

# Couleurs
def random_color():
    return tuple(random.randint(50, 255) for _ in range(3))

# Chargement sécurisé d’un son "pop"
try:
    pop_sound = pygame.mixer.Sound("neymar-brainrot.mp3")  # Ton fichier son
except pygame.error:
    print("⚠️ Fichier 'pop.wav' non trouvé ou erreur de lecture.")
    pop_sound = None

sound_channel = pygame.mixer.Channel(0)  # Utiliser le canal 0 pour la musique

sound_lock = False  # Verrou pour empêcher les sons superposés
sound_lock_time = 0  # Temps du dernier son joué

# Cercle
circle_radius = WIDTH // 2 - 40
circle_center = (WIDTH // 2, HEIGHT // 2)

# Balle
class Ball:
    def __init__(self, x, y, angle, speed, color=None):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.color = color or random_color()
        self.radius = 10
        self.last_bounced = False
        self.last_bounce_time = 0  # Temps du dernier rebond

    def move(self):
        # Calcul du déplacement
        vx = math.cos(self.angle) * self.speed
        vy = math.sin(self.angle) * self.speed

        # Nouvelle position potentielle
        new_x = self.x + vx
        new_y = self.y + vy

        # Vecteur centre -> nouvelle position
        dx = new_x - circle_center[0]
        dy = new_y - circle_center[1]
        dist = math.hypot(dx, dy)

        if dist + self.radius > circle_radius:
            # Normalisé
            nx = dx / dist
            ny = dy / dist

            # Vecteur incident (vx, vy)
            v_dot_n = vx * nx + vy * ny

            # Vecteur réfléchi = v - 2*(v·n)*n
            rx = vx - 2 * v_dot_n * nx
            ry = vy - 2 * v_dot_n * ny

            # Mise à jour de l'angle selon le vecteur réfléchi
            self.angle = math.atan2(ry, rx)

            # Repositionnement juste à l'intérieur du cercle
            edge_x = circle_center[0] + nx * (circle_radius - self.radius)
            edge_y = circle_center[1] + ny * (circle_radius - self.radius)
            self.x = edge_x
            self.y = edge_y

            # Indiquer que la balle a rebondi
            self.last_bounced = True

            # Relancer la musique
            if pop_sound:
                if not sound_channel.get_busy():  # Si le canal est libre
                    sound_channel.play(pop_sound)
                else:
                    sound_channel.stop()  # Arrêter la musique en cours
                    sound_channel.play(pop_sound)
        else:
            self.x = new_x
            self.y = new_y
            self.last_bounced = False  # Pas de rebond

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

# Initialisation
balls = [Ball(circle_center[0], circle_center[1], random.uniform(0, 2 * math.pi), 2.5)]
MAX_BALLS = 10000
SPEED_INCREMENT = 0.25

# Timer avant le début
start_time = pygame.time.get_ticks()
while True:
    screen.fill((10, 10, 20))  # Fond sombre

    # Calcul du temps écoulé
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    countdown = 3 - elapsed_time

    if countdown > 0:
        # Affichage du compte à rebours
        timer_text = font.render(f"Starting in {countdown}...", True, (255, 255, 255))
        timer_text_rect = timer_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(timer_text, timer_text_rect)
        pygame.display.flip()
        clock.tick(FPS)
    else:
        break
    
# Boucle principale
running = True
while running:
    screen.fill((10, 10, 20))  # Fond sombre

    # Cercle de confinement
    pygame.draw.circle(screen, (255, 255, 255), circle_center, circle_radius, 2)

    new_balls = []

    for ball in balls:
        ball.move()

        # Contrôle adaptatif de la duplication
        duplication_probability = max(0.8 - (len(balls) / MAX_BALLS), 0.05)

        if ball.last_bounced and len(balls) + len(new_balls) < MAX_BALLS:
            if random.random() < duplication_probability:
                angle_offset = random.uniform(-0.3, 0.3)
                new_ball = Ball(
                    ball.x,
                    ball.y,
                    ball.angle + angle_offset,
                    ball.speed + SPEED_INCREMENT
                )
                new_balls.append(new_ball)

        ball.draw(screen)


    balls.extend(new_balls)

    # Quitter proprement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_ball_counter(screen, len(balls))
    pygame.display.flip()
    clock.tick(FPS)

# Réinitialiser le verrou sonore après 200 ms
if sound_lock and pygame.time.get_ticks() - sound_lock_time > 200:
    sound_lock = False

pygame.quit()
