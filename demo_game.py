import pygame
import random
import whisper
import pyaudio
import wave
import threading
import speech_recognition as sr
import sys

def main():
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
    direction = "UP"

    recognizer = sr.Recognizer()
    command = ''
    with sr.Microphone() as source:
        print("\nAdjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Ready! Start speaking...\n")
        # Game Loop
        running = True
        clock = pygame.time.Clock()
        while running:
            screen.fill(BLACK)
            
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=1)
                print("Recognizing...")

                # Use Google's online speech recognition API
                command = recognizer.recognize_google(audio)
                print(f"🗣️  You said: {command}\n")
            except sr.UnknownValueError:
                print("❌ Could not understand audio\n")
            except sr.RequestError as e:
                print(f"🚫 Could not request results from Google Speech Recognition service; {e}\n")
            except sr.WaitTimeoutError:
                print("listening timed out while waiting for phrase to start")
            except KeyboardInterrupt:
                print("\n👋 Exiting...")
                sys.exit(0)
            # Paddle Movement (Player Controlled)
            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_w] and paddle1.top > 0:
            #     paddle1.y -= PADDLE_SPEED
            # if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
            #     paddle1.y += PADDLE_SPEED

            if("up" in command and paddle1.top > 0):
                direction = "UP"
            if("down" in command and paddle1.bottom < HEIGHT):
                direction = "DOWN"
            if(direction == "UP" and paddle1.top > 0):
                paddle1.y -= PADDLE_SPEED
            if(direction == "DOWN" and paddle1.bottom < HEIGHT):
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


if __name__ == "__main__":
    main()

