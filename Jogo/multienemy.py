import pygame
import random
import pickle
from settings import MAP_WIDTH, MAP_HEIGHT
from enemy import Enemy as NormalEnemy
from enemy2 import Enemy as FastEnemy
from enemy3 import Enemy as TankEnemy
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
        Cria e adiciona um novo inimigo normal no mapa, escolhendo aleatoriamente
        entre Normal, Rápido e Tanque conforme o round.
        """
        pos_x = random.randint(50, MAP_WIDTH - 50)
        pos_y = random.randint(50, MAP_HEIGHT - 50)

        # Seleciona o tipo de inimigo baseado no round
        if self.round_number % 3 == 0:
            enemy_class = random.choices(
                [NormalEnemy, FastEnemy, TankEnemy],
                weights=[30, 30, 40]
            )[0]
        elif self.round_number % 2 == 0:
            enemy_class = random.choices(
                [NormalEnemy, FastEnemy, TankEnemy],
                weights=[30, 50, 20]
            )[0]
        else:
            enemy_class = random.choice([NormalEnemy, FastEnemy, TankEnemy])
        
        enemy = enemy_class((pos_x, pos_y), self.round_number, self.all_sprites, self.items_group)
        self.enemies_group.add(enemy)
        print(f"👿 Novo inimigo ({enemy.type}) (round {self.round_number}) spawnado na posição {enemy.rect.topleft}!")

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
        Atualiza os inimigos (movimentação, ataque) e realiza o spawn em intervalos de tempo.
        :param players: Lista de jogadores (ou jogador único) para os inimigos atacarem.
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
        Serializa o estado dos inimigos (posições, saúde, tipo, etc.) para enviar aos jogadores.
        """
        enemies_data = {}
        for idx, enemy in enumerate(self.enemies_group):
            enemies_data[idx] = {
                "x": enemy.rect.x,
                "y": enemy.rect.y,
                "health": enemy.health,
                "round": self.round_number,
                "type": enemy.type  # Inclui o tipo: Normal, Rápido, Tanque ou Boss
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
                enemy_type = info.get("type", "Normal")
                if enemy_type == "Boss":
                    enemy = EnemyBoss(
                        (info["x"], info["y"]),
                        info["round"],
                        self.all_sprites,
                        self.items_group
                    )
                elif enemy_type == "Tanque":
                    enemy = TankEnemy(
                        (info["x"], info["y"]),
                        info["round"],
                        self.all_sprites,
                        self.items_group
                    )
                elif enemy_type == "Rápido":
                    enemy = FastEnemy(
                        (info["x"], info["y"]),
                        info["round"],
                        self.all_sprites,
                        self.items_group
                    )
                else:
                    enemy = NormalEnemy(
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
