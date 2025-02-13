import os
import pygame
import random
from settings import *
from item import Item  # Importa os itens para permitir o drop

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, round_number, all_sprites, items_group):
        super().__init__()

        # Caminho das imagens dos inimigos
        current_path = os.path.dirname(__file__)
        enemy_images = {
            "Normal": os.path.join(current_path, "assets", "enemy.png"),
            "Rápido": os.path.join(current_path, "assets", "enemy1.png"),
            "Tanque": os.path.join(current_path, "assets", "enemy2.png"),
        }

        # Determina o tipo de inimigo com base no round
        self.type = self.choose_enemy_type(round_number)

        # Ajusta os multiplicadores de força e dano conforme o round
        strength_multiplier = 1.5 if round_number % 2 == 0 else 1
        damage_multiplier = 0.75 if round_number % 2 == 0 else 1

        # Define atributos do inimigo conforme seu tipo
        if self.type == "Normal":
            self.speed = ENEMY_SPEED + (round_number * 0.2)
            self.health = self.max_health = (ENEMY_HEALTH + (round_number * 10)) * strength_multiplier
            self.attack_damage = (10 + (round_number * 2)) * damage_multiplier
            scale_factor = 1.0  # Tamanho normal
            self.can_be_frozen = True
        elif self.type == "Rápido":
            self.speed = ENEMY_SPEED + (round_number * 0.3)  # Mais rápido
            self.health = self.max_health = (ENEMY_HEALTH + (round_number * 5)) * strength_multiplier
            self.attack_damage = (8 + (round_number * 2)) * damage_multiplier
            scale_factor = 1.2  # Levemente maior
            self.can_be_frozen = True
        elif self.type == "Tanque":
            self.speed = ENEMY_SPEED + (round_number * 0.05)  # Muito lento
            self.health = self.max_health = (ENEMY_HEALTH + (round_number * 20)) * strength_multiplier
            self.attack_damage = (15 + (round_number * 2.5)) * damage_multiplier
            scale_factor = 1.5  # Muito maior
            self.can_be_frozen = False

        # Carrega a imagem correspondente ao tipo de inimigo
        enemy_image_path = enemy_images[self.type]
        try:
            original_image = pygame.image.load(enemy_image_path).convert_alpha()
        except pygame.error:
            print(f"⚠️ ERRO: Imagem do inimigo {enemy_image_path} não encontrada!")
            # Fallback: cria uma imagem magenta chamativa
            original_image = pygame.Surface((50, 50), pygame.SRCALPHA)
            original_image.fill((255, 0, 255))

        # Ajusta o tamanho do inimigo: cresce 2% a cada round
        scale_factor += round_number * 0.02
        new_size = (int(128 * scale_factor), int(128 * scale_factor))
        self.image = pygame.transform.scale(original_image, new_size)
        self.rect = self.image.get_rect(center=pos)

        # Configuração do ataque e do spawn
        self.attack_cooldown = 1000  # Tempo entre ataques (milissegundos)
        self.last_attack_time = 0

        self.spawn_time = pygame.time.get_ticks() + 2500  # Delay para o spawn (2.5 segundos)
        self.visible = False  # Inicialmente invisível

        # Controle de congelamento
        self.frozen_until = 0

        # Grupos para spawn de itens
        self.all_sprites = all_sprites
        self.items_group = items_group

        # Adiciona o inimigo ao grupo de sprites imediatamente
        self.all_sprites.add(self)
        print(f"👿 {self.type} spawnado na posição {self.rect.topleft}!")

    def choose_enemy_type(self, round_number):
        """
        Escolhe um tipo de inimigo aleatoriamente com base no round.
          - Em rounds múltiplos de 3: maior chance de 'Tanque'
          - Em rounds pares: maior chance de 'Rápido'
          - Caso contrário: distribuição balanceada
        """
        enemy_types = ["Normal", "Rápido", "Tanque"]

        # Maior chance de Tanque em rounds múltiplos de 3
        if round_number % 3 == 0:
            return random.choices(enemy_types, weights=[30, 30, 40])[0]
        # Maior chance de Rápido em rounds pares
        elif round_number % 2 == 0:
            return random.choices(enemy_types, weights=[30, 50, 20])[0]
        # Caso contrário, distribuição balanceada
        else:
            return random.choice(enemy_types)

    def update(self, player):
        """
        Torna o inimigo visível após o delay de spawn, verifica se está congelado
        e, se não estiver, move-se em direção ao jogador e ataca se possível.
        """
        current_time = pygame.time.get_ticks()

        # Verifica se já passou o tempo de spawn para tornar o inimigo visível
        if not self.visible:
            if current_time >= self.spawn_time:
                self.visible = True
                print(f"👀 {self.type} agora está visível!")
            else:
                return

        # Se o inimigo estiver congelado, não executa movimentação ou ataque
        if current_time < self.frozen_until:
            return

        # Movimento suave em direção ao jogador utilizando vetores
        direction = pygame.math.Vector2(
            player.rect.centerx - self.rect.centerx,
            player.rect.centery - self.rect.centery
        )
        if direction.length() != 0:
            direction = direction.normalize()
        self.rect.x += int(direction.x * self.speed)
        self.rect.y += int(direction.y * self.speed)

        self.attack(player)

    def attack(self, player):
        """Ataca o jogador se estiver próximo e se o cooldown permitir."""
        current_time = pygame.time.get_ticks()
        if (self.visible and self.rect.colliderect(player.rect) and
                (current_time - self.last_attack_time >= self.attack_cooldown)):
            player.take_damage(self.attack_damage)
            self.last_attack_time = current_time

    def take_damage(self, amount):
        """Reduz a vida do inimigo. Se a vida chegar a 0, dropa um item e remove o inimigo."""
        self.health -= amount
        if self.health <= 0:
            print(f"☠️ {self.type} eliminado!")
            self.drop_item()
            self.kill()
        else:
            self.freeze_enemy()

    def freeze_enemy(self):
        """Congela o inimigo por 1.5 segundos se ele puder ser congelado."""
        if self.can_be_frozen:
            self.frozen_until = pygame.time.get_ticks() + 1500
            print(f"❄️ {self.type} ficou congelado por 1.5 segundos!")
        else:
            print(f"🔥 {self.type} é resistente e não pode ser congelado!")

    def drop_item(self):
        """
        Faz o inimigo dropar um item ao morrer.
        - 50% de chance de dropar um item
          - Se drop_chance < 0.1: dropa uma 'Super Health Potion'
          - Caso contrário, escolhe aleatoriamente entre 'Health Potion', 'Mana Potion' e 'Gold Coin'
        """
        drop_chance = random.random()
        if drop_chance < 0.3:
            item_types = ["Health Potion", "Mana Potion", "Gold Coin"]
            
            # Pequena chance de dropar uma poção especial
            if drop_chance < 0.1:
                item_name = "Super Health Potion"
                item = Item(self.rect.center, item_name, special=True)
                print("💖 Super Health Potion dropada!")
            else:
                item_types = ["Health Potion", "Mana Potion", "Gold Coin"]
                item_name = random.choice(item_types)
                item = Item(self.rect.center, item_name)

            # Adiciona o item ao grupo de sprites
            self.all_sprites.add(item)
            self.items_group.add(item)
            print(f"🆕 Item dropado: {item_name} na posição {self.rect.center}")

    def draw_health_bar(self, screen):
        """Desenha a barra de vida acima do inimigo, indicando sua saúde atual."""
        if self.visible:
            bar_width = 50
            bar_height = 5
            fill = (self.health / self.max_health) * bar_width
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
            pygame.draw.rect(screen, (255, 255, 255), outline_rect)
            pygame.draw.rect(screen, (255, 0, 0), fill_rect)
            pygame.draw.rect(screen, (0, 0, 0), outline_rect, 1)
