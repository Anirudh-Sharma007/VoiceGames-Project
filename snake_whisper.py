import pygame
import random
import whisper
import pyaudio
import wave
import threading

# Initialize Whisper model
model = whisper.load_model("base")

# Speech recognition function
def recognize_speech():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 2
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    print("Listening...")

    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Processing...")
    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    result = model.transcribe(WAVE_OUTPUT_FILENAME)
    print("Recognized:", result['text'].lower())
    return result['text'].lower()

# # Snake game setup
# pygame.init()

# WIDTH, HEIGHT = 600, 400
# CELL_SIZE = 20
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# clock = pygame.time.Clock()

# snake = [(100, 100), (90, 100), (80, 100)]
# direction = "RIGHT"
# food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
#         random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

# font = pygame.font.SysFont(None, 36)

# def draw_snake(snake):
#     for segment in snake:
#         pygame.draw.rect(screen, (0, 255, 0), (*segment, CELL_SIZE, CELL_SIZE))

# while True:
for i in range(10):
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         pygame.quit()
    #         exit()

    # # Start a thread to listen for voice commands
    # speech_thread = threading.Thread(target=recognize_speech)
    # speech_thread.start()
    # speech_thread.join()
    command = recognize_speech()

    # Map speech commands to directions
#     if "up" in command and direction != "DOWN":
#         direction = "UP"
#     if "down" in command and direction != "UP":
#         direction = "DOWN"
#     if "left" in command and direction != "RIGHT":
#         direction = "LEFT"
#     if "right" in command and direction != "LEFT":
#         direction = "RIGHT"

#     # Move the snake
#     x, y = snake[0]
#     if direction == "UP":
#         y -= CELL_SIZE
#     if direction == "DOWN":
#         y += CELL_SIZE
#     if direction == "LEFT":
#         x -= CELL_SIZE
#     if direction == "RIGHT":
#         x += CELL_SIZE

#     snake.insert(0, (x, y))
#     if snake[0] == food:
#         food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
#                 random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
#     else:
#         snake.pop()

#     # Check for collisions
#     if (x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or snake[0] in snake[1:]):
#         break

#     # Draw everything
#     screen.fill((0, 0, 0))
#     draw_snake(snake)
#     pygame.draw.rect(screen, (255, 0, 0), (*food, CELL_SIZE, CELL_SIZE))
#     pygame.display.flip()
#     clock.tick(10)

# pygame.quit()
