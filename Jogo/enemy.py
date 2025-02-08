import os
import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        current_path = os.path.dirname(__file__)
        assets_path = os.path.join(current_path, "assets", "enemy.png")

        original_image = pygame.image.load(assets_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (256, 256))  # Ajuste para o tamanho desejado
        self.rect = self.image.get_rect(center=pos)
        self.speed = ENEMY_SPEED
        self.health = ENEMY_HEALTH

    def update(self, player):
        if player.rect.x > self.rect.x:
            self.rect.x += self.speed
        if player.rect.x < self.rect.x:
            self.rect.x -= self.speed
        if player.rect.y > self.rect.y:
            self.rect.y += self.speed
        if player.rect.y < self.rect.y:
            self.rect.y -= self.speed

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
