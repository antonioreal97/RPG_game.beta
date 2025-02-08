# player.py
import os
import pygame
from settings import *
from inventory import Inventory

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        
        # Obtém caminho absoluto correto da imagem
        current_path = os.path.dirname(__file__)
        assets_path = os.path.join(current_path, "assets", "player.png")

        original_image = pygame.image.load(assets_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (128, 128))
        self.rect = self.image.get_rect(center=pos)
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.mana = PLAYER_MANA
        self.last_attack = 0
        self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
        self.inventory = Inventory()
    
    def update(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_w]: dy = -self.speed
        if keys[pygame.K_s]: dy = self.speed
        if keys[pygame.K_a]: dx = -self.speed
        if keys[pygame.K_d]: dx = self.speed
        
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, enemies_group):
        """Ataque do jogador em inimigos próximos."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= self.attack_cooldown:
            for enemy in enemies_group:
                if self.rect.colliderect(enemy.rect):
                    enemy.take_damage(20)
            self.last_attack = current_time
