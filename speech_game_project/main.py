import pygame
from command_mapper import map_command
from demo_game import Game
from speech_recognition import command_queue

def main():
    pygame.init()
    game = Game()
    running = True
    
    while running:
        while not command_queue.empty():
            command = command_queue.get()
            action = map_command(command)
            if action:
                game.handle_voice_input(action)
        
        running = game.update()
        game.draw()
        pygame.time.delay(30)
    
    pygame.quit()

if __name__ == "__main__":
    main()
