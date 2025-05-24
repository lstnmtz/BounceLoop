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
BALL_IMAGE_PATH = "images/yes.jpg"  # Image de la balle
BALL_SIZE = 50
BALL_SPEED = 6

# Chargement de l'image de la balle
ball_image = pygame.image.load(BALL_IMAGE_PATH).convert_alpha()
ball_image = pygame.transform.scale(ball_image, (BALL_SIZE, BALL_SIZE))
ball_mask = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
pygame.draw.circle(ball_mask, (255, 255, 255, 255), (BALL_SIZE // 2, BALL_SIZE // 2), BALL_SIZE // 2)
ball_image.blit(ball_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

# Chargement des sons
SOUND_PATH_REBOUND_yes = "sons/yes.mp3"  # Son de rebond pour "yes.jpg"
SOUND_PATH_OPENING_yes = "sons/yes.mp3"  # Son d'ouverture pour "yes.jpg"
SOUND_PATH_REBOUND_no = "sons/no.mp3"  # Son de rebond pour "no.jpg"
SOUND_PATH_OPENING_no = "sons/no.mp3"  # Son d'ouverture pour "no.jpg"

# Fonction pour générer une nouvelle balle
def new_ball(image_path, speed, rebound_sound_path, opening_sound_path):
    angle = random.uniform(0, 2 * math.pi)
    ball_image = pygame.image.load(image_path).convert_alpha()
    ball_image = pygame.transform.scale(ball_image, (BALL_SIZE, BALL_SIZE))
    ball_mask = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(ball_mask, (255, 255, 255, 255), (BALL_SIZE // 2, BALL_SIZE // 2), BALL_SIZE // 2)
    ball_image.blit(ball_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return {
        "x": WIDTH // 2,
        "y": HEIGHT // 2,
        "vx": speed * math.cos(angle),
        "vy": speed * math.sin(angle),
        "image": ball_image,
        "image_path": image_path,  # Ajout du chemin de l'image
        "rebound_sound": pygame.mixer.Sound(rebound_sound_path),
        "opening_sound": pygame.mixer.Sound(opening_sound_path),
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
balls = [
    new_ball("images/yes.jpg", BALL_SPEED, SOUND_PATH_REBOUND_yes, SOUND_PATH_OPENING_yes),
    new_ball("images/no.jpg", BALL_SPEED, SOUND_PATH_REBOUND_no, SOUND_PATH_OPENING_no),
]

# Angle de rotation initial
rotation_angle = 0

# Initialisation du temps de départ
start_time = pygame.time.get_ticks()

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calcul du temps écoulé
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convertir en secondes

    # Vérifier si 57 secondes se sont écoulées
    if elapsed_time >= 57:
        # Calculer le gagnant
        if count_yes > count_no:
            winner_text = "YES wins!"
        elif count_no > count_yes:
            winner_text = "NO wins!"
        else:
            winner_text = "It's a tie!"

        # Afficher le message final
        screen.fill((0, 0, 0))  # Effacer l'écran
        font = pygame.font.Font(None, 100)
        winner_surface = font.render(winner_text, True, (255, 255, 255))
        winner_rect = winner_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(winner_surface, winner_rect)

        # Afficher les scores des deux familles
        yes_score_surface = font.render(f"YES: {count_yes}", True, (255, 255, 255))
        yes_score_rect = yes_score_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(yes_score_surface, yes_score_rect)

        no_score_surface = font.render(f"NO: {count_no}", True, (255, 255, 255))
        no_score_rect = no_score_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(no_score_surface, no_score_rect)

        # Afficher l'image du gagnant
        if count_yes > count_no:
            winner_image = pygame.image.load("images/yes.jpg").convert_alpha()
        elif count_no > count_yes:
            winner_image = pygame.image.load("images/no.jpg").convert_alpha()
        else:
            winner_image = None  # Pas d'image en cas d'égalité

        if winner_image:
            winner_image = pygame.transform.scale(winner_image, (200, 200))  # Redimensionner l'image
            winner_image_rect = winner_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
            screen.blit(winner_image, winner_image_rect)

        pygame.display.flip()

        # Attendre quelques secondes avant de quitter
        pygame.time.wait(5000)
        running = False
        break

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
                ball["rebound_sound"].play()
            else:
                # Sortie par l'ouverture : dédoublement
                ball["opening_sound"].play()  # Jouer le son pour l'ouverture
                if ball["image_path"] == "images/yes.jpg":
                    balls_to_add.append(new_ball("images/yes.jpg", BALL_SPEED, SOUND_PATH_REBOUND_yes, SOUND_PATH_OPENING_yes))
                    balls_to_add.append(new_ball("images/yes.jpg", BALL_SPEED, SOUND_PATH_REBOUND_yes, SOUND_PATH_OPENING_yes))
                elif ball["image_path"] == "images/no.jpg":
                    balls_to_add.append(new_ball("images/no.jpg", BALL_SPEED, SOUND_PATH_REBOUND_no, SOUND_PATH_OPENING_no))
                    balls_to_add.append(new_ball("images/no.jpg", BALL_SPEED, SOUND_PATH_REBOUND_no, SOUND_PATH_OPENING_no))
                balls.remove(ball)  # Supprimer la balle qui est sortie
        else:
            # Dessiner la balle
            screen.blit(ball["image"], (ball["x"] - BALL_SIZE // 2, ball["y"] - BALL_SIZE // 2))

    # Ajouter les nouvelles balles
    balls.extend(balls_to_add)

    # Affichage du texte avec un rectangle blanc derrière
    font = pygame.font.Font(None, 74)
    text_surface = font.render("Are you dumb?", True, (0, 0, 0))  # Texte en noir
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - CIRCLE_RADIUS - 50))

    # Dessiner un rectangle blanc derrière le texte
    pygame.draw.rect(screen, (255, 255, 255), text_rect.inflate(20, 10))  # Rectangle légèrement plus grand que le texte

    # Dessiner le texte par-dessus le rectangle
    screen.blit(text_surface, text_rect)

    # Compter les balles par famille
    count_yes = sum(1 for ball in balls if ball["image_path"] == "images/yes.jpg")  # Inversé avec "no.jpg"
    count_no = sum(1 for ball in balls if ball["image_path"] == "images/no.jpg")  # Inversé avec "yes.jpg"

    # Afficher les compteurs pour chaque famille
    font = pygame.font.Font(None, 50)

    # Compteur pour "yes.jpg"
    yes_image = pygame.image.load("images/yes.jpg").convert_alpha()
    yes_image = pygame.transform.scale(yes_image, (BALL_SIZE, BALL_SIZE))
    screen.blit(yes_image, (WIDTH // 2 - 150, HEIGHT // 2 + CIRCLE_RADIUS + 20))
    yes_counter = font.render(f"{count_yes}", True, (255, 255, 255))
    screen.blit(yes_counter, (WIDTH // 2 - 100, HEIGHT // 2 + CIRCLE_RADIUS + 30))

    # Compteur pour "no.jpg"
    no_image = pygame.image.load("images/no.jpg").convert_alpha()
    no_image = pygame.transform.scale(no_image, (BALL_SIZE, BALL_SIZE))
    screen.blit(no_image, (WIDTH // 2 + 50, HEIGHT // 2 + CIRCLE_RADIUS + 20))
    no_counter = font.render(f"{count_no}", True, (255, 255, 255))
    screen.blit(no_counter, (WIDTH // 2 + 100, HEIGHT // 2 + CIRCLE_RADIUS + 30))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
