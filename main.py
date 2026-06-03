"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
Additional author: Andy Wang
Commit hash: cfcac38ebf8d0da7475a6662af24faee47ab38d2

Features I added:
- Character select (Tralalero Tralala and Tung Tung Tung Sahur)
- Lives system with 3 hearts
- Double jump
- High score leaderboard saved to scores.txt
- Coins you collect during the run, saved to coins.txt
- Shop to spend coins on boosts for your next run
- Scrolling biome backgrounds that change every 500 points
- Pause menu
"""

import pygame
from random import randint, choice
import math


def load_scores():
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
    scores.sort(reverse=True)
    f = open("scores.txt", "w")
    for s in scores[:10]:
        f.write(str(s) + "\n")
    f.close()


def load_coins():
    try:
        f = open("coins.txt", "r")
        val = f.read().strip()
        f.close()
        if val.isdigit():
            return int(val)
    except:
        pass
    return 0


def save_coins(amount):
    f = open("coins.txt", "w")
    f.write(str(amount))
    f.close()


def load_boost():
    try:
        f = open("shop.txt", "r")
        val = f.read().strip()
        f.close()
        return val if val else "none"
    except:
        return "none"


def save_boost(name):
    f = open("shop.txt", "w")
    f.write(name)
    f.close()


def display_score(score):
    """Draw score at top of screen."""
    score_surf = game_font.render("Score: " + str(score), False, (255, 255, 255))
    screen.blit(score_surf, score_surf.get_rect(center=(400, 30)))


def spawn_obstacle():
    if obstacle_list:
        last_rect = obstacle_list[-1][1]
        x = max(randint(900, 1100), last_rect.right + 260)
    else:
        x = randint(900, 1100)

    if randint(0, 2):
        rect = bbp_surf.get_rect(bottomleft=(x, GROUND_Y))
        obstacle_list.append((bbp_surf, rect))
    else:
        rect = bombardino_surf.get_rect(bottomleft=(x, 300))
        obstacle_list.append((bombardino_surf, rect))


def move_obstacles():
    global obstacle_list
    updated = []
    for surf, rect in obstacle_list:
        rect.x -= game_speed
        screen.blit(surf, rect)
        if rect.right > 0:
            updated.append((surf, rect))
    obstacle_list = updated


def check_collisions():
    for surf, rect in obstacle_list:
        if player_rect.colliderect(rect):
            return False
    return True


def spawn_coins():
    """Spawn a row of coins for the player to collect."""
    x = randint(900, 1100)
    y = randint(270, 350)
    for i in range(randint(5, 8)):
        coin_list.append(pygame.Rect(x + i * 32, y, 22, 22))


def move_and_collect_coins():
    global coin_list, coins_run, total_coins
    updated = []
    for rect in coin_list:
        rect.x -= game_speed
        screen.blit(coin_surf, rect)
        if player_rect.colliderect(rect):
            coins_run += 1
            total_coins += 1
        elif rect.right > 0:
            updated.append(rect)
    coin_list = updated


def player_animation():
    global player_surf, player_index
    if player_rect.bottom < GROUND_Y:
        player_surf = char_jump[selected_char]
    else:
        player_index += 0.1
        if player_index >= 2:
            player_index = 0
        player_surf = char_walk[selected_char][int(player_index)]


def reset_game():
    global gravity_speed, obstacle_list, coin_list, score_acc
    global lives, score, jumps_used, coins_run, game_speed, bg_offset

    gravity_speed = 0
    obstacle_list = []
    coin_list = []
    score_acc = 0.0
    lives = 3
    score = 0
    jumps_used = 0
    coins_run = 0
    game_speed = 5
    bg_offset = 0
    player_rect.bottomleft = (25, GROUND_Y)

    boost = load_boost()
    if boost == "extra_life":
        lives = 4
    save_boost("none")


def handle_death():
    global lives, obstacle_list, coin_list, game_state, total_coins, jumps_used, gravity_speed

    lives -= 1
    obstacle_list = []
    coin_list = []
    player_rect.bottomleft = (25, GROUND_Y)
    gravity_speed = 0
    jumps_used = 0

    if lives <= 0:
        scores.append(score)
        save_scores(scores)
        total_coins += coins_run
        save_coins(total_coins)
        game_state = "game_over"


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Brainrot Run")
clock = pygame.time.Clock()

game_font = pygame.font.Font(pygame.font.get_default_font(), 28)
small_font = pygame.font.Font(pygame.font.get_default_font(), 20)
tiny_font = pygame.font.Font(pygame.font.get_default_font(), 13)

GROUND_Y = 380
MAX_JUMPS = 2
JUMP_POWER = [-20, -23]
GRAVITY = [1.0, 1.5]

# Backgrounds - city, desert, mountain, jungle, underwater from itch.io packs
# The Pixel Nook: https://the-pixel-nook.itch.io/parallax-backgrounds-demo
# ansimuz: https://ansimuz.itch.io/underwater-fantasy-pixel-art-environment
# License: Creative Commons Attribution v4.0 International
BG_FILES = ["city_clean.gif", "forest1.png", "desert.gif",
            "mountain.gif", "jungle.gif", "underwater.png", "city_dirty.gif", "forest2.png"]
backgrounds = []
for name in BG_FILES:
    try:
        img = pygame.image.load("graphics/level/" + name).convert()
        backgrounds.append(pygame.transform.scale(img, (800, 400)))
    except:
        surf = pygame.Surface((800, 400))
        surf.fill((30, 20, 50))
        backgrounds.append(surf)

# Player sprites
t_w1 = pygame.transform.scale(pygame.image.load("graphics/tralalero/tralalero_walk1.png").convert_alpha(), (60, 64))
t_w2 = pygame.transform.scale(pygame.image.load("graphics/tralalero/tralalero_walk2.png").convert_alpha(), (60, 64))
t_jump = pygame.transform.scale(pygame.image.load("graphics/tralalero/tralalero_jump.png").convert_alpha(), (60, 64))
t_base = pygame.transform.scale(pygame.image.load("graphics/tralalero/tralalero_base.png").convert_alpha(), (110, 110))

tt_w1 = pygame.transform.scale(pygame.image.load("graphics/tripleT/tripleT_walk1.png").convert_alpha(), (60, 64))
tt_w2 = pygame.transform.scale(pygame.image.load("graphics/tripleT/tripleT_walk2.png").convert_alpha(), (60, 64))
tt_jump = pygame.transform.scale(pygame.image.load("graphics/tripleT/tripleT_jump.png").convert_alpha(), (60, 64))
tt_base = pygame.transform.scale(pygame.image.load("graphics/tripleT/tripleT_base.png").convert_alpha(), (110, 110))

char_walk = [[t_w1, t_w2], [tt_w1, tt_w2]]
char_jump = [t_jump, tt_jump]
base_surfs = [t_base, tt_base]

# Enemies
bbp_surf = pygame.transform.scale(pygame.image.load("graphics/bbp/bbp.png").convert_alpha(), (52, 52))
bombardino_surf = pygame.transform.scale(pygame.image.load("graphics/bombardino/bombardino.png").convert_alpha(), (56, 48))

# UI
heart_surf = pygame.transform.scale(pygame.image.load("graphics/utils/life.png").convert_alpha(), (28, 28))
coin_surf = pygame.transform.scale(pygame.image.load("graphics/utils/coin.png").convert_alpha(), (22, 22))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
coin_timer = pygame.USEREVENT + 2
pygame.time.set_timer(coin_timer, 4000)

scores = load_scores()
total_coins = load_coins()
game_state = "menu"
selected_char = 0

gravity_speed = 0
obstacle_list = []
coin_list = []
score = 0
score_acc = 0.0
game_speed = 5
lives = 3
jumps_used = 0
coins_run = 0
bg_offset = 0

player_surf = char_walk[0][0]
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
                elif event.key == pygame.K_s:
                    game_state = "shop"

        elif game_state == "char_select":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_char = (selected_char - 1) % 2
                elif event.key == pygame.K_RIGHT:
                    selected_char = (selected_char + 1) % 2
                elif event.key == pygame.K_SPACE:
                    reset_game()
                    game_state = "playing"

        elif game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and jumps_used < MAX_JUMPS:
                    gravity_speed = JUMP_POWER[selected_char]
                    jumps_used += 1
                elif event.key == pygame.K_p:
                    game_state = "paused"
            if event.type == pygame.MOUSEBUTTONDOWN and jumps_used < MAX_JUMPS:
                gravity_speed = JUMP_POWER[selected_char]
                jumps_used += 1
            if event.type == obstacle_timer:
                spawn_obstacle()
            if event.type == coin_timer:
                spawn_coins()

        elif game_state == "paused":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_state = "playing"
                elif event.key == pygame.K_q:
                    game_state = "menu"

        elif game_state == "game_over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "char_select"
                elif event.key == pygame.K_m:
                    game_state = "menu"

        elif game_state == "high_scores":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "menu"

        elif game_state == "shop":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "menu"
                if event.key == pygame.K_1 and total_coins >= 25 and load_boost() != "extra_life":
                    total_coins -= 25
                    save_coins(total_coins)
                    save_boost("extra_life")
                elif event.key == pygame.K_2 and total_coins >= 50 and load_boost() != "shield":
                    total_coins -= 50
                    save_coins(total_coins)
                    save_boost("shield")

    if game_state == "menu":
        screen.fill((20, 12, 40))
        screen.blit(base_surfs[selected_char], base_surfs[selected_char].get_rect(center=(400, 200)))
        screen.blit(game_font.render("BRAINROT RUN", False, (255, 215, 0)),
                    game_font.render("BRAINROT RUN", False, (255, 215, 0)).get_rect(center=(400, 60)))
        screen.blit(small_font.render("SPACE: play   H: scores   S: shop", False, (200, 200, 200)),
                    small_font.render("SPACE: play   H: scores   S: shop", False, (200, 200, 200)).get_rect(center=(400, 350)))
        screen.blit(small_font.render("Coins: " + str(total_coins), False, (255, 215, 0)),
                    small_font.render("Coins: " + str(total_coins), False, (255, 215, 0)).get_rect(center=(400, 380)))

    elif game_state == "char_select":
        screen.fill((25, 18, 45))
        screen.blit(game_font.render("Choose Your Character", False, (255, 215, 0)),
                    game_font.render("Choose Your Character", False, (255, 215, 0)).get_rect(center=(400, 40)))
        names = ["Tralalero", "T.T.T. Sahur"]
        descs = ["Floaty jump", "Strong jump, heavy fall"]
        for i in range(2):
            cx = 200 + i * 400
            color = (80, 60, 120) if i == selected_char else (45, 35, 65)
            pygame.draw.rect(screen, color, (cx - 110, 80, 220, 240), border_radius=14)
            if i == selected_char:
                pygame.draw.rect(screen, (200, 160, 255), (cx - 110, 80, 220, 240), 3, border_radius=14)
            screen.blit(pygame.transform.scale(char_walk[i][0], (100, 100)),
                        pygame.transform.scale(char_walk[i][0], (100, 100)).get_rect(center=(cx, 175)))
            screen.blit(small_font.render(names[i], False, (255, 255, 255)),
                        small_font.render(names[i], False, (255, 255, 255)).get_rect(center=(cx, 248)))
            screen.blit(tiny_font.render(descs[i], False, (190, 190, 220)),
                        tiny_font.render(descs[i], False, (190, 190, 220)).get_rect(center=(cx, 272)))
        screen.blit(small_font.render("LEFT/RIGHT   SPACE to start", False, (220, 220, 220)),
                    small_font.render("LEFT/RIGHT   SPACE to start", False, (220, 220, 220)).get_rect(center=(400, 370)))

    elif game_state == "playing":
        bg_offset += game_speed
        biome = (score // 500) % len(backgrounds)
        bx = -(bg_offset % 800)
        screen.blit(backgrounds[biome], (bx, 0))
        screen.blit(backgrounds[biome], (bx + 800, 0))

        score_acc += 1 / 60.0
        score = int(score_acc) + coins_run * 10
        game_speed = 5 + score // 200

        move_and_collect_coins()
        move_obstacles()

        gravity_speed += GRAVITY[selected_char]
        player_rect.y += int(gravity_speed)
        if player_rect.bottom >= GROUND_Y:
            player_rect.bottom = GROUND_Y
            jumps_used = 0

        player_animation()
        screen.blit(player_surf, player_rect)

        # HUD
        screen.blit(game_font.render("Score: " + str(score), False, (255, 255, 255)),
                    game_font.render("Score: " + str(score), False, (255, 255, 255)).get_rect(center=(400, 30)))
        for i in range(lives):
            screen.blit(heart_surf, heart_surf.get_rect(center=(770 - i * 36, 30)))
        screen.blit(coin_surf, coin_surf.get_rect(center=(750, 65)))
        screen.blit(small_font.render(str(coins_run), False, (255, 215, 0)), (700, 55))

        if not check_collisions():
            handle_death()

    elif game_state == "paused":
        biome = (score // 500) % len(backgrounds)
        screen.blit(backgrounds[biome], (0, 0))
        overlay = pygame.Surface((800, 400))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        screen.blit(game_font.render("PAUSED", False, (255, 255, 255)),
                    game_font.render("PAUSED", False, (255, 255, 255)).get_rect(center=(400, 180)))
        screen.blit(small_font.render("P to resume   Q to quit", False, (200, 200, 200)),
                    small_font.render("P to resume   Q to quit", False, (200, 200, 200)).get_rect(center=(400, 240)))

    elif game_state == "game_over":
        screen.fill((10, 10, 22))
        screen.blit(base_surfs[selected_char], base_surfs[selected_char].get_rect(center=(400, 200)))
        screen.blit(game_font.render("GAME OVER", False, (220, 60, 60)),
                    game_font.render("GAME OVER", False, (220, 60, 60)).get_rect(center=(400, 50)))
        screen.blit(small_font.render("Score: " + str(score), False, (255, 255, 255)),
                    small_font.render("Score: " + str(score), False, (255, 255, 255)).get_rect(center=(400, 320)))
        screen.blit(small_font.render("Coins earned: " + str(coins_run), False, (255, 215, 0)),
                    small_font.render("Coins earned: " + str(coins_run), False, (255, 215, 0)).get_rect(center=(400, 350)))
        screen.blit(small_font.render("SPACE to play again   M for menu", False, (200, 200, 200)),
                    small_font.render("SPACE to play again   M for menu", False, (200, 200, 200)).get_rect(center=(400, 385)))

    elif game_state == "high_scores":
        screen.fill((20, 20, 40))
        screen.blit(game_font.render("HIGH SCORES", False, (255, 215, 0)),
                    game_font.render("HIGH SCORES", False, (255, 215, 0)).get_rect(center=(400, 40)))
        if not scores:
            screen.blit(small_font.render("No scores yet!", False, (200, 200, 200)),
                        small_font.render("No scores yet!", False, (200, 200, 200)).get_rect(center=(400, 200)))
        else:
            for i in range(len(sorted(scores, reverse=True)[:10])):
                s = sorted(scores, reverse=True)[i]
                color = (255, 215, 0) if i == 0 else (200, 200, 200)
                screen.blit(small_font.render(str(i + 1) + ".  " + str(s), False, color),
                            small_font.render(str(i + 1) + ".  " + str(s), False, color).get_rect(center=(400, 100 + i * 26)))
        screen.blit(small_font.render("SPACE to return", False, (150, 150, 150)),
                    small_font.render("SPACE to return", False, (150, 150, 150)).get_rect(center=(400, 375)))

    elif game_state == "shop":
        screen.fill((30, 25, 55))
        screen.blit(game_font.render("SHOP", False, (255, 215, 0)),
                    game_font.render("SHOP", False, (255, 215, 0)).get_rect(center=(400, 40)))
        screen.blit(small_font.render("Your coins: " + str(total_coins), False, (255, 215, 0)),
                    small_font.render("Your coins: " + str(total_coins), False, (255, 215, 0)).get_rect(center=(400, 85)))
        pending = load_boost()
        items = [("[1] Extra Life - 25 coins", "extra_life"),
                 ("[2] Starter Shield - 50 coins", "shield")]
        for i in range(len(items)):
            y = 150 + i * 80
            color = (60, 100, 60) if pending == items[i][1] else (45, 38, 75)
            pygame.draw.rect(screen, color, (150, y, 500, 55), border_radius=10)
            pygame.draw.rect(screen, (255, 215, 0), (150, y, 500, 55), 2, border_radius=10)
            screen.blit(small_font.render(items[i][0], False, (255, 255, 255)), (170, y + 16))
            if pending == items[i][1]:
                screen.blit(tiny_font.render("QUEUED", False, (130, 255, 130)), (560, y + 20))
        screen.blit(small_font.render("SPACE to leave", False, (200, 200, 200)),
                    small_font.render("SPACE to leave", False, (200, 200, 200)).get_rect(center=(400, 375)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()