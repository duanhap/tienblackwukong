import pygame

#icon = pygame.image.load('./assets/images/readme-assets/logo.png')
caption = "Tripitaka's Endless Pilgrimage"

screen_width = 1280
screen_height = 720

pygame.font.init()
font = pygame.font.Font(None, 40)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BROWN = (252, 210, 0)

class GameState:
    def __init__(self):
        self.paused = False
        self.sound_on = True
        self.fullscreen = False
        self.running = True