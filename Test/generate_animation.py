import pygame
import random
import math
import os

# ================== PARAMÈTRES GÉNÉRAUX =====================
WIDTH, HEIGHT = 720, 1280
FPS = 30
DURATION = 10
FRAMES = DURATION * FPS

# ================== DÉFI & PHRASE ============================
CHALLENGE_TEXT = "Can you find the ball that changes color?"

# ================== THÈMES DISPONIBLES =======================
THEMES = {
    "zen": {
        "background": (10, 10, 20),
        "glow_alpha": 25,
        "palette": [(100, 200, 255), (80, 180, 180), (120, 220, 200)],
        "speed": (1.0, 2.5),
        "count": 50,
        "radius": (30, 60),
    },
    "futuriste": {
        "background": (0, 0, 0),
        "glow_alpha": 60,
        "palette": [(0, 255, 255), (255, 0, 255), (0, 255, 100)],
        "speed": (2.5, 5.0),
        "count": 50,
        "radius": (20, 40),
    },
    "psychedelic": {
        "background": (0, 0, 0),
        "glow_alpha": 50,
        "palette": [lambda: (
            random.randint(100, 255),
            random.randint(50, 200),
            random.randint(100, 255)
        )],
        "speed": (2.0, 4.5),
        "count": 50,
        "radius": (25, 50),
    }
}

# ================== CLASSES ===============================

class Ball:
    def __init__(self, is_special=False):
        self.radius = random.randint(*theme["radius"])
        self.is_special = is_special
        self.pos = [
            random.uniform(self.radius, WIDTH - self.radius),
            random.uniform(self.radius, HEIGHT - self.radius)
        ]
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(*theme["speed"])
        self.velocity = [math.cos(angle) * speed, math.sin(angle) * speed]
        self.base_color = self.random_color()
        self.color = self.base_color

    def random_color(self):
        palette = theme["palette"]
        c = random.choice(palette)
        return c() if callable(c) else c

    def update(self, frame):
        # Rebond
        for i in [0, 1]:
            self.pos[i] += self.velocity[i]
            if self.pos[i] < self.radius or self.pos[i] > (WIDTH if i == 0 else HEIGHT) - self.radius:
                self.velocity[i] *= -1
        # Changement progressif pour la balle spéciale
        if self.is_special:
            r = int((math.sin(frame / 20.0) + 1) * 127)
            g = int((math.cos(frame / 25.0) + 1) * 127)
            b = int((math.sin(frame / 15.0 + 2) + 1) * 127)
            self.color = (r, g, b)

    def draw(self, surface):
        glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*self.color, theme["glow_alpha"]), self.pos, self.radius * 2)
        pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)
        surface.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

# ================ INITIALISATION ==========================
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial", 40, bold=True)

# Choix aléatoire de thème
theme_name = random.choice(list(THEMES.keys()))
theme = THEMES[theme_name]
print("🎨 Thème :", theme_name)

# Écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Création des balles
balls = [Ball() for _ in range(theme["count"] - 1)]
balls.append(Ball(is_special=True))
random.shuffle(balls)

# Création du dossier
folder = f"frames_{theme_name}_challenge"
os.makedirs(folder, exist_ok=True)

# ================ RENDU DES FRAMES ========================
for frame in range(FRAMES):
    screen.fill(theme["background"])
    for ball in balls:
        ball.update(frame)
        ball.draw(screen)

    # Texte challenge sur 2 lignes max
    def wrap_text(text, font, max_width):
        words = text.split()
        lines = []
        line = ""
        for word in words:
            test_line = f"{line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)
        return lines

    wrapped_lines = wrap_text(CHALLENGE_TEXT, font, WIDTH - 100)

    # Dessiner un rectangle de fond derrière le texte
    rect_width = WIDTH - 100
    rect_height = len(wrapped_lines) * 50 + 20  # Ajuster la hauteur en fonction du nombre de lignes
    rect_x = (WIDTH - rect_width) // 2
    rect_y = 100 - 10  # Ajuster pour inclure un peu de marge
    pygame.draw.rect(screen, (0, 0, 0, 200), (rect_x, rect_y, rect_width, rect_height))  # Fond noir semi-transparent

    # Dessiner le texte
    for i, line in enumerate(wrapped_lines[:2]):
        text_surface = font.render(line, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 100 + i * 50))
        screen.blit(text_surface, text_rect)

    pygame.image.save(screen, f"{folder}/frame_{frame:04d}.png")
    clock.tick(FPS)

pygame.quit()
print("✅ Animation avec défi et texte générée :", folder)
