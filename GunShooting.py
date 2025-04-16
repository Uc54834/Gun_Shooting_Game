import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gun Shooting Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player (gun) properties
gun_pos = [WIDTH // 2, HEIGHT - 50]
gun_width = 40
gun_height = 20
gun_angle = 0

# Bullet properties
bullets = []
bullet_speed = 10
bullet_radius = 5

# Target properties
targets = []
target_radius = 20
target_spawn_timer = 0
target_spawn_delay = 60  # frames

# Score
score = 0
font = pygame.font.SysFont(None, 36)

def spawn_target():
    x = random.randint(target_radius, WIDTH - target_radius)
    y = random.randint(target_radius, HEIGHT // 2)
    targets.append([x, y])

def draw_gun():
    # Calculate end point of gun barrel based on angle
    end_x = gun_pos[0] + math.cos(gun_angle) * gun_width
    end_y = gun_pos[1] - math.sin(gun_angle) * gun_width
    
    pygame.draw.line(screen, BLACK, gun_pos, (end_x, end_y), gun_height)
    pygame.draw.circle(screen, BLACK, (int(gun_pos[0]), int(gun_pos[1])), gun_height)

def fire_bullet():
    # Calculate bullet direction based on gun angle
    vel_x = math.cos(gun_angle) * bullet_speed
    vel_y = -math.sin(gun_angle) * bullet_speed
    bullets.append([gun_pos[0], gun_pos[1], vel_x, vel_y])

def update_bullets():
    for bullet in bullets[:]:
        bullet[0] += bullet[2]  # x position
        bullet[1] += bullet[3]  # y position
        
        # Remove bullets that go off-screen
        if (bullet[0] < 0 or bullet[0] > WIDTH or 
            bullet[1] < 0 or bullet[1] > HEIGHT):
            bullets.remove(bullet)

def check_collisions():
    global score
    for bullet in bullets[:]:
        for target in targets[:]:
            dx = bullet[0] - target[0]
            dy = bullet[1] - target[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < target_radius + bullet_radius:
                if bullet in bullets:
                    bullets.remove(bullet)
                if target in targets:
                    targets.remove(target)
                score += 1
                break

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fire_bullet()
    
    # Get mouse position and calculate gun angle
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - gun_pos[0]
    dy = gun_pos[1] - mouse_y
    gun_angle = math.atan2(dy, dx)
    
    # Spawn targets periodically
    target_spawn_timer += 1
    if target_spawn_timer >= target_spawn_delay:
        spawn_target()
        target_spawn_timer = 0
    
    # Update game objects
    update_bullets()
    check_collisions()
    
    # Draw everything
    draw_gun()
    
    for bullet in bullets:
        pygame.draw.circle(screen, BLUE, (int(bullet[0]), int(bullet[1])), bullet_radius)
    
    for target in targets:
        pygame.draw.circle(screen, RED, (int(target[0]), int(target[1])), target_radius)
    
    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()