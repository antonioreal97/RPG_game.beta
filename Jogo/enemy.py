import os
import pygame
import random
from settings import *
from item import Item  # Importando os itens para permitir drop

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, round_number, all_sprites, items_group):
        super().__init__()

        # Obtém o caminho correto da imagem
        current_path = os.path.dirname(__file__)
        assets_path = os.path.join(current_path, "assets", "enemy.png")

        original_image = pygame.image.load(assets_path).convert_alpha()

        # Determina tipo de inimigo
        self.type = self.choose_enemy_type(round_number)

        # Atributos do inimigo ajustados para cada tipo
        if self.type == "Normal":
            self.speed = ENEMY_SPEED + (round_number * 0.01)
            self.health = self.max_health = ENEMY_HEALTH + (round_number * 10)
            self.attack_damage = 10 + (round_number * 2)
            scale_factor = 1.0  # Tamanho normal
        elif self.type == "Rápido":
            self.speed = ENEMY_SPEED + (round_number * 0.3)  # Mais rápido
            self.health = self.max_health = ENEMY_HEALTH + (round_number * 5)  # Menos vida
            self.attack_damage = 8 + (round_number * 2)  # Dano levemente menor
            scale_factor = 1.1  # Levemente maior
        elif self.type == "Tanque":
            self.speed = ENEMY_SPEED + (round_number * 0.05)  # Muito lento
            self.health = self.max_health = ENEMY_HEALTH + (round_number * 20)  # Vida muito maior
            self.attack_damage = 15 + (round_number * 2.5)  # Dano mais alto
            scale_factor = 1.5  # Muito maior

        # Aumenta o tamanho do inimigo conforme o round
        scale_factor += round_number * 0.05  # Cresce 5% por round
        new_size = (int(128 * scale_factor), int(128 * scale_factor))
        self.image = pygame.transform.scale(original_image, new_size)
        self.rect = self.image.get_rect(center=pos)

        self.attack_cooldown = 1000  # Tempo entre ataques (milissegundos)
        self.last_attack_time = 0  # Guarda o último ataque realizado

        # Delay para o spawn
        self.spawn_time = pygame.time.get_ticks() + 3000  # Adiciona 3 segundos ao tempo atual
        self.visible = False  # Inicialmente, o inimigo está invisível

        # Grupos para spawn de itens
        self.all_sprites = all_sprites
        self.items_group = items_group

    def choose_enemy_type(self, round_number):
        """Define o tipo do inimigo baseado na progressão do jogo."""
        if round_number < 3:
            return "Normal"
        elif round_number % 3 == 0:
            return "Tanque"
        elif round_number % 2 == 0:
            return "Rápido"
        else:
            return "Normal"

    def update(self, player):
        """Aguarda 3 segundos antes de se tornar visível e atacar o jogador."""
        current_time = pygame.time.get_ticks()

        if not self.visible:
            if current_time >= self.spawn_time:
                self.visible = True  # Torna o inimigo visível após 3 segundos
            return  # Se ainda não está visível, não faz nada

        # Movimenta-se em direção ao jogador
        if player.rect.x > self.rect.x:
            self.rect.x += self.speed
        if player.rect.x < self.rect.x:
            self.rect.x -= self.speed
        if player.rect.y > self.rect.y:
            self.rect.y += self.speed
        if player.rect.y < self.rect.y:
            self.rect.y -= self.speed
        
        # Verifica se o inimigo pode atacar o jogador
        self.attack(player)

    def attack(self, player):
        """Ataca o jogador se estiver próximo e o cooldown permitir."""
        current_time = pygame.time.get_ticks()
        if self.visible and self.rect.colliderect(player.rect) and (current_time - self.last_attack_time >= self.attack_cooldown):
            player.take_damage(self.attack_damage)
            self.last_attack_time = current_time  # Atualiza o tempo do último ataque

    def take_damage(self, amount):
        """Recebe dano e verifica se deve morrer."""
        self.health -= amount
        if self.health <= 0:
            print(f"☠️ {self.type} eliminado!")
            self.drop_item()  # Faz o inimigo dropar um item ao morrer
            self.kill()

    def drop_item(self):
        """Faz o inimigo dropar um item ao morrer."""
        drop_chance = random.random()  # Número entre 0 e 1

        if drop_chance < 0.5:  # 50% de chance de dropar um item
            item_types = ["Health Potion", "Mana Potion", "Gold Coin"]
            
            # Pequena chance de dropar uma poção especial
            if drop_chance < 0.1:
                item_name = "Super Health Potion"
                item = Item(self.rect.center, item_name, special=True)
                print("💖 Super Health Potion dropada!")
            else:
                item_name = random.choice(item_types)
                item = Item(self.rect.center, item_name)

            # Adiciona o item ao grupo de sprites
            self.all_sprites.add(item)
            self.items_group.add(item)
            print(f"🆕 Item dropado: {item_name} na posição {self.rect.center}")

    def draw_health_bar(self, screen):
        """Desenha a barra de vida acima do inimigo."""
        if self.visible:
            bar_width = 50
            bar_height = 5
            fill = (self.health / self.max_health) * bar_width  # Calcula o tamanho da barra verde
            outline_rect = pygame.Rect(self.rect.centerx - bar_width // 2, self.rect.top - 10, bar_width, bar_height)
            fill_rect = pygame.Rect(self.rect.centerx - bar_width // 2, self.rect.top - 10, fill, bar_height)

            pygame.draw.rect(screen, (255, 255, 255), outline_rect)  # Barra vermelha (fundo)
            pygame.draw.rect(screen, (255, 0, 0), fill_rect)  # Barra verde (vida atual)
            pygame.draw.rect(screen, (0, 0, 0), outline_rect, 1)  # Contorno preto
