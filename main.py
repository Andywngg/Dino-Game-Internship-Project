"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
Additional author: Andy Wang
Commit hash: cfcac38ebf8d0da7475a6662af24faee47ab38d2

Features:
- Character select screen (Tralalero Tralala and Tung Tung Tung Sahur)
- Lives system with 3 hearts
- Double jump
- High score leaderboard saved to scores.txt
"""

import pygame
from random import randint, choice


def display_score(start_time):
    """Calculate and draw the score based on time survived."""
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = game_font.render("Score: " + str(current_time), False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    """Move all obstacles left and remove ones that go off screen."""
    if not obstacle_list:
        return []
    updated = []
    for obstacle_surf, obstacle_rect in obstacle_list:
        obstacle_rect.x -= 5
        screen.blit(obstacle_surf, obstacle_rect)
        if obstacle_rect.right > 0:
            updated.append((obstacle_surf, obstacle_rect))
    return updated


def collisions(player, obstacles):
    """Return False if player hits an obstacle."""
    for _, obstacle_rect in obstacles:
        if player.colliderect(obstacle_rect):
            return False
    return True


def spawn_obstacle():
    """Spawn a new obstacle at the right side of the screen."""
    if obstacle_rect_list:
        last_rect = obstacle_rect_list[-1][1]
        spawn_x = max(randint(900, 1100), last_rect.right + 260)
    else:
        spawn_x = randint(900, 1100)

    if randint(0, 2):
        obstacle_rect_list.append(
            (egg_surf, egg_surf.get_rect(bottomleft=(spawn_x, GROUND_Y)))
        )
    else:
        obstacle_rect_list.append(
            (bc_surf, bc_surf.get_rect(bottomleft=(spawn_x, 210)))
        )


def player_animation():
    """Switch between walk and jump frames depending on if player is airborne."""
    global player_surf, player_index

    if player_rect.bottom < GROUND_Y:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


def load_scores():
    """Load saved high scores from scores.txt."""
    scores = []
    try:
        f = open("scores.txt", "r")
        for line in f:
            if line.strip().isdigit():
                scores.append(int(line.strip()))
        f.close()
    except:
        pass
    return scores


def save_scores(scores):
    """Save top 10 scores to scores.txt."""
    scores.sort(reverse=True)
    f = open("scores.txt", "w")
    for s in scores[:10]:
        f.write(str(s) + "\n")
    f.close()


def draw_high_scores(scores):
    """Draw the high scores screen."""
    screen.fill((20, 20, 40))
    title = game_font.render("HIGH SCORES", False, (255, 215, 0))
    screen.blit(title, title.get_rect(center=(400, 40)))
    if not scores:
        msg = game_font.render("No scores yet!", False, (200, 200, 200))
        screen.blit(msg, msg.get_rect(center=(400, 200)))
    else:
        for i in range(len(sorted(scores, reverse=True)[:10])):
            s = sorted(scores, reverse=True)[i]
            color = (255, 215, 0) if i == 0 else (200, 200, 200)
            entry = game_font.render(str(i + 1) + ". " + str(s), False, color)
            screen.blit(entry, entry.get_rect(center=(400, 100 + i * 30)))
    hint = game_font.render("SPACE to return", False, (150, 150, 150))
    screen.blit(hint, hint.get_rect(center=(400, 375)))


def draw_char_select():
    """Draw the character selection screen."""
    screen.fill((25, 18, 45))
    title = game_font.render("Choose Your Character", False, (255, 215, 0))
    screen.blit(title, title.get_rect(center=(400, 40)))
    names = ["Tralalero", "T.T.T. Sahur"]
    descs = ["Floaty jump", "Heavy, strong jump"]
    for i in range(2):
        cx = 200 + i * 400
        if i == selected_char:
            pygame.draw.rect(screen, (80, 60, 120), (cx - 110, 80, 220, 240), border_radius=14)
            pygame.draw.rect(screen, (200, 160, 255), (cx - 110, 80, 220, 240), 3, border_radius=14)
        else:
            pygame.draw.rect(screen, (45, 35, 65), (cx - 110, 80, 220, 240), border_radius=14)
    hint = game_font.render("LEFT/RIGHT to choose   SPACE to start", False, (220, 220, 220))
    screen.blit(hint, hint.get_rect(center=(400, 370)))


def reset_game():
    """Reset all game variables for a new run."""
    global players_gravity_speed, obstacle_rect_list, score_start_time
    global lives, score, jumps_used

    players_gravity_speed = 0
    obstacle_rect_list = []
    score_start_time = pygame.time.get_ticks()
    lives = 3
    score = 0
    jumps_used = 0
    player_rect.bottomleft = (25, GROUND_Y)


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Brainrot Run")
clock = pygame.time.Clock()

game_font = pygame.font.Font(pygame.font.get_default_font(), 30)

GROUND_Y = 300
MAX_JUMPS = 2
JUMP_POWER = [-20, -23]
GRAVITY = [1, 1.5]

# Load assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()

# Tralalero sprites
t_w1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
t_w2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
t_jump = pygame.image.load("graphics/player/player_jump.png").convert_alpha()

# Tung Tung Tung sprites
tt_w1 = pygame.image.load("graphics/tripleT/tripleT_walk1.png").convert_alpha()
tt_w2 = pygame.image.load("graphics/tripleT/tripleT_walk2.png").convert_alpha()
tt_jump = pygame.image.load("graphics/tripleT/tripleT_jump.png").convert_alpha()

char_walk = [[t_w1, t_w2], [tt_w1, tt_w2]]
char_jump = [t_jump, tt_jump]

# Standing sprite for menu
player_stand = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# Enemies
egg_surf = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
bc_surf = pygame.image.load("graphics/bombardino/bc.png").convert_alpha()

# Heart icon for lives
heart_surf = pygame.image.load("graphics/utils/life.png").convert_alpha()
heart_surf = pygame.transform.scale(heart_surf, (28, 28))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)

scores = load_scores()
game_state = "menu"
selected_char = 0

players_gravity_speed = 0
obstacle_rect_list = []
score_start_time = 0
score = 0
lives = 3
jumps_used = 0

player_walk = char_walk[selected_char]
player_jump = char_jump[selected_char]
player_surf = player_walk[0]
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
player_index = 0

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "char_select"
                elif event.key == pygame.K_h:
                    game_state = "high_scores"

        elif game_state == "char_select":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_char = (selected_char - 1) % 2
                elif event.key == pygame.K_RIGHT:
                    selected_char = (selected_char + 1) % 2
                elif event.key == pygame.K_SPACE:
                    player_walk = char_walk[selected_char]
                    player_jump = char_jump[selected_char]
                    reset_game()
                    game_state = "playing"

        elif game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and jumps_used < MAX_JUMPS:
                    players_gravity_speed = JUMP_POWER[selected_char]
                    jumps_used += 1
            if event.type == pygame.MOUSEBUTTONDOWN and jumps_used < MAX_JUMPS:
                players_gravity_speed = JUMP_POWER[selected_char]
                jumps_used += 1
            if event.type == obstacle_timer:
                spawn_obstacle()

        elif game_state == "game_over":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "char_select"

        elif game_state == "high_scores":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "menu"

    if game_state == "menu":
        screen.fill("white")
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))
        screen.blit(player_stand, player_stand_rect)
        title = game_font.render("Brainrot Run", False, (111, 196, 169))
        hint = game_font.render("SPACE to play   H for high scores", False, (111, 196, 169))
        screen.blit(title, title.get_rect(center=(400, 80)))
        screen.blit(hint, hint.get_rect(center=(400, 320)))

    elif game_state == "char_select":
        draw_char_select()

    elif game_state == "playing":
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))

        score = display_score(score_start_time)

        players_gravity_speed += GRAVITY[selected_char]
        player_rect.y += int(players_gravity_speed)
        if player_rect.bottom >= GROUND_Y:
            player_rect.bottom = GROUND_Y
            jumps_used = 0

        player_animation()
        screen.blit(player_surf, player_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Draw hearts for lives
        for i in range(lives):
            screen.blit(heart_surf, heart_surf.get_rect(center=(770 - i * 36, 30)))

        if not collisions(player_rect, obstacle_rect_list):
            lives -= 1
            obstacle_rect_list = []
            player_rect.bottomleft = (25, GROUND_Y)
            players_gravity_speed = 0
            jumps_used = 0
            if lives <= 0:
                scores.append(score)
                save_scores(scores)
                game_state = "game_over"

    elif game_state == "game_over":
        screen.fill("black")
        over = game_font.render("Game Over! Score: " + str(score), False, "white")
        hint = game_font.render("SPACE to play again", False, "white")
        screen.blit(over, over.get_rect(center=(400, 180)))
        screen.blit(hint, hint.get_rect(center=(400, 240)))

    elif game_state == "high_scores":
        draw_high_scores(scores)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()