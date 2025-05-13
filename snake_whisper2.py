import pygame
import random
import whisper
import pyaudio
import wave
import threading
import speech_recognition as sr
import sys


def main():
    # Snake game setup
    pygame.init()

    WIDTH, HEIGHT = 600, 400
    CELL_SIZE = 20
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    snake = [(100, 100), (90, 100), (80, 100)]
    direction = "RIGHT"
    food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

    font = pygame.font.SysFont(None, 36)

    def draw_snake(snake):
        for segment in snake:
            pygame.draw.rect(screen, (0, 255, 0), (*segment, CELL_SIZE, CELL_SIZE))

    recognizer = sr.Recognizer()
    command = ''

    with sr.Microphone() as source:
        print("\nAdjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Ready! Start speaking...\n")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
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

            # Map speech commands to directions
            if "up" in command and direction != "DOWN":
                direction = "UP"
            if "down" in command and direction != "UP":
                direction = "DOWN"
            if "left" in command and direction != "RIGHT":
                direction = "LEFT"
            if "right" in command and direction != "LEFT":
                direction = "RIGHT"

            # Move the snake
            x, y = snake[0]
            if direction == "UP":
                y -= CELL_SIZE
            if direction == "DOWN":
                y += CELL_SIZE
            if direction == "LEFT":
                x -= CELL_SIZE
            if direction == "RIGHT":
                x += CELL_SIZE

            snake.insert(0, (x, y))
            if snake[0] == food:
                food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                        random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
            else:
                snake.pop()

            # Check for collisions
            if (x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or snake[0] in snake[1:]):
                break

            # Draw everything
            screen.fill((0, 0, 0))
            draw_snake(snake)
            pygame.draw.rect(screen, (255, 0, 0), (*food, CELL_SIZE, CELL_SIZE))
            pygame.display.flip()
            clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()