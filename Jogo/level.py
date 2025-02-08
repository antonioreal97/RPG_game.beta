import pygame
import random
from enemy import Enemy
from item import Item
from settings import WIDTH, HEIGHT

class Level:
    def __init__(self, player, all_sprites, enemies_group, items_group):
        self.player = player
        self.all_sprites = all_sprites
        self.enemies_group = enemies_group
        self.items_group = items_group
        self.enemies_killed = 0  # Contador de inimigos mortos
        self.round_number = 1  # Número do round atual
        self.enemy_spawn_rate = 3  # Número inicial de inimigos
        self.round_active = True  # Controla se o round está ativo
        self.create_level()

    def create_level(self):
        """Cria os inimigos iniciais do nível."""
        for _ in range(self.enemy_spawn_rate):
            self.spawn_enemy()

    def update(self):
        """Atualiza o nível, verifica mortes de inimigos e gerencia a progressão dos rounds."""
        enemies_to_remove = []

        # Verifica quais inimigos foram mortos
        for enemy in self.enemies_group:
            if enemy.health <= 0:
                self.player.gain_xp(enemy.xp_reward)
                self.enemies_killed += 1
                enemies_to_remove.append(enemy)

        # Remove os inimigos mortos
        for enemy in enemies_to_remove:
            enemy.kill()
            self.enemies_group.remove(enemy)

        # Gera um item a cada 6 inimigos mortos
        if self.enemies_killed > 0 and self.enemies_killed % 6 == 0:
            self.spawn_item()

        # Se todos os inimigos morreram, inicia o próximo round
        if len(self.enemies_group) == 0 and self.round_active:
            self.next_round()

    def spawn_enemy(self):
        """Gera um inimigo aleatório no mapa."""
        pos = self.get_random_spawn_position()
        enemy = Enemy(pos, self.round_number, self.all_sprites, self.items_group)  # 🔥 Agora passamos os grupos!
        enemy.xp_reward = random.randint(15, 30)

        self.all_sprites.add(enemy)
        self.enemies_group.add(enemy)
        print(f"👿 Novo inimigo spawnado! Vida: {enemy.health}, XP: {enemy.xp_reward}")

    def spawn_item(self):
        """Gera um item aleatório no mapa. A cada 6 inimigos mortos, há 50% de chance de ser uma Super Health Potion."""
        pos = self.get_random_spawn_position()

        if random.random() < 0.5:  # 50% de chance de spawnar a Super Health Potion
            item_name = "Super Health Potion"
            item = Item(pos, item_name, special=True)
            print("💖 Super Health Potion apareceu no mapa!")
        else:
            item_types = ["Health Potion", "Mana Potion", "Gold Coin"]
            item_name = random.choice(item_types)
            item = Item(pos, item_name)

        # Adiciona o item ao jogo
        self.all_sprites.add(item)
        self.items_group.add(item)
        print(f"🆕 Item Spawnado: {item_name} na posição {pos}")

    def next_round(self):
        """Inicia um novo round, aumentando o número e a força dos inimigos."""
        self.round_active = False
        self.round_number += 1
        self.enemy_spawn_rate += 1

        print(f"🔥 Novo Round {self.round_number}! Agora teremos {self.enemy_spawn_rate} inimigos!")

        pygame.time.delay(1000)  # Pequeno delay antes do novo round

        for _ in range(self.enemy_spawn_rate):
            self.spawn_enemy()

        self.round_active = True

    def get_random_spawn_position(self):
        """Gera uma posição aleatória no mapa sem sobrepor o jogador."""
        while True:
            pos = (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
            if abs(pos[0] - self.player.rect.x) > 100 and abs(pos[1] - self.player.rect.y) > 100:
                return pos
