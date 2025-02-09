import pygame
import os
import random
import time

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, name, temporary=False, special=False, description="", rarity="Common", value=0):
        """
        Inicializa o item com posição, nome e atributos opcionais.

        Parâmetros:
            pos (tuple): Posição (x, y) onde o item será criado.
            name (str): Nome do item (ex: "Health Potion").
            temporary (bool): Se True, o item possui efeito temporário (ex: multiplicador de dano).
            special (bool): Se True, o item é especial (ex: Super Health Potion).
            description (str): Descrição do item.
            rarity (str): Raridade do item (ex: "Common", "Uncommon", "Rare").
            value (int): Valor do item (pode ser usado como preço ou para outros efeitos).
        """
        super().__init__()
        self.name = name
        self.temporary = temporary
        self.special = special

        # Atribui atributos adicionais, usando valores padrão se nenhum for informado
        if not description:
            default_descriptions = {
                "Health Potion": "Restaura 50 HP",
                "Mana Potion": "Restaura 30 Mana",
                "Gold Coin": "Uma moeda valiosa",
                "Super Health Potion": "Triplica o HP por 30 segundos"
            }
            self.description = default_descriptions.get(name, "")
        else:
            self.description = description

        self.rarity = rarity
        self.value = value

        # Define o caminho correto da imagem do item
        current_path = os.path.dirname(__file__)
        item_images = {
            "Health Potion": "vida.png",
            "Mana Potion": "item.png",
            "Gold Coin": "gold_coin.png",
            "Super Health Potion": "super_health_potion.png",
        }
        assets_path = os.path.join(current_path, "assets", item_images.get(self.name, "item.png"))

        # Verifica se a imagem existe antes de carregar; caso não, usa uma superfície padrão
        if os.path.exists(assets_path):
            self.image = pygame.image.load(assets_path).convert_alpha()
        else:
            print(f"⚠️ Erro: Arquivo {assets_path} não encontrado! Usando um item padrão.")
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 255, 0))

        # Ajusta o tamanho do item
        scale_size = (72, 72) if (self.temporary or self.special) else (48, 48)
        self.image = pygame.transform.scale(self.image, scale_size)
        self.rect = self.image.get_rect(center=pos)

        # Configuração da animação de drop do item (queda suave)
        self.start_y = self.rect.y - 100  # Posição inicial (100 pixels acima)
        self.final_y = self.rect.y       # Posição final (no chão)
        self.rect.y = self.start_y       # Inicia acima do chão
        self.drop_speed = 3              # Velocidade da queda
        self.dropping = True             # Indica se o item ainda está caindo

    def update(self):
        """Atualiza a animação de drop do item."""
        if self.dropping:
            self.rect.y += self.drop_speed  # Faz o item descer suavemente
            if self.rect.y >= self.final_y:
                self.rect.y = self.final_y
                self.dropping = False       # Para a animação ao atingir o solo

    def apply_effect(self, player):
        """
        Aplica o efeito do item ao jogador e remove o item do jogo.

        Os efeitos variam conforme o nome do item ou se ele é temporário.
        """
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
            print("❤️Vida Triplica (3x)!❤️")

        # Remove o item do grupo de sprites (ou seja, do jogo) após seu uso
        self.kill()

    def activate_super_health(self, player):
        """Triplica a vida do jogador por 30 segundos, se o efeito não estiver ativo."""
        if not player.super_health_active:  # Impede múltiplas ativações simultâneas
            print("💖 Poção de Vida Especial ativada! HP x3 por 30 segundos!")
            player.max_health *= 3
            player.health = player.max_health
            player.super_health_active = True
            player.super_health_end_time = time.time() + 30  # Define a duração do efeito
            # Define um evento para reverter o efeito após 30 segundos (caso seja tratado via event loop)
            pygame.time.set_timer(pygame.USEREVENT + 1, 30000)
