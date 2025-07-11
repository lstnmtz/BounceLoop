# -*- coding: utf-8 -*-
import pygame
import sys
import math
import random

# Choix de la version : "easy", "medium" ou "hard"
GAME_VERSION = "hard"  # <-- change ici pour "easy", "medium" ou "hard"

if GAME_VERSION == "easy":
    BALL_DIAMETER = 15
    MAX_TIME = 30.0
    VERSION_TEXT = ("version easy", (0, 200, 0))  # vert
elif GAME_VERSION == "medium":
    BALL_DIAMETER = 7
    MAX_TIME = 50.0
    VERSION_TEXT = ("version medium", (255, 128, 0))  # orange
else:
    BALL_DIAMETER = 2
    MAX_TIME = 70.0
    VERSION_TEXT = ("version hard", (255, 0, 0))  # rouge

# ----------------------------------------------
WINDOW_WIDTH = 720            # Largeur de la fenêtre
WINDOW_HEIGHT = 1280          # Hauteur de la fenêtre
ARC_RADIUS = 300              # Rayon de l'arc de cercle (en pixels)
ARC_OPEN_ANGLE = 270          # Ouverture de l'arc (en degrés, portion manquante de 360°)
ARC_ROTATION_SPEED = 50.0     # Vitesse de rotation de l'arc (degrés par seconde, sens horaire)
BALL_SPEED = 200.0             # Vitesse de la balle (pixels par seconde)
IMAGE_PATH = "images/paul.png"   # Chemin vers l'image de fond
SOUND_PATH = "sons/bounce.wav"    # Chemin vers le son joué au rebond
# ----------------------------------------------

# Initialisation de Pygame et de la fenêtre
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Arc tournant et balles")
clock = pygame.time.Clock()

# Chargement de l'image de fond (mise à l'échelle de la fenêtre)
try:
    background_image = pygame.image.load(IMAGE_PATH).convert()
except pygame.error:
    print(f"Impossible de charger l'image {IMAGE_PATH}. Fond noir utilisé.")
    background_image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    background_image.fill((0,0,0))
background_image = pygame.transform.scale(background_image, (2 * ARC_RADIUS, 2 * ARC_RADIUS))

# Chargement du son de rebond
try:
    bounce_sound = pygame.mixer.Sound(SOUND_PATH)
except pygame.error:
    print(f"Impossible de charger le son {SOUND_PATH}. Aucun son ne sera joué.")
    bounce_sound = None

# Classe représentant une balle dans l'arc
class Balle:
    def __init__(self, x, y, vx, vy):
        self.x = x      # Position x
        self.y = y      # Position y
        self.vx = vx    # Vitesse en x
        self.vy = vy    # Vitesse en y
        self.escaped = False  # Indique si la balle a quitté l'arc (ne rebondit plus)

# Centre de rotation (centre de la fenêtre)
CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2

# Création de la première balle au centre avec direction aléatoire
start_angle = random.uniform(0, 2*math.pi)
vx_init = math.cos(start_angle) * BALL_SPEED
vy_init = math.sin(start_angle) * BALL_SPEED
balls = [Balle(CENTER_X, CENTER_Y, vx_init, vy_init)]
ball_count = 1  # Compte du nombre de balles existantes (pour l'effet de révélation)

# Création de la surface contenant un arc blanc statique (270° CCW)
arc_surface = pygame.Surface((2*ARC_RADIUS, 2*ARC_RADIUS), pygame.SRCALPHA)
arc_rect = pygame.Rect(0, 0, 2*ARC_RADIUS, 2*ARC_RADIUS)
# Dessin de l'arc blanc (épaisseur 3px) de 0 à 270° CCW
pygame.draw.arc(arc_surface, (255, 255, 255), arc_rect,
                0, 3 * math.pi / 2, 3)

# Surface noire pour l'effet d'opacité (cache de l'image de fond)
overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
overlay.fill((0, 0, 0))
overlay_alpha = 255  # Opacité initiale (image cachée)

# Variables de temps
start_ticks = pygame.time.get_ticks()
arc_angle_offset = 0.0  # Angle de départ

def is_in_opening(angle_base, opening_start, opening_size):
    """angle_base en degrés, opening_start en degrés, opening_size en degrés"""
    end = (opening_start + opening_size) % 360
    if opening_size >= 360:
        return True
    if opening_start < end:
        return opening_start <= angle_base < end
    else:
        return angle_base >= opening_start or angle_base < end

# --- Affichage de l'image uniquement à travers la traînée des balles ---

# 1. Initialiser le masque global UNE SEULE FOIS avant la boucle principale :
mask_surface = pygame.Surface((2 * ARC_RADIUS, 2 * ARC_RADIUS), pygame.SRCALPHA)
mask_surface.fill((0, 0, 0, 0))

# Boucle principale
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Temps écoulé depuis la dernière itération (secondes)
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000.0
    if elapsed_time >= MAX_TIME:
        running = False  # Arrêt de la boucle après MAX_TIME secondes
    
    # Gestion des événements (fermeture de la fenêtre)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Mise à jour de la rotation de l'arc (sens horaire)
    arc_angle_offset = (arc_angle_offset + ARC_ROTATION_SPEED * dt) % 360.0
    
    # Calcul de l'opacité en fonction du nombre de balles
    # Plus il y a de balles, plus l'image est visible (alpha diminue)
    overlay_alpha = max(0, 255 - ball_count * 10)
    overlay.set_alpha(overlay_alpha)
    
    # Dessin du fond (noir), de l'image et du calque d'opacité
    screen.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Dessin de l'arc tournant en blanc
    rotated_arc = pygame.transform.rotate(arc_surface, -(arc_angle_offset + ARC_OPEN_ANGLE))
    arc_pos = rotated_arc.get_rect(center=(CENTER_X, CENTER_Y))
    screen.blit(rotated_arc, arc_pos.topleft)
    
    # Mise à jour et dessin des balles
    for ball in balls:
        # Déplacement de la balle
        ball.x += ball.vx * dt
        ball.y += ball.vy * dt
        # Dessin de la balle (cercle blanc)
        pygame.draw.circle(screen, (255, 255, 255),
                           (int(ball.x), int(ball.y)), BALL_DIAMETER // 2)
        
        # Si la balle n'est pas encore sortie, on gère collisions/rebond
        if not ball.escaped:
            dx = ball.x - CENTER_X
            dy = ball.y - CENTER_Y
            dist = math.hypot(dx, dy)
            # Si la balle atteint ou dépasse l'arc (collision possible)
            if dist + BALL_DIAMETER/2 >= ARC_RADIUS:
                # Calcul de l'angle CCW (en degrés) depuis l'axe x positif
                angle = math.degrees(math.atan2(dy, dx))
                if angle < 0:
                    angle += 360
                # Correction ici :
                angle_base = (angle - arc_angle_offset) % 360
                opening_start = ARC_OPEN_ANGLE
                opening_size = 360 - ARC_OPEN_ANGLE
                if is_in_opening(angle_base, opening_start, opening_size):
                    # Sortie par l'ouverture : création de DEUX nouvelles balles au centre
                    for _ in range(2):
                        new_angle = random.uniform(0, 2*math.pi)
                        vx_new = math.cos(new_angle) * BALL_SPEED
                        vy_new = math.sin(new_angle) * BALL_SPEED
                        balls.append(Balle(CENTER_X, CENTER_Y, vx_new, vy_new))
                        ball_count += 1
                    ball.escaped = True  # Marquer la balle comme "sortie"
                else:
                    # Rebond sur l'arc : réflexion de la vitesse
                    # Normale du cercle (vecteur radial)
                    nx = dx / dist
                    ny = dy / dist
                    # Calcul du produit scalaire
                    dot = ball.vx * nx + ball.vy * ny
                    # Réflexion : v' = v - 2*(v·n)*n
                    ball.vx = ball.vx - 2 * dot * nx
                    ball.vy = ball.vy - 2 * dot * ny

                    # --- Ajout d'un rebond aléatoire ---
                    angle_variation = random.uniform(-math.pi/12, math.pi/12)  # +/- 15 degrés
                    speed = math.hypot(ball.vx, ball.vy)
                    current_angle = math.atan2(ball.vy, ball.vx)
                    new_angle = current_angle + angle_variation
                    ball.vx = speed * math.cos(new_angle)
                    ball.vy = speed * math.sin(new_angle)
                    # --- Fin rebond aléatoire ---

                    # Repositionnement de la balle juste à l'intérieur de l'arc
                    ball.x = CENTER_X + nx * (ARC_RADIUS - BALL_DIAMETER/2)
                    ball.y = CENTER_Y + ny * (ARC_RADIUS - BALL_DIAMETER/2)
                    # Jouer le son de rebond si disponible
                    if bounce_sound:
                        bounce_sound.play()
    
    # Pour chaque balle, dessiner un cercle blanc (opaque) sur le masque
    for ball in balls:
        # Position relative dans le cercle
        rel_x = int(ball.x - CENTER_X + ARC_RADIUS)
        rel_y = int(ball.y - CENTER_Y + ARC_RADIUS)
        pygame.draw.circle(mask_surface, (255, 255, 255, 255), (rel_x, rel_y), BALL_DIAMETER // 2)
    # Appliquer le masque sur l'image de fond (qui fait la taille du cercle)
    img_visible = background_image.copy()
    img_visible.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    # Afficher l'image masquée, centrée sur le cercle
    screen.blit(img_visible, (CENTER_X - ARC_RADIUS, CENTER_Y - ARC_RADIUS))

    # Dessiner le contour du cercle/arc par-dessus l'image
    rotated_arc = pygame.transform.rotate(arc_surface, -(arc_angle_offset + ARC_OPEN_ANGLE))
    arc_pos = rotated_arc.get_rect(center=(CENTER_X, CENTER_Y))
    screen.blit(rotated_arc, arc_pos.topleft)

    # Afficher la balle par-dessus la traînée (toujours en coordonnées écran)
    for ball in balls:
        pygame.draw.circle(screen, (255, 255, 255), (int(ball.x), int(ball.y)), BALL_DIAMETER // 2)

    # Afficher le texte principal centré au-dessus du cercle (plus haut)
    font = pygame.font.Font(None, 48)
    text = "Guess the image and write your time"
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(CENTER_X, CENTER_Y - ARC_RADIUS - 60))
    screen.blit(text_surface, text_rect)

    # Afficher la version (couleur selon la difficulté)
    font_small = pygame.font.Font(None, 32)
    version_text, version_color = VERSION_TEXT
    version_surface = font_small.render(version_text, True, version_color)
    version_rect = version_surface.get_rect(center=(CENTER_X, CENTER_Y - ARC_RADIUS - 30))
    screen.blit(version_surface, version_rect)

    # Afficher le timer en bas du cercle, centré
    font_timer = pygame.font.Font(None, 48)
    timer_text = f"Time : {int(elapsed_time)}"
    timer_surface = font_timer.render(timer_text, True, (255, 255, 255))
    timer_rect = timer_surface.get_rect(center=(CENTER_X, CENTER_Y + ARC_RADIUS + 30))
    screen.blit(timer_surface, timer_rect)

    # Gestion des collisions entre balles
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            b1 = balls[i]
            b2 = balls[j]
            if b1.escaped or b2.escaped:
                continue  # On ignore les balles déjà sorties
            dx = b2.x - b1.x
            dy = b2.y - b1.y
            dist = math.hypot(dx, dy)
            min_dist = BALL_DIAMETER
            if dist < min_dist and dist > 0:
                # Calcul du recouvrement
                overlap = 0.5 * (min_dist - dist)
                # Repousser les balles pour éviter l'enfoncement
                nx = dx / dist
                ny = dy / dist
                b1.x -= overlap * nx
                b1.y -= overlap * ny
                b2.x += overlap * nx
                b2.y += overlap * ny
                # Échange des vitesses (rebond élastique simplifié)
                v1x, v1y = b1.vx, b1.vy
                v2x, v2y = b2.vx, b2.vy
                b1.vx, b1.vy = v2x, v2y
                b2.vx, b2.vy = v1x, v1y

    # Mise à jour de l'affichage
    pygame.display.flip()

pygame.quit()
sys.exit()
