import pygame
import random
import sys

pygame.init()

# -------------------------
# WINDOW SETUP
# -------------------------
WIDTH = 1400
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chairlift Control System")

font = pygame.font.SysFont("consolas", 22)
bigfont = pygame.font.SysFont("consolas", 32)

clock = pygame.time.Clock()

# -------------------------
# STATUS VARIABLES
# -------------------------

# 0: Default
# 1: Running
# 2: Ready
# 3: Emergency Stop
# 4: Service Stop
# 5: Slowed 1
# 6: Slowed 2
# 7: Awaiting Reset
# 9: ERROR

mainstatus = 0
reset = 0
speed = 100
direction = 1  # 1 forward, 2 backward
go = 0

startcodes = (808081, 909187, 676754, 515158, 494941)
setgocode = random.choice(startcodes)

input_text = ""
boot_phase = True
message = "System just booted. Not Ready."

# -------------------------
# COLORS
# -------------------------
WHITE = (240, 240, 240)
BLACK = (20, 20, 20)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (230, 180, 0)
GRAY = (70, 70, 70)
BLUE = (50, 120, 220)

# -------------------------
# BUTTON CLASS
# -------------------------
class Button:
    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        label = font.render(self.text, True, WHITE)
        screen.blit(label, (self.rect.x + 10, self.rect.y + 10))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


# -------------------------
# BUTTONS
# -------------------------
buttons = [
    Button(50, 400, 120, 50, "START", GREEN),
    Button(200, 400, 120, 50, "EMERGENCY", RED),
    Button(350, 400, 120, 50, "SERVICE", YELLOW),
    Button(500, 400, 120, 50, "SLOW 1", BLUE),
    Button(650, 400, 120, 50, "SLOW 2", BLUE),
    Button(50, 470, 120, 50, "RESET", GRAY),
    Button(200, 470, 120, 50, "INVERT", GRAY),
    Button(350, 470, 120, 50, "ERR RESET", RED),
    Button(500, 470, 120, 50, "QUIT", BLACK),
]

# -------------------------
# STATUS TEXT
# -------------------------
def update_status():
    global message
    if mainstatus == 0:
        message = "Default - Booting"
    elif mainstatus == 1:
        message = "Running"
    elif mainstatus == 2:
        message = "Ready"
    elif mainstatus == 3:
        message = "Emergency Stop"
    elif mainstatus == 4:
        message = "Service Stop"
    elif mainstatus == 5:
        message = "Slowed 1"
    elif mainstatus == 6:
        message = "Slowed 2"
    elif mainstatus == 7:
        message = "Awaiting Reset"
    elif mainstatus == 9:
        message = "ERROR"


# -------------------------
# MAIN LOOP
# -------------------------
running = True

while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # -------------------------
        # BOOT PHASE INPUT
        # -------------------------
        if boot_phase:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text == str(setgocode):
                        go = 1
                        mainstatus = 2
                        reset = 1
                        boot_phase = False
                    else:
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        # -------------------------
        # BUTTON CLICK HANDLING
        # -------------------------
        if event.type == pygame.MOUSEBUTTONDOWN and not boot_phase:
            pos = pygame.mouse.get_pos()

            if buttons[0].clicked(pos):  # START
                if mainstatus == 2 and reset == 1:
                    mainstatus = 1
                elif mainstatus in (5, 6):
                    speed = 100
                    mainstatus = 1

            elif buttons[1].clicked(pos):  # EMERGENCY
                mainstatus = 3
                reset = 0

            elif buttons[2].clicked(pos):  # SERVICE
                mainstatus = 4
                reset = 0

            elif buttons[3].clicked(pos):  # SLOW 1
                mainstatus = 5
                speed = 75

            elif buttons[4].clicked(pos):  # SLOW 2
                mainstatus = 6
                speed = 50

            elif buttons[5].clicked(pos):  # RESET
                if mainstatus != 3:
                    mainstatus = 2
                    reset = 1

            elif buttons[6].clicked(pos):  # INVERT
                if mainstatus == 2:
                    direction = 2 if direction == 1 else 1
                elif mainstatus == 1:
                    mainstatus = 9

            elif buttons[7].clicked(pos):  # ERROR RESET
                if mainstatus == 9:
                    mainstatus = 2
                    reset = 1

            elif buttons[8].clicked(pos):  # QUIT
                running = False

    # -------------------------
    # DRAW BOOT SCREEN
    # -------------------------
    if boot_phase:
        title = bigfont.render("Chairlift Boot System", True, WHITE)
        screen.blit(title, (WIDTH//2 - 180, 150))

        code_text = font.render(
            f"Enter Code {setgocode} to Start:", True, WHITE
        )
        screen.blit(code_text, (WIDTH//2 - 200, 250))

        input_surface = font.render(input_text, True, GREEN)
        screen.blit(input_surface, (WIDTH//2 - 100, 300))

    else:
        update_status()

        # Title
        title = bigfont.render("Chairlift Control Panel", True, WHITE)
        screen.blit(title, (WIDTH//2 - 200, 30))

        # Status
        status_text = font.render(f"STATUS: {message}", True, WHITE)
        screen.blit(status_text, (50, 120))

        speed_text = font.render(f"SPEED: {speed}%", True, WHITE)
        screen.blit(speed_text, (50, 160))

        dir_text = font.render(
            f"DIRECTION: {'Forward' if direction == 1 else 'Backward'}",
            True,
            WHITE,
        )
        screen.blit(dir_text, (50, 200))

        # Draw Buttons
        for b in buttons:
            b.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

