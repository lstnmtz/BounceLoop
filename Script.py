import pygame
import sys
import random
import math

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 720, 1280
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Animation")

# Paramètres de l'animation
FPS = 60
clock = pygame.time.Clock()

# Paramètres du cercle
CIRCLE_RADIUS = WIDTH // 2 - 40
CIRCLE_THICKNESS = 10
OPENING_ANGLE = math.radians(45)  # Ouverture de 45 degrés
CIRCLE_SPEED = 360 / (FPS * 15)  # Vitesse de rotation pour une boucle parfaite

# Gravité appliquée à la balle
GRAVITY = 0.05

# Paramètres de la balle
BALL_IMAGE_PATH = "images/patapim.jpg"  # Image de la balle
BALL_SIZE = 50
BALL_SPEED = 6

# Chargement de l'image de la balle
ball_image = pygame.image.load(BALL_IMAGE_PATH).convert_alpha()
ball_image = pygame.transform.scale(ball_image, (BALL_SIZE, BALL_SIZE))
ball_mask = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
pygame.draw.circle(ball_mask, (255, 255, 255, 255), (BALL_SIZE // 2, BALL_SIZE // 2), BALL_SIZE // 2)
ball_image.blit(ball_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

# Chargement des sons
SOUND_PATH_REBOUND = "sons/brrr.mp3"  # Son pour les rebonds
SOUND_PATH_OPENING = "sons/patapim.mp3"  # Son pour l'ouverture
rebound_sound = pygame.mixer.Sound(SOUND_PATH_REBOUND)
opening_sound = pygame.mixer.Sound(SOUND_PATH_OPENING)

# Fonction pour générer une nouvelle balle
def new_ball():
    angle = random.uniform(0, 2 * math.pi)
    return {
        "x": WIDTH // 2,
        "y": HEIGHT // 2,
        "vx": BALL_SPEED * math.cos(angle),
        "vy": BALL_SPEED * math.sin(angle)
    }

# Fonction pour normaliser un angle entre 0 et 360 degrés
def normalize_angle(angle):
    return angle % 360

# Fonction pour vérifier si un angle est dans une plage
def is_angle_in_range(angle, start, end):
    angle = normalize_angle(angle)
    start = normalize_angle(start)
    end = normalize_angle(end)
    if start < end:
        return start <= angle <= end
    else:
        return angle >= start or angle <= end

# Initialisation des balles
balls = [new_ball()]

# Angle de rotation initial
rotation_angle = 0

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Calcul de l'angle de rotation
    rotation_angle = (rotation_angle + CIRCLE_SPEED) % 360

    # Dessin du cercle avec ouverture
    center = (WIDTH // 2, HEIGHT // 2)
    pygame.draw.circle(screen, (255, 255, 255), center, CIRCLE_RADIUS, CIRCLE_THICKNESS)

    # Calcul des coordonnées de l'ouverture
    opening_start_angle = rotation_angle
    opening_end_angle = rotation_angle + math.degrees(OPENING_ANGLE)

    opening_x1 = center[0] + CIRCLE_RADIUS * math.cos(math.radians(opening_start_angle))
    opening_y1 = center[1] + CIRCLE_RADIUS * math.sin(math.radians(opening_start_angle))
    opening_x2 = center[0] + CIRCLE_RADIUS * math.cos(math.radians(opening_end_angle))
    opening_y2 = center[1] + CIRCLE_RADIUS * math.sin(math.radians(opening_end_angle))
    
    pygame.draw.line(screen, (0, 0, 0), (opening_x1, opening_y1), (opening_x2, opening_y2), CIRCLE_THICKNESS + 5)

    # Mise à jour des balles
    balls_to_add = []
    for ball in balls:
        # Mise à jour de la balle avec gravité
        ball["vy"] += GRAVITY
        ball["x"] += ball["vx"]
        ball["y"] += ball["vy"]

        # Vérification des rebonds
        dx = ball["x"] - center[0]
        dy = ball["y"] - center[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance + BALL_SIZE // 2 >= CIRCLE_RADIUS - CIRCLE_THICKNESS:
            # Vérification si c'est l'ouverture
            angle_to_ball = math.degrees(math.atan2(dy, dx))
            if not is_angle_in_range(angle_to_ball, opening_start_angle, opening_end_angle):
                # Rebonds normaux
                normal_angle = math.atan2(dy, dx)
                normal_x = math.cos(normal_angle)
                normal_y = math.sin(normal_angle)

                dot = ball["vx"] * normal_x + ball["vy"] * normal_y
                ball["vx"] -= 2 * dot * normal_x
                ball["vy"] -= 2 * dot * normal_y

                # Jouer le son de rebond
                rebound_sound.play()
            else:
                # Sortie par l'ouverture : dédoublement
                opening_sound.play()  # Jouer le son pour l'ouverture
                balls_to_add.append(new_ball())  # Ajouter une nouvelle balle
                balls_to_add.append(new_ball())  # Ajouter une deuxième balle
                balls.remove(ball)  # Supprimer la balle qui est sortie
        else:
            # Dessiner la balle
            screen.blit(ball_image, (ball["x"] - BALL_SIZE // 2, ball["y"] - BALL_SIZE // 2))

    # Ajouter les nouvelles balles
    balls.extend(balls_to_add)

    # Affichage du texte
    font = pygame.font.Font(None, 74)
    text_surface = font.render("BRRR BRRR PATAPIM LALA", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - CIRCLE_RADIUS - 50))
    screen.blit(text_surface, text_rect)

    counter_surface = font.render(f"Balls: {len(balls)}", True, (255, 255, 255))
    counter_rect = counter_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + CIRCLE_RADIUS + 50))
    screen.blit(counter_surface, counter_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
