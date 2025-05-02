import pygame
import math
import sys

# Config
WIDTH, HEIGHT = 720, 1280
FPS = 60
DURATION = 25  # seconds
TOTAL_FRAMES = FPS * DURATION
BALL_RADIUS = 30

# Couleurs
BG_COLOR = (10, 10, 20)
BALL_COLOR = (240, 240, 255)

# Initialisation
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Charger un son doux
pygame.mixer.init()
pock_sound = pygame.mixer.Sound('pock.mp3')  # Remplace par ton fichier son
pock_sound.set_volume(0.3)
RAIN_SOUND = pygame.mixer.Sound("rain_loop.mp3")  # Bruit de pluie en boucle
RAIN_SOUND.play(loops=-1)

# Fonction trajectoire en boucle parfaite (modèle de Lissajous 2D modifié)
def lissajous(t, A, B, a, b, delta):
    x = WIDTH // 2 + A * math.sin(a * t + delta)
    y = HEIGHT // 2 + B * math.sin(b * t)
    return int(x), int(y)

# Pour éviter les sons multiples sur le même bord
last_hits = {'left': False, 'right': False, 'top': False, 'bottom': False}

def check_and_play_sound(x, y):
    hit = False
    margin = BALL_RADIUS + 2

    if x <= margin:
        if not last_hits['left']:
            pock_sound.play()
            last_hits['left'] = True
        hit = True
    else:
        last_hits['left'] = False

    if x >= WIDTH - margin:
        if not last_hits['right']:
            pock_sound.play()
            last_hits['right'] = True
        hit = True
    else:
        last_hits['right'] = False

    if y <= margin:
        if not last_hits['top']:
            pock_sound.play()
            last_hits['top'] = True
        hit = True
    else:
        last_hits['top'] = False

    if y >= HEIGHT - margin:
        if not last_hits['bottom']:
            pock_sound.play()
            last_hits['bottom'] = True
        hit = True
    else:
        last_hits['bottom'] = False

# Ajouter une liste pour les balles secondaires
secondary_balls = []
secondary_colors = [
    (255, 100, 100),  # Rouge clair
    (100, 255, 100),  # Vert clair
    (100, 100, 255),  # Bleu clair
    (255, 255, 100),  # Jaune clair
    (255, 100, 255),  # Magenta clair
    (100, 255, 255),  # Cyan clair
]

# Paramètres pour boucle parfaite
A = WIDTH // 2 - BALL_RADIUS - 10
B = HEIGHT // 2 - BALL_RADIUS - 10
a = 3 * math.pi * 2 / DURATION  # nombre de cycles horizontaux
b = 4 * math.pi * 2 / DURATION  # nombre de cycles verticaux
delta = math.pi / 2  # décalage de phase pour rendre la boucle élégante

frame = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Temps normalisé
    t = (frame % TOTAL_FRAMES) / FPS

    # Position de la balle principale
    x, y = lissajous(t, A, B, a, b, delta)
    check_and_play_sound(x, y)

    # Ajouter une nouvelle balle toutes les secondes
    if frame % FPS == 0:
        color = secondary_colors[len(secondary_balls) % len(secondary_colors)]
        secondary_balls.append({'color': color, 'offset': frame / FPS})
        pock_sound.play()  # Jouer le son à chaque apparition d'une nouvelle balle

    # Affichage
    screen.fill(BG_COLOR)

    # Dessiner la balle principale
    pygame.draw.circle(screen, BALL_COLOR, (x, y), BALL_RADIUS)

    # Dessiner les balles secondaires
    for ball in secondary_balls:
        t_offset = t - ball['offset']  # Décalage temporel pour suivre la balle principale
        if t_offset >= 0:  # Ne dessiner que si la balle est active
            sx, sy = lissajous(t_offset, A, B, a, b, delta)
            pygame.draw.circle(screen, ball['color'], (sx, sy), BALL_RADIUS)

    pygame.display.flip()
    clock.tick(FPS)
    frame += 1
