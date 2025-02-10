import os
import pygame
import random
from settings import *
from item import Item  # Importa os itens para permitir o drop

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, round_number, all_sprites, items_group):
        super().__init__()

        # Caminho base para as imagens dos inimigos
        current_path = os.path.dirname(__file__)
        enemy_images = {
            "Normal": os.path.join(current_path, "assets", "enemy.png"),
            "Rápido": os.path.join(current_path, "assets", "enemy1.png"),
            "Tanque": os.path.join(current_path, "assets", "enemy2.png"),
        }

        # Escolhe o tipo de inimigo conforme o round
        self.type = self.choose_enemy_type(round_number)

        # Ajustes de força e dano para cada round
        strength_multiplier = 1.5 if round_number % 2 == 0 else 1
        damage_multiplier = 0.75 if round_number % 2 == 0 else 1

        # DEFININDO XP REWARD AQUI (Exemplo)
        # Ajuste como preferir (ex.: com base no tipo do inimigo ou round)
        base_xp = 20
        self.xp_reward = base_xp + (round_number * 5)

        # Define atributos do inimigo conforme o tipo
        if self.type == "Normal":
            self.speed = ENEMY_SPEED + (round_number * 0.2)
            self.health = self.max_health = (ENEMY_HEALTH + (round_number * 10)) * strength_multiplier
            self.attack_damage = (10 + (round_number * 2)) * damage_multiplier
            scale_factor = 1.0
            self.can_be_frozen = True
        elif self.type == "Rápido":
            self.speed = ENEMY_SPEED + (round_number * 0.3)
            self.health = self.max_health = (ENEMY_HEALTH + (round_number * 5)) * strength_multiplier
            self.attack_damage = (8 + (round_number * 2)) * damage_multiplier
            scale_factor = 1.2
            self.can_be_frozen = True
        elif self.type == "Tanque":
            self.speed = ENEMY_SPEED + (round_number * 0.05)
            self.health = self.max_health = (ENEMY_HEALTH + (round_number * 20)) * strength_multiplier
            self.attack_damage = (15 + (round_number * 2.5)) * damage_multiplier
            scale_factor = 1.5
            self.can_be_frozen = False

        # Carrega a imagem do inimigo
        enemy_image_path = enemy_images[self.type]
        try:
            original_image = pygame.image.load(enemy_image_path).convert_alpha()
        except pygame.error:
            print(f"⚠️ ERRO: Imagem do inimigo {enemy_image_path} não encontrada!")
            original_image = pygame.Surface((50, 50), pygame.SRCALPHA)
            original_image.fill((255, 0, 255))

        # Escala do inimigo: cresce 2% a cada round
        scale_factor += round_number * 0.02
        new_size = (int(128 * scale_factor), int(128 * scale_factor))
        self.image = pygame.transform.scale(original_image, new_size)
        self.rect = self.image.get_rect(center=pos)

        # Configurações de ataque e spawn
        self.attack_cooldown = 1000  # ms
        self.last_attack_time = 0
        self.spawn_time = pygame.time.get_ticks() + 2500  # Delay de spawn (2.5s)
        self.visible = False

        # Controle de congelamento
        self.frozen_until = 0

        # Grupos para drops
        self.all_sprites = all_sprites
        self.items_group = items_group

        # Adiciona o inimigo ao grupo
        self.all_sprites.add(self)
        print(f"👿 {self.type} spawnado na posição {self.rect.topleft}, XP Reward={self.xp_reward}")

    def choose_enemy_type(self, round_number):
        """
        Escolhe o tipo de inimigo:
          - Em rounds múltiplos de 3: maior chance de Tanque
          - Em rounds pares: maior chance de Rápido
          - Caso contrário: distribuição balanceada
        """
        enemy_types = ["Normal", "Rápido", "Tanque"]
        if round_number % 3 == 0:
            return random.choices(enemy_types, weights=[30, 30, 40])[0]
        elif round_number % 2 == 0:
            return random.choices(enemy_types, weights=[30, 50, 20])[0]
        else:
            return random.choice(enemy_types)

    def update(self, players):
        """
        Atualiza o inimigo a cada frame:
          - Torna visível após spawn_time;
          - Se não estiver congelado, escolhe jogador mais próximo e se move em direção a ele;
          - Ataca se colidir e cooldown permitir.
        """
        current_time = pygame.time.get_ticks()

        # Torna-se visível após spawn_time
        if not self.visible:
            if current_time >= self.spawn_time:
                self.visible = True
                print(f"👀 {self.type} agora está visível!")
            else:
                return

        # Checa congelamento
        if current_time < self.frozen_until:
            return

        # Se for um jogador único, converte players em lista
        if not isinstance(players, list):
            players = [players]

        # Seleciona o jogador mais próximo
        target = None
        min_dist = float('inf')
        for p in players:
            dist = pygame.math.Vector2(self.rect.center).distance_to(p.rect.center)
            if dist < min_dist:
                min_dist = dist
                target = p

        if target is None:
            return

        # Movimento em direção ao alvo
        direction = pygame.math.Vector2(target.rect.centerx - self.rect.centerx,
                                        target.rect.centery - self.rect.centery)
        if direction.length() != 0:
            direction = direction.normalize()
        self.rect.x += int(direction.x * self.speed)
        self.rect.y += int(direction.y * self.speed)

        # Tenta atacar
        self.attack(target)

    def attack(self, target):
        """Ataca se colidir com o alvo e se cooldown permitir."""
        current_time = pygame.time.get_ticks()
        if self.visible and self.rect.colliderect(target.rect) and (current_time - self.last_attack_time >= self.attack_cooldown):
            target.take_damage(self.attack_damage)
            self.last_attack_time = current_time

    def take_damage(self, amount):
        """Reduz a vida do inimigo e checa se morre."""
        self.health -= amount
        if self.health <= 0:
            print(f"☠️ {self.type} eliminado! XP Reward={self.xp_reward}")
            self.drop_item()
            self.kill()
        else:
            self.freeze_enemy()

    def freeze_enemy(self):
        """Congela o inimigo por 1.5s se for permitido."""
        if self.can_be_frozen:
            self.frozen_until = pygame.time.get_ticks() + 1500
            print(f"❄️ {self.type} congelado por 1.5s!")
        else:
            print(f"🔥 {self.type} é resistente a congelamento!")

    def drop_item(self):
        """
        Item drop (30% de chance):
          - Se <0.1 => 'Super Health Potion'
          - Senão => item comum aleatório
        """
        drop_chance = random.random()
        if drop_chance < 0.3:
            if drop_chance < 0.1:
                item_name = "Super Health Potion"
                item = Item(self.rect.center, item_name, special=True)
                print("💖 Super Health Potion dropada!")
            else:
                item_name = random.choice(["Health Potion", "Mana Potion", "Gold Coin"])
                item = Item(self.rect.center, item_name)
            self.all_sprites.add(item)
            self.items_group.add(item)
            print(f"🆕 Item dropado: {item_name} na posição {self.rect.center}")

    def draw_health_bar(self, screen, zoomed_rect=None):
        """
        Desenha a barra de vida acima do inimigo.
        Se 'zoomed_rect' for fornecido, desenha de acordo com as coordenadas transformadas
        (para quando há zoom no multiplayer).
        """
        if not self.visible:
            return

        # Se não usar zoomed_rect, desenha em self.rect
        if zoomed_rect is None:
            bar_width = 50
            bar_height = 5
            fill = (self.health / self.max_health) * bar_width
            fill = max(min(fill, bar_width), 0)

            outline_rect = pygame.Rect(
                self.rect.centerx - bar_width // 2,
                self.rect.top - 10,
                bar_width,
                bar_height
            )
            fill_rect = pygame.Rect(
                self.rect.centerx - bar_width // 2,
                self.rect.top - 10,
                fill,
                bar_height
            )
        else:
            # Desenha com base no rect "zoomado"
            bar_width = zoomed_rect.width * 0.6
            bar_height = 5
            fill = (self.health / self.max_health) * bar_width
            fill = max(min(fill, bar_width), 0)

            outline_rect = pygame.Rect(
                zoomed_rect.centerx - bar_width // 2,
                zoomed_rect.top - 10,
                bar_width,
                bar_height
            )
            fill_rect = pygame.Rect(
                zoomed_rect.centerx - bar_width // 2,
                zoomed_rect.top - 10,
                fill,
                bar_height
            )

        # Desenha a barra
        pygame.draw.rect(screen, (255, 255, 255), outline_rect)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (0, 0, 0), outline_rect, 1)
