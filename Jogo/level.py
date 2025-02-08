# level.py
import pygame
from enemy import Enemy
from item import Item
from settings import WIDTH, HEIGHT

class Level:
    def __init__(self, player, all_sprites, enemies_group, items_group):
        self.player = player
        self.all_sprites = all_sprites
        self.enemies_group = enemies_group
        self.items_group = items_group
        self.create_level()
    
    def create_level(self):
        # Cria alguns inimigos em posições fixas para demonstração
        enemy_positions = [(100, 100), (900, 200), (500, 600)]
        for pos in enemy_positions:
            enemy = Enemy(pos)
            self.all_sprites.add(enemy)
            self.enemies_group.add(enemy)
        
        # Cria alguns itens para coleta
        item_positions = [(400, 300), (700, 500)]
        for pos in item_positions:
            item = Item(pos, "Gold")
            self.all_sprites.add(item)
            self.items_group.add(item)
    
    def update(self):
        # Em um projeto maior, aqui poderiam ser tratadas mudanças de fase, eventos, etc.
        pass
