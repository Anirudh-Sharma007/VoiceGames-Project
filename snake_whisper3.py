import pygame
import random
# import sys
from queue import Queue
from threading import Thread
import time
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
import queue as sd_queue


def listen_for_commands(command_queue):
    model = Model("vosk-model-small-en-us-0.15")  
    recognizer = KaldiRecognizer(
        model, 16000, '["up", "down", "left", "right", "[unk]"]')
    q = sd_queue.Queue()

    def callback(indata, frames, time_, status):
        q.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=2048,
        dtype='int16',
        channels=1,
        callback=callback):
        print("🎙️ Voice recognition started using Vosk...")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text and text != "[unk]":
                    print(f"🗣️ You said: {text}")
                    command_queue.put(text)
            else:
                partial = json.loads(
                    recognizer.PartialResult()).get("partial", "")
                if partial in ["up", "down", "left", "right"]:
                    print(f"⚡ Quick match: {partial}")
                    command_queue.put(partial)

def play_game(command_queue):
    # Initialize Pygame
    pygame.init()

    # Game Constants
    WIDTH, HEIGHT = 600, 400
    CELL_SIZE = 10
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Create Game Window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    # Snake and Food Setup
    snake = [(100, 100), (90, 100), (80, 100)]
    direction = "RIGHT"
    food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

    clock = pygame.time.Clock()

    def draw_snake(snake):
        for segment in snake:
            pygame.draw.rect(screen, (0, 255, 0), (*segment, CELL_SIZE, CELL_SIZE))
    def draw_food(food):
        pygame.draw.rect(screen, (255, 0, 0), (*food, CELL_SIZE, CELL_SIZE))
    def draw_score(score):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
    def draw_game_over():
        font = pygame.font.SysFont(None, 48)
        game_over_text = font.render("Game Over!", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        time.sleep(2)
    # Game Loop
    running = True
    while running:
        screen.fill(BLACK)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check for commands in the queue
        if not command_queue.empty():
            command = command_queue.get()
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

        #if snake goes out of wall, then returns from the next wall
        if x < 0:
            x = WIDTH - CELL_SIZE
        elif x >= WIDTH:
            x = 0
        if y < 0:
            y = HEIGHT - CELL_SIZE
        elif y >= HEIGHT:
            y = 0
        snake.insert(0, (x, y))
        if snake[0] == food:
            food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                    random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
        else:
            snake.pop()


        
        # Check for collisions
        if (snake[0] in snake[1:]):
            draw_game_over()
            break
        
        # Draw everything
        draw_snake(snake)
        draw_food(food)
        draw_score(len(snake) - 3)
        pygame.display.flip()
        clock.tick(10)  

    pygame.quit()

def main():
    command_queue = Queue()
    
    game_thread = Thread(target=play_game, args=(command_queue,))
    speech_thread = Thread(target=listen_for_commands, args=(command_queue,))

    game_thread.start()
    speech_thread.start()


if __name__ == "__main__":
    main()