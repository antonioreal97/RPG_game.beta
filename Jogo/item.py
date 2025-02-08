import pygame
import os
import random
import time

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, name, temporary=False, special=False):
        super().__init__()
        self.name = name
        self.temporary = temporary  # Define se o item é temporário (multiplicador de dano)
        self.special = special  # Define se o item é uma Poção de Vida Especial

        # Define o caminho correto da imagem do item
        current_path = os.path.dirname(__file__)
        if self.name == "Super Health Potion":
            assets_path = os.path.join(current_path, "assets", "vida.png")
        else:
            assets_path = os.path.join(current_path, "assets", "item.png")

        # Verifica se a imagem existe antes de carregar
        if os.path.exists(assets_path):
            self.image = pygame.image.load(assets_path).convert_alpha()
        else:
            print(f"⚠️ Erro: Arquivo {assets_path} não encontrado! Usando um item padrão.")
            self.image = pygame.Surface((50, 50))  # Cria um quadrado temporário
            self.image.fill((255, 255, 0))  # Amarelo para indicar erro

        # Ajusta o tamanho do item
        scale_size = (72, 72) if (self.temporary or self.special) else (48, 48)
        self.image = pygame.transform.scale(self.image, scale_size)
        self.rect = self.image.get_rect(center=pos)

        # Configuração da animação de drop
        self.start_y = self.rect.y - 100  # Começa 100 pixels acima
        self.final_y = self.rect.y  # Posição final do item
        self.rect.y = self.start_y  # Define a posição inicial acima do chão
        self.drop_speed = 5  # Velocidade da queda
        self.dropping = True  # Define que o item está caindo

    def update(self):
        """Atualiza a animação do drop do item."""
        if self.dropping:
            self.rect.y += self.drop_speed  # Faz o item cair suavemente
            if self.rect.y >= self.final_y:
                self.rect.y = self.final_y
                self.dropping = False  # Para a animação quando atingir o solo

    def apply_effect(self, player):
        """Aplica o efeito do item ao jogador e remove do jogo."""
        if self.temporary:
            print("🔥 Dano x2 ativado por 10 segundos!")
            player.activate_damage_multiplier()
        elif self.name == "Health Potion":
            player.restore_health(50)
            print("❤️ Poção de Vida consumida! +50 HP")
        elif self.name == "Mana Potion":
            player.restore_mana(30)
            print("🔵 Poção de Mana consumida! +30 Mana")
        elif self.name == "Gold Coin":
            print("💰 Você pegou uma moeda de ouro!")
        elif self.name == "Super Health Potion":
            self.activate_super_health(player)

        # Remove o item após ser coletado
        self.kill()

    def activate_super_health(self, player):
        """Triplica a vida do jogador por 30 segundos."""
        print("💖 Poção de Vida Especial ativada! HP x3 por 30 segundos!")
        player.max_health *= 3
        player.health = player.max_health
        player.super_health_active = True
        player.super_health_end_time = time.time() + 30  # Define a duração do efeito

        # Define um evento para reverter o efeito após 30 segundos
        pygame.time.set_timer(pygame.USEREVENT + 1, 30000)  # Dispara um evento após 30s

