import pygame
# import random
# import sys
from queue import Queue
from threading import Thread
# import time
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
import queue as sd_queue


def listen_for_commands(command_queue):
    model = Model("vosk-model-small-en-us-0.15")  # Ensure this path is correct
    recognizer = KaldiRecognizer(model, 16000, '["up", "down", "stop", "[unk]"]')
    q = sd_queue.Queue()

    def callback(indata, frames, time_, status):
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=16000, blocksize=2048, dtype='int16',
                           channels=1, callback=callback):
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
                partial = json.loads(recognizer.PartialResult()).get("partial", "")
                if partial in ["up", "down", "stop"]:
                    print(f"⚡ Quick match: {partial}")
                    command_queue.put(partial)


def play_game(command_queue):
    # Initialize Pygame
    pygame.init()

    # Game Constants
    WIDTH, HEIGHT = 800, 600
    BALL_SPEED = [4, 4]
    PADDLE_SPEED = 4
    MOVEMENT_DIST = 4
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

    command = ''
    # Game Loop
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill(BLACK)
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Check for commands in the queue
        if not command_queue.empty():
            command = command_queue.get()
            print(f"Command from queue: {command}")

        if("up" in command and paddle1.top > 0):
            direction = "UP"
        elif("down" in command and paddle1.bottom < HEIGHT):
            direction = "DOWN"
        elif("stop" in command):
            direction = "STOP"
    
        if(direction == "UP" and paddle1.top > 0):
            paddle1.y -= MOVEMENT_DIST
        if(direction == "DOWN" and paddle1.bottom < HEIGHT):
            paddle1.y += MOVEMENT_DIST

        
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


def main():
    command_queue = Queue()

    game_thread = Thread(target=play_game, args=(command_queue,))
    speech_thread = Thread(target=listen_for_commands, args=(command_queue,))
    
    speech_thread.start()
    game_thread.start()


if __name__ == "__main__":
    main()

