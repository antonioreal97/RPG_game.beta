import os
import pygame
import random
from settings import *
from item import Item  # Importa os itens para permitir o drop

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, round_number, all_sprites, items_group):
        super().__init__()

        self.current_path = os.path.dirname(__file__)
        self.type = "Normal"

        # Multiplicadores baseados no round
        strength_multiplier = 1.5 if round_number % 2 == 0 else 1
        damage_multiplier = 0.75 if round_number % 2 == 0 else 1

        # XP reward
        base_xp = 20
        self.xp_reward = base_xp + (round_number * 5)

        # Configurações específicas para o inimigo Normal
        self.speed = ENEMY_SPEED + (round_number * 0.2)
        self.health = self.max_health = (ENEMY_HEALTH + (round_number * 10)) * strength_multiplier
        self.attack_damage = (10 + (round_number * 2)) * damage_multiplier
        scale_factor = 1.0
        self.can_be_frozen = True

        # Carrega a imagem e aplica escala
        enemy_image_path = os.path.join(self.current_path, "assets", "enemy.png")
        try:
            original_image = pygame.image.load(enemy_image_path).convert_alpha()
        except pygame.error:
            print(f"⚠️ ERRO: Imagem do inimigo {enemy_image_path} não encontrada!")
            original_image = pygame.Surface((50, 50), pygame.SRCALPHA)
            original_image.fill((255, 0, 255))

        # Escala: aumenta 2% a cada round
        scale_factor += round_number * 0.02
        new_size = (int(128 * scale_factor), int(128 * scale_factor))
        self.normal_image = pygame.transform.scale(original_image, new_size)
        self.image = self.normal_image
        self.rect = self.image.get_rect(center=pos)

        # Configurações de ataque e spawn
        self.attack_cooldown = 1000  # em ms
        self.last_attack_time = 0
        self.spawn_time = pygame.time.get_ticks() + 2500  # Delay de 2.5s
        self.visible = False

        # Controle de congelamento
        self.frozen_until = 0

        # Grupos para drops
        self.all_sprites = all_sprites
        self.items_group = items_group

        # Adiciona o inimigo ao grupo de sprites
        self.all_sprites.add(self)
        print(f"👿 {self.type} spawnado na posição {self.rect.topleft}, XP Reward={self.xp_reward}")

        # --- Animação de Ataque ---
        self.attack_frames = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(self.current_path, "assets", "enemy_frame(1).png")).convert_alpha(),
                (1920, 1080)
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join(self.current_path, "assets", "enemy_frame(2).png")).convert_alpha(),
                (1920, 1080)
            )
        ]
        self.attack_anim_duration = 200      # Duração total da animação (ms)
        self.attack_anim_frame_time = 100    # Tempo de cada frame (ms)
        self.attack_anim_start = None
        self.attacking = False

    def play_attack_animation(self):
        """Inicia a animação de ataque do inimigo."""
        self.attacking = True
        self.attack_anim_start = pygame.time.get_ticks()

    def update(self, players):
        """Atualiza o inimigo a cada frame."""
        current_time = pygame.time.get_ticks()

        # Atualiza a animação de ataque se estiver ocorrendo
        if self.attacking:
            elapsed = current_time - self.attack_anim_start
            frame_index = int(elapsed / self.attack_anim_frame_time)
            if frame_index < len(self.attack_frames):
                self.image = self.attack_frames[frame_index]
            else:
                self.image = self.normal_image
                self.attacking = False

        # Torna o inimigo visível após o spawn_time
        if not self.visible:
            if current_time >= self.spawn_time:
                self.visible = True
                print(f"👀 {self.type} agora está visível!")
            else:
                return

        # Se estiver congelado, não age
        if current_time < self.frozen_until:
            return

        # Se players não for uma lista, converte para lista
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
        direction = pygame.math.Vector2(
            target.rect.centerx - self.rect.centerx,
            target.rect.centery - self.rect.centery
        )
        if direction.length() != 0:
            direction = direction.normalize()
        self.rect.x += int(direction.x * self.speed)
        self.rect.y += int(direction.y * self.speed)

        self.attack(target)

    def attack(self, target):
        """Ataca o jogador se houver colisão e o cooldown permitir."""
        current_time = pygame.time.get_ticks()
        if self.visible and self.rect.colliderect(target.rect) and (current_time - self.last_attack_time >= self.attack_cooldown):
            self.play_attack_animation()
            target.take_damage(self.attack_damage)
            self.last_attack_time = current_time

    def take_damage(self, amount):
        """Reduz a vida do inimigo. Se <=0, dropa um item e remove o inimigo."""
        self.health -= amount
        if self.health <= 0:
            print(f"☠️ {self.type} eliminado! XP Reward={self.xp_reward}")
            self.drop_item()
            self.kill()
        else:
            self.freeze_enemy()

    def freeze_enemy(self):
        """Congela o inimigo por 1.5s se permitido."""
        if self.can_be_frozen:
            self.frozen_until = pygame.time.get_ticks() + 1500
            print(f"❄️ {self.type} congelado por 1.5s!")
        else:
            print(f"🔥 {self.type} é resistente a congelamento!")

    def drop_item(self):
        """
        Realiza o drop de item (30% de chance):
          - Se drop_chance < 0.1: 'Super Health Potion'
          - Senão: item comum aleatório
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
        """Desenha a barra de vida acima do inimigo."""
        if not self.visible:
            return

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

        pygame.draw.rect(screen, (255, 255, 255), outline_rect)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (0, 0, 0), outline_rect, 1)
