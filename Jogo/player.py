import os
import pygame
import sys
import time
from settings import *
from inventory import Inventory

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # Caminho dos assets
        self.current_path = os.path.dirname(__file__)
        self.image_paths = {
            "normal": os.path.join(self.current_path, "assets", "player.png"),
            "special1": os.path.join(self.current_path, "assets", "player1.png"),
            "special2": os.path.join(self.current_path, "assets", "player2.png"),
        }

        # Carrega a imagem normal
        self.image = pygame.transform.scale(
            pygame.image.load(self.image_paths["normal"]).convert_alpha(), (150, 150)
        )
        self.rect = self.image.get_rect(center=pos)

        # Atributos do jogador
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.mana = PLAYER_MANA
        self.max_mana = PLAYER_MANA
        self.base_damage = 20
        self.special_damage = 50
        self.last_attack = 0
        self.last_special_attack = 0
        self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
        self.special_cooldown = 3000
        self.mana_cost = 30
        self.inventory = Inventory()

        # Multiplicadores de Dano e Vida
        self.damage_multiplier = 1
        self.multiplier_active = False
        self.multiplier_end_time = 0
        self.super_health_active = False
        self.super_health_end_time = 0

        # Sistema de Level e XP
        self.xp = 0
        self.level = 1
        self.xp_to_next_level = 100

        # Controle de troca de imagem
        self.special_item_time = 0  # Última vez que pegou um item especial
        self.image_change_end_time = 0  # Quando a imagem deve voltar ao normal

    def update(self, keys):
        """Atualiza a movimentação do jogador e verifica efeitos ativos."""
        dx, dy = 0, 0
        if keys[pygame.K_w]: dy = -self.speed
        if keys[pygame.K_s]: dy = self.speed
        if keys[pygame.K_a]: dx = -self.speed
        if keys[pygame.K_d]: dx = self.speed

        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x + dx))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y + dy))

        # Verifica se os buffs expiraram
        self.check_buffs()
        self.check_image_reset()

    def collect_special_item(self):
        """Altera a imagem do jogador ao pegar um item especial."""
        current_time = time.time()

        if current_time - self.special_item_time < 10:  # Pegou outro item especial em menos de 10s
            self.image = pygame.transform.scale(
                pygame.image.load(self.image_paths["special2"]).convert_alpha(), (180, 180)
            )
            print("🔵 O jogador pegou outro item especial rapidamente! Mudou para player2.png")
        else:
            self.image = pygame.transform.scale(
                pygame.image.load(self.image_paths["special1"]).convert_alpha(), (200, 200)
            )
            print("🟢 O jogador pegou um item especial! Mudou para player1.png")

        # Atualiza os tempos de troca de imagem
        self.special_item_time = current_time
        self.image_change_end_time = current_time + 10  # Voltar ao normal após 10s

    def check_image_reset(self):
        """Verifica se a imagem do jogador deve voltar ao normal."""
        if time.time() >= self.image_change_end_time and self.image_change_end_time != 0:
            self.image = pygame.transform.scale(
                pygame.image.load(self.image_paths["normal"]).convert_alpha(), (150, 150)
            )
            self.image_change_end_time = 0
            print("🔄 O tempo do efeito especial acabou. Voltando para a imagem normal.")

    def attack(self, enemies_group):
        """Realiza ataque normal."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= self.attack_cooldown:
            damage = (self.base_damage + (self.level * 2)) * self.damage_multiplier

            for enemy in enemies_group.copy():
                if self.rect.colliderect(enemy.rect):
                    enemy.take_damage(damage)
                    if enemy.health <= 0:
                        self.gain_xp(enemy.xp_reward)
                        self.restore_health(25)  # 🔥 Reduzimos o HP restaurado ao derrotar inimigos
                        print(f"⚔️ Inimigo derrotado! +25 HP. HP atual: {self.health}/{self.max_health}")

            self.last_attack = current_time

    def special_attack(self, enemies_group):
        """Realiza ataque especial com consumo de mana."""
        current_time = pygame.time.get_ticks()
        if self.mana >= self.mana_cost and (current_time - self.last_special_attack >= self.special_cooldown):
            damage = (self.special_damage + (self.level * 5)) * self.damage_multiplier
            self.mana -= self.mana_cost
            
            for enemy in enemies_group.copy():
                if self.rect.colliderect(enemy.rect):
                    enemy.take_damage(damage)
                    print(f"💥 Ataque Especial! Causou {damage} de dano.")

            self.last_special_attack = current_time
        elif self.mana < self.mana_cost:
            print("❌ Mana insuficiente para ataque especial!")

    def restore_health(self, amount):
        """Restaura HP do jogador, sem ultrapassar o máximo."""
        self.health = min(self.health + amount, self.max_health)
        print(f"❤️ Vida recuperada: {amount}. HP atual: {self.health}/{self.max_health}")

    def restore_mana(self, amount):
        """Restaura mana do jogador, sem ultrapassar o máximo."""
        self.mana = min(self.mana + amount, self.max_mana)
        print(f"🔵 Mana recuperada: {amount}. Mana atual: {self.mana}/{self.max_mana}")

    def take_damage(self, amount):
        """Reduz a vida do jogador ao ser atacado."""
        self.health -= amount
        print(f"💥 Dano recebido: {amount}. HP atual: {self.health}/{self.max_health}")

        if self.health <= 0:
            self.game_over()

    def gain_xp(self, amount):
        """Ganha XP e sobe de nível se necessário."""
        self.xp += amount
        print(f"🎉 XP Gained: {amount}! Total XP: {self.xp}/{self.xp_to_next_level}")

        if self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        """Aumenta o nível e melhora os atributos (com progressão mais difícil)."""
        self.level += 1
        self.xp = 0
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)

        # 🔥 Agora ganha apenas +15 HP por nível
        self.health = min(self.health + 15, self.max_health)
        self.mana = min(self.mana + 20, self.max_mana)

        print(f"🔥 Level UP! Novo nível: {self.level}")
        print(f"❤️ HP restaurado para {self.health}/{self.max_health}")
        print(f"🔵 Mana restaurada para {self.mana}/{self.max_mana}")

    def activate_damage_multiplier(self):
        """Ativa o multiplicador de dano por 10 segundos."""
        self.damage_multiplier = 0.5
        self.multiplier_active = True
        self.multiplier_end_time = time.time() + 10
        print("🔥 Dano x2 ativado por 10 segundos!")

    def activate_super_health(self):
        """Triplica a vida do jogador por 30 segundos."""
        if not self.super_health_active:
            print("💖 Poção de Vida Especial ativada! HP x3 por 30 segundos!")
            self.max_health *= 3
            self.health = self.max_health
            self.super_health_active = True
            self.super_health_end_time = time.time() + 30

    def check_buffs(self):
        """Verifica se os buffs de dano e vida especial expiraram."""
        if self.multiplier_active and time.time() >= self.multiplier_end_time:
            self.damage_multiplier = 1
            self.multiplier_active = False
            print("⏳ Dano x2 expirado!")

        if self.super_health_active and time.time() >= self.super_health_end_time:
            self.max_health //= 3  # Retorna ao valor normal
            self.health = min(self.health, self.max_health)  # Ajusta o HP atual
            self.super_health_active = False
            print("💖 Poção de Vida Especial acabou! HP voltou ao normal.")

    def game_over(self):
        """Exibe a tela de Game Over."""
        print("💀 GAME OVER! Você foi derrotado.")

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        gameover_path = os.path.join(os.path.dirname(__file__), "assets", "gameover.png")
        gameover_image = pygame.image.load(gameover_path).convert()

        running = True
        while running:
            screen.blit(gameover_image, (0, 0))
            font = pygame.font.SysFont("arial", 36)
            text = font.render("Pressione R para Reiniciar ou ESC para Sair", True, WHITE)
            screen.blit(text, (WIDTH // 2 - 200, HEIGHT - 100))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_r:
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "restart"}))
                        running = False
