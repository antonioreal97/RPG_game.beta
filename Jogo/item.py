# item.py
import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, name):
        super().__init__()
        self.name = name
        self.image = pygame.image.load('Jogo/assets/item.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
