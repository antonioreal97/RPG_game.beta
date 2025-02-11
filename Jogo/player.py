import os
import pygame
import sys
import time
from settings import *  # Certifique-se de que MAP_WIDTH e MAP_HEIGHT estão definidos em settings
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
        self.normal_image = pygame.transform.scale(
            pygame.image.load(self.image_paths["normal"]).convert_alpha(), (125, 125)
        )
        self.image = self.normal_image
        self.rect = self.image.get_rect(center=pos)

        # Animação de ataque: carrega frames de ataque
        self.attack_frames = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(self.current_path, "assets", "player_frame(1).png")).convert_alpha(), (1920, 1080)
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join(self.current_path, "assets", "player_frame(2).png")).convert_alpha(), (1920, 1080)
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join(self.current_path, "assets", "player_frame(3).png")).convert_alpha(), (1920, 1080)
            )
        ]
        self.attack_anim_duration = 300  # duração total da animação de ataque (ms)
        self.attack_anim_frame_time = 100  # tempo de cada frame (ms)
        self.attack_anim_start = None   # hora de início da animação
        self.attacking = False

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

        # Multiplicadores de dano e vida
        self.damage_multiplier = 1
        self.multiplier_active = False
        self.multiplier_end_time = 0
        self.super_health_active = False
        self.super_health_end_time = 0

        # Sistema de level e XP
        self.xp = 0
        self.level = 1
        self.xp_to_next_level = 100

        # Controle de troca de imagem para itens especiais
        self.special_item_time = 0  # Última vez que pegou um item especial
        self.image_change_end_time = 0  # Momento em que a imagem deve voltar ao normal

    def update(self, keys):
        """Atualiza a movimentação do jogador, animação de ataque e verifica efeitos ativos."""
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_s]:
            dy = self.speed
        if keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_d]:
            dx = self.speed

        # Atualiza a posição, garantindo que o jogador não saia dos limites do MAPA
        self.rect.x = max(0, min(MAP_WIDTH - self.rect.width, self.rect.x + dx))
        self.rect.y = max(0, min(MAP_HEIGHT - self.rect.height, self.rect.y + dy))

        # Atualiza a animação de ataque, se estiver ocorrendo
        if self.attacking:
            elapsed = pygame.time.get_ticks() - self.attack_anim_start
            frame_index = int(elapsed / self.attack_anim_frame_time)
            if frame_index < len(self.attack_frames):
                self.image = self.attack_frames[frame_index]
            else:
                # Final da animação; volta para imagem normal
                self.image = self.normal_image
                self.attacking = False

        # Verifica se os buffs ou efeitos especiais expiraram
        self.check_buffs()
        self.check_image_reset()

    def play_attack_animation(self):
        """Inicia a animação de ataque."""
        self.attacking = True
        self.attack_anim_start = pygame.time.get_ticks()

    def collect_special_item(self):
        """Altera a imagem do jogador ao pegar um item especial."""
        current_time = time.time()

        if current_time - self.special_item_time < 10:
            self.image = pygame.transform.scale(
                pygame.image.load(self.image_paths["special2"]).convert_alpha(), (180, 180)
            )
            print("🔵 O jogador pegou outro item especial rapidamente! Mudou para player2.png")
        else:
            self.image = pygame.transform.scale(
                pygame.image.load(self.image_paths["special1"]).convert_alpha(), (200, 200)
            )
            print("🟢 O jogador pegou um item especial! Mudou para player1.png")

        self.special_item_time = current_time
        self.image_change_end_time = current_time + 10

    def check_image_reset(self):
        """Verifica se a imagem do jogador deve voltar à normalidade."""
        if time.time() >= self.image_change_end_time and self.image_change_end_time != 0:
            self.image = self.normal_image
            self.image_change_end_time = 0
            print("🔄 O tempo do efeito especial acabou. Voltando para a imagem normal.")

    def attack(self, enemies_group):
        """Realiza o ataque normal e toca a animação de ataque."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= self.attack_cooldown:
            # Inicia animação de ataque
            self.play_attack_animation()

            damage = (self.base_damage + (self.level * 2)) * self.damage_multiplier

            for enemy in enemies_group.copy():
                if self.rect.colliderect(enemy.rect):
                    enemy.take_damage(damage)
                    if enemy.health <= 0:
                        self.gain_xp(enemy.xp_reward)
                        self.restore_health(25)
                        print(f"⚔️ Inimigo derrotado! +25 HP. HP atual: {self.health}/{self.max_health}")

            self.last_attack = current_time

    def special_attack(self, enemies_group):
        """Realiza o ataque especial, consumindo mana."""
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
        """Restaura a mana do jogador, sem ultrapassar o máximo."""
        self.mana = min(self.mana + amount, self.max_mana)
        print(f"🔵 Mana recuperada: {amount}. Mana atual: {self.mana}/{self.max_mana}")

    def take_damage(self, amount):
        """Reduz o HP do jogador ao receber dano."""
        self.health -= amount
        print(f"💥 Dano recebido: {amount}. HP atual: {self.health}/{self.max_health}")
        if self.health <= 0:
            self.game_over()

    def gain_xp(self, amount):
        """Adiciona XP e verifica se o jogador sobe de nível."""
        self.xp += amount
        print(f"🎉 XP Gained: {amount}! Total XP: {self.xp}/{self.xp_to_next_level}")
        if self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        """Sobe de nível e melhora os atributos do jogador."""
        self.level += 1
        self.xp = 0
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        # Mantemos a lógica atual para restauração parcial, se desejar
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
        """Triplica a vida do jogador por 30 segundos, se o efeito não estiver ativo."""
        if not self.super_health_active:
            print("💖 Poção de Vida Especial ativada! HP x3 por 30 segundos!")
            self.max_health *= 3
            self.health = self.max_health
            self.super_health_active = True
            self.super_health_end_time = time.time() + 30

    def check_buffs(self):
        """Verifica se os buffs de dano e super health expiraram."""
        if self.multiplier_active and time.time() >= self.multiplier_end_time:
            self.damage_multiplier = 1
            self.multiplier_active = False
            print("⏳ Dano x2 expirado!")
        if self.super_health_active and time.time() >= self.super_health_end_time:
            self.max_health //= 3
            self.health = min(self.health, self.max_health)
            self.super_health_active = False
            print("💖 Poção de Vida Especial acabou! HP voltou ao normal.")

    def game_over(self):
        """Exibe a tela de Game Over e aguarda a ação do jogador."""
        print("💀 GAME OVER! Você foi derrotado.")
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        gameover_path = os.path.join(os.path.dirname(__file__), "assets", "gameover.png")
        gameover_image = pygame.image.load(gameover_path).convert()

        running = True
        while running:
            screen.blit(gameover_image, (0, 0))
            font = pygame.font.SysFont("arial", 36)
            text = font.render("Pressione R para Reiniciar ou ESC para Sair", True, (255, 255, 255))
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

    def round_win_bonus(self):
        """
        Aplica o bônus de vitória de round, aumentando permanentemente
        o HP máximo, o HP atual, a Mana máxima e a Mana atual em 10.
        """
        self.max_health += 10
        self.health += 10
        self.max_mana += 10
        self.mana += 10
        print(f"🏆 Round vencido! HP e Mana aumentados em 10. Novo HP: {self.max_health} (atual: {self.health}), Nova Mana: {self.max_mana} (atual: {self.mana})")
