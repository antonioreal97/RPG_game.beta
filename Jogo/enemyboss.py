import os
import pygame
import random
from settings import *
from item import Item

STATE_IDLE    = 0
STATE_CHASE   = 1
STATE_ATTACK  = 2
STATE_SPECIAL = 3
STATE_EVADE   = 4

class EnemyBoss(pygame.sprite.Sprite):
    def __init__(self, pos, round_number, all_sprites, items_group):
        super().__init__()
        # (Código de carregamento e escalonamento da imagem permanece o mesmo)
        current_path = os.path.dirname(__file__)
        boss_image_path = os.path.join(current_path, "assets", "boss.png")
        try:
            original_image = pygame.image.load(boss_image_path).convert_alpha()
        except pygame.error:
            print(f"⚠️ ERRO: Imagem do Boss '{boss_image_path}' não encontrada!")
            original_image = pygame.Surface((100, 100), pygame.SRCALPHA)
            original_image.fill((255, 0, 255))
        
        scale_factor = 2.0 + round_number * 0.05
        new_size = (int(256 * scale_factor), int(256 * scale_factor))
        self.image = pygame.transform.scale(original_image, new_size)
        self.rect = self.image.get_rect(center=pos)
        
        self.max_health = 500 + round_number * 50
        self.health = self.max_health
        self.attack_damage = 30 + round_number * 5
        self.speed = 1.5
        self.attack_cooldown = 1500
        self.last_attack_time = 0

        self.special_attack_cooldown = 5000
        self.last_special_attack = 0

        self.spawn_time = pygame.time.get_ticks() + 3000
        self.visible = False
        
        self.all_sprites = all_sprites
        self.items_group = items_group

        # Estado inicial do boss
        self.state = STATE_IDLE
        
        self.all_sprites.add(self)
        print(f"👹 Boss spawnado na posição {self.rect.topleft}!")

    def update(self, player):
        current_time = pygame.time.get_ticks()
        
        if not self.visible:
            if current_time >= self.spawn_time:
                self.visible = True
                print("👀 Boss agora está visível!")
            else:
                return

        # Atualiza o estado com base na saúde
        if self.health < self.max_health * 0.5:
            self.state = STATE_SPECIAL
        
        # Exemplo de transição: se o jogador estiver próximo, vai para chase
        if self.state == STATE_IDLE and self._player_is_near(player):
            self.state = STATE_CHASE

        # Comportamento baseado no estado
        if self.state == STATE_IDLE:
            self.idle_behavior()
        elif self.state == STATE_CHASE:
            self.chase_player(player)
        elif self.state == STATE_ATTACK:
            self.attack(player)
        elif self.state == STATE_SPECIAL:
            self.special_attack(player)
        elif self.state == STATE_EVADE:
            self.evade(player)

    def _player_is_near(self, player):
        distance = pygame.math.Vector2(self.rect.center).distance_to(player.rect.center)
        return distance < 300  # Exemplo: se o jogador estiver a menos de 300 pixels

    def idle_behavior(self):
        # Por exemplo, o boss pode ficar patrulhando uma área
        pass

    def chase_player(self, player):
        # Move-se em direção ao jogador
        direction = pygame.math.Vector2(player.rect.centerx - self.rect.centerx,
                                        player.rect.centery - self.rect.centery)
        if direction.length() != 0:
            direction = direction.normalize()
        self.rect.x += int(direction.x * self.speed)
        self.rect.y += int(direction.y * self.speed)
        
        # Se estiver suficientemente perto, transita para ataque
        if self.rect.colliderect(player.rect):
            self.state = STATE_ATTACK

    def attack(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            player.take_damage(self.attack_damage)
            self.last_attack_time = current_time
            print(f"👹 Boss atacou causando {self.attack_damage} de dano!")
            # Após atacar, pode voltar para chase ou manter o estado de ataque
            self.state = STATE_CHASE

    def special_attack(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_special_attack >= self.special_attack_cooldown:
            damage = self.attack_damage * 2
            player.take_damage(damage)
            if hasattr(player, 'stun'):
                player.stun(2000)
            self.last_special_attack = current_time
            print(f"💥 Boss realizou um ataque especial causando {damage} de dano!")
            # Após o ataque especial, pode recuar para um estado de evadir
            self.state = STATE_EVADE

    def evade(self, player):
        # Exemplo: o boss recua por um curto período para se reposicionar
        direction = pygame.math.Vector2(self.rect.centerx - player.rect.centerx,
                                        self.rect.centery - player.rect.centery)
        if direction.length() != 0:
            direction = direction.normalize()
        # Move mais rápido para fugir temporariamente
        self.rect.x += int(direction.x * self.speed * 2)
        self.rect.y += int(direction.y * self.speed * 2)
        # Após evadir, volta para chase
        self.state = STATE_CHASE

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            print("☠️ Boss eliminado!")
            self.drop_item()
            self.kill()
        else:
            print(f"Boss recebeu {amount} de dano. HP atual: {self.health}/{self.max_health}")

    def drop_item(self):
        item = Item(self.rect.center, "Super Health Potion", special=True)
        self.all_sprites.add(item)
        self.items_group.add(item)
        print("💖 Boss dropou uma Super Health Potion!")

    def draw_health_bar(self, screen):
        if self.visible:
            bar_width = 150
            bar_height = 10
            fill = (self.health / self.max_health) * bar_width
            outline_rect = pygame.Rect(self.rect.centerx - bar_width // 2,
                                       self.rect.top - 20, bar_width, bar_height)
            fill_rect = pygame.Rect(self.rect.centerx - bar_width // 2,
                                    self.rect.top - 20, fill, bar_height)
            pygame.draw.rect(screen, WHITE, outline_rect)
            pygame.draw.rect(screen, RED, fill_rect)
            pygame.draw.rect(screen, BLACK, outline_rect, 2)

