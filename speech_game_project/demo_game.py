import pygame

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
BALL_SPEED = [5, 5]
PADDLE_SPEED = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Ball and Paddle Setup
ball = pygame.Rect(WIDTH//2 - 15, HEIGHT//2 - 15, 30, 30)
paddle1 = pygame.Rect(20, HEIGHT//2 - 60, 10, 120)
paddle2 = pygame.Rect(WIDTH - 30, HEIGHT//2 - 60, 10, 120)
ball_dx, ball_dy = BALL_SPEED

# Game Loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BLACK)
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Paddle Movement (Player Controlled)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1.top > 0:
        paddle1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
        paddle1.y += PADDLE_SPEED
    
    # AI-Controlled Paddle Movement
    if paddle2.centery < ball.centery:
        paddle2.y += PADDLE_SPEED
    elif paddle2.centery > ball.centery:
        paddle2.y -= PADDLE_SPEED
    
    # Ball Movement
    ball.x += ball_dx
    ball.y += ball_dy
    
    # Ball Collision with Walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy = -ball_dy
    
    # Ball Collision with Paddles
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_dx = -ball_dx
    
    # Reset Ball if it Goes Out of Play
    if ball.left <= 0 or ball.right >= WIDTH:
        ball.x, ball.y = WIDTH//2 - 15, HEIGHT//2 - 15
        ball_dx, ball_dy = BALL_SPEED
    
    # Draw Elements
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()

