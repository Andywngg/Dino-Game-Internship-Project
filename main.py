"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
Additional author: Andy Wang
Commit hash: 
"""

import pygame
from random import randint


def display_score(start_time):
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = game_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if not obstacle_list:
        return []

    updated_obstacles = []
    for obstacle_surface, obstacle_rect in obstacle_list:
        obstacle_rect.x -= 5
        screen.blit(obstacle_surface, obstacle_rect)

        if obstacle_rect.right > 0:
            updated_obstacles.append((obstacle_surface, obstacle_rect))

    return updated_obstacles

def collisions(player, obstacles):
    for _, obstacle_rect in obstacles:
        if player.colliderect(obstacle_rect):
            return False
    return True


def reset_game():
    global players_gravity_speed, obstacle_rect_list, score_start_time

    players_gravity_speed = 0
    obstacle_rect_list = []
    player_rect.bottomleft = (25, GROUND_Y)
    score_start_time = pygame.time.get_ticks()


def spawn_obstacle():
    if obstacle_rect_list:
        last_obstacle_rect = obstacle_rect_list[-1][1]
        spawn_x = max(randint(900, 1100), last_obstacle_rect.right + OBSTACLE_MIN_GAP)
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
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index=0
        player_surf = player_walk[int(player_index)]
    # play walking animation if the player is on the floor
    # display the jump surface when player is not on floor

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False
score = 0
score_start_time = 0
OBSTACLE_MIN_GAP = 260

# Game state variables
is_playing = False  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls
player_stand = pygame.image.load('graphics/player/player_jump.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400, 200))


# Load level assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)
game_name = game_font.render("Brainrot Run", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400,80))
game_message = game_font.render("Press space to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 320))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)

obstacle_rect_list = []

# Load sprite assets
player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/player/player_jump.png").convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
egg_surf = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
bc_surf = pygame.image.load("graphics/bombardino/bc.png").convert_alpha() 


while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            # When player wants to jump by pressing SPACE
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y:
                players_gravity_speed = JUMP_GRAVITY_START_SPEED
        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
                reset_game()
            
        if event.type == obstacle_timer and is_playing:
            spawn_obstacle()


    if is_playing:
        screen.fill("purple")  # Wipe the screen

        # Blit the level assets
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))
        score = display_score(score_start_time)

        # Adjust player's vertical location then blit it
        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        player_animation()
        screen.blit(player_surf, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # When player collides with any enemy, game ends
        if not collisions(player_rect, obstacle_rect_list):
            is_playing = False

    # When game is over, display game over message
    else:
        screen.fill("white")
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        players_gravity_speed = 0
        score_message = game_font.render(f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name,game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
