import pygame
import random
import pickle
from settings import MAP_WIDTH, MAP_HEIGHT
from enemy import Enemy
from enemyboss import EnemyBoss  # <-- Importe sua classe Boss aqui

class MultiEnemyManager:
    def __init__(self, all_sprites, enemies_group, items_group):
        """
        Gerencia inimigos para o multiplayer.
        """
        self.all_sprites = all_sprites
        self.enemies_group = enemies_group
        self.items_group = items_group

        self.round_number = 1
        self.spawn_interval = 5000  # Tempo (ms) entre spawns
        self.last_spawn_time = pygame.time.get_ticks()

    def spawn_enemy(self):
        """
        Decide se vai criar um inimigo normal ou um Boss,
        dependendo se o round atual é múltiplo de 10.
        """
        if self.round_number % 10 == 0:
            self.spawn_boss()
        else:
            self.spawn_normal_enemy()

    def spawn_normal_enemy(self):
        """
        Cria e adiciona um novo inimigo normal no mapa, em posição aleatória.
        """
        pos_x = random.randint(50, MAP_WIDTH - 50)
        pos_y = random.randint(50, MAP_HEIGHT - 50)
        enemy = Enemy((pos_x, pos_y), self.round_number, self.all_sprites, self.items_group)
        self.enemies_group.add(enemy)
        print(f"👿 Novo inimigo (round {self.round_number}) spawnado na posição {enemy.rect.topleft}!")

    def spawn_boss(self):
        """
        Cria e adiciona o Boss no mapa, em posição aleatória.
        """
        pos_x = random.randint(100, MAP_WIDTH - 100)
        pos_y = random.randint(100, MAP_HEIGHT - 100)
        boss = EnemyBoss((pos_x, pos_y), self.round_number, self.all_sprites, self.items_group)
        self.enemies_group.add(boss)
        print(f"👹 Boss spawnado no round {self.round_number}, posição {boss.rect.topleft}!")

    def update(self, players):
        """
        Atualiza os inimigos (movimentação, ataque) e spawn em intervalos de tempo.
        :param players: Lista de jogadores (ou jogador único) para o inimigo atacar.
        """
        current_time = pygame.time.get_ticks()

        # Verifica se deve spawnar um novo inimigo/boss
        if current_time - self.last_spawn_time >= self.spawn_interval:
            self.spawn_enemy()
            self.last_spawn_time = current_time

        # Atualiza cada inimigo (movimento e ataque)
        for enemy in self.enemies_group:
            enemy.update(players)

    def get_enemy_state(self):
        """
        Serializa o estado dos inimigos (posições, saúde, etc.) para enviar aos jogadores.
        """
        enemies_data = {}
        for idx, enemy in enumerate(self.enemies_group):
            enemies_data[idx] = {
                "x": enemy.rect.x,
                "y": enemy.rect.y,
                "health": enemy.health,
                "round": self.round_number,
                # Se quiser sincronizar outras infos, inclua aqui
            }
        return pickle.dumps(enemies_data)

    def sync_enemies(self, enemy_data):
        """
        Atualiza os inimigos locais com base nos dados recebidos do servidor.
        :param enemy_data: Dados dos inimigos em formato serializado.
        """
        try:
            enemies = pickle.loads(enemy_data)
            self.enemies_group.empty()

            for _, info in enemies.items():
                # Verifica se o round é múltiplo de 10 para recriar um Boss ou um inimigo normal
                if self.round_number % 10 == 0:
                    from enemyboss import EnemyBoss
                    enemy = EnemyBoss(
                        (info["x"], info["y"]),
                        info["round"],
                        self.all_sprites,
                        self.items_group
                    )
                else:
                    # Inimigo normal
                    enemy = Enemy(
                        (info["x"], info["y"]),
                        info["round"],
                        self.all_sprites,
                        self.items_group
                    )
                enemy.health = info["health"]
                self.enemies_group.add(enemy)
        except Exception as e:
            print(f"[ERROR] Falha ao sincronizar inimigos: {e}")

    def increase_difficulty(self):
        """
        Aumenta a dificuldade a cada round (ex.: round +1, reduz spawn_interval).
        """
        self.round_number += 1
        self.spawn_interval = max(3000, self.spawn_interval - 500)
        print(f"🔥 Novo Round: {self.round_number}. Inimigos mais fortes e spawn mais rápido!")
