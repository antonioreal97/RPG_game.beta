import pygame
import os
from settings import WIDTH, HEIGHT, FONT_NAME, WHITE, BLACK

class Inventory:
    def __init__(self, capacity=10):
        """Inicializa o inventário com um limite de espaço (número de tipos de itens)."""
        self.capacity = capacity  # Número máximo de tipos distintos de itens
        self.items = {}  # Dicionário para armazenar itens e quantidades (chave: item.name)
        self.scroll_offset = 0  # Controle de rolagem para inventários grandes

    def add_item(self, item):
        """
        Adiciona um item ao inventário, empilhando se já existir.
        O objeto 'item' deve possuir, pelo menos, o atributo 'name'.
        """
        if item.name in self.items or len(self.items) < self.capacity:
            if item.name in self.items:
                self.items[item.name]["quantity"] += 1
            else:
                self.items[item.name] = {"object": item, "quantity": 1}
            print(f"🆕 {item.name} adicionado ao inventário! ({self.items[item.name]['quantity']}x)")
        else:
            print("❌ Inventário cheio! Não é possível carregar mais itens.")

    def remove_item(self, item_name):
        """
        Remove um item do inventário ou reduz a quantidade se for empilhável.
        """
        if item_name in self.items:
            if self.items[item_name]["quantity"] > 1:
                self.items[item_name]["quantity"] -= 1
            else:
                del self.items[item_name]
            print(f"🗑 {item_name} removido do inventário.")
        else:
            print(f"⚠ {item_name} não está no inventário.")

    def use_item(self, item_name, player):
        """
        Usa um item aplicando seu efeito no jogador.
        Itens consumíveis, após uso, são removidos do inventário.
        """
        if item_name in self.items:
            item = self.items[item_name]["object"]

            if item_name == "Health Potion":
                player.restore_health(50)
                print("❤️ Jogador usou uma Health Potion e recuperou 50 HP!")
            elif item_name == "Mana Potion":
                player.restore_mana(30)
                print("🔵 Jogador usou uma Mana Potion e recuperou 30 MP!")
            elif item_name == "Super Health Potion":
                player.activate_super_health()
                print("💖 Jogador usou uma Super Health Potion!")
            elif item_name == "Gold Coin":
                # Geralmente, moedas não são consumidas diretamente
                print("💰 Gold Coin não pode ser usada diretamente!")
                return
            else:
                print(f"⚠ Efeito do item {item_name} não está definido.")
                return

            self.remove_item(item_name)
        else:
            print(f"⚠ {item_name} não está disponível para uso.")

    def open_inventory(self, screen, player):
        """
        Pausa o jogo e exibe o inventário na tela.
        Permite a rolagem (setas ↑/↓) e o uso de itens (teclas 1-9).
        Se o jogador tiver 10 ou mais Gold Coins, exibe também a opção de
        convertê-las em bônus de +5% no HP total ou +5% na Mana total (consumindo 10 moedas).
        Além disso, exibe estatísticas do jogador (HP, Mana e uso do inventário).
        """
        running = True
        font = pygame.font.SysFont(FONT_NAME, 32)
        clock = pygame.time.Clock()

        visible_slots = 7  # Número de itens visíveis simultaneamente

        # Carrega a imagem de fundo do inventário
        inventory_bg_path = os.path.join(os.path.dirname(__file__), "assets", "inventory.png")
        if os.path.exists(inventory_bg_path):
            background_image = pygame.image.load(inventory_bg_path).convert()
            background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        else:
            background_image = None

        while running:
            if background_image:
                screen.blit(background_image, (0, 0))
            else:
                screen.fill((30, 30, 30))
            # Título centralizado
            title = font.render("🎒 Inventário", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
            
            # Exibe estatísticas do jogador
            stats_text = font.render(
                f"HP: {player.health}/{player.max_health} | Mana: {player.mana}/{player.max_mana} | Slots: {len(self.items)}/{self.capacity}",
                True, WHITE)
            screen.blit(stats_text, (WIDTH // 2 - stats_text.get_width() // 2, 70))

            y_offset = 120
            items_list = list(self.items.items())
            visible_items = items_list[self.scroll_offset:self.scroll_offset + visible_slots]

            for idx, (item_name, details) in enumerate(visible_items):
                desc = getattr(details["object"], "description", "")
                text_str = f"{idx + 1}. {item_name} (x{details['quantity']})"
                if desc:
                    text_str += f" - {desc}"
                text = font.render(text_str, True, WHITE)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
                y_offset += 40

            instructions = font.render("↑/↓ para rolar | 1-9 para usar item | I para sair", True, WHITE)
            screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT - 80))
            
            # Opção de bônus para Gold Coins
            if "Gold Coin" in self.items and self.items["Gold Coin"]["quantity"] >= 10:
                bonus_info = font.render("Pressione 0 para converter 10 Gold Coins em +5% de HP ou Mana", True, WHITE)
                screen.blit(bonus_info, (WIDTH // 2 - bonus_info.get_width() // 2, HEIGHT - 120))

            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        running = False  # Fecha o inventário
                    elif event.key == pygame.K_DOWN:
                        if self.scroll_offset < max(0, len(self.items) - visible_slots):
                            self.scroll_offset += 1
                    elif event.key == pygame.K_UP:
                        if self.scroll_offset > 0:
                            self.scroll_offset -= 1
                    elif event.key == pygame.K_0:
                        # Opção de bônus: converter 10 Gold Coins
                        if "Gold Coin" in self.items and self.items["Gold Coin"]["quantity"] >= 10:
                            bonus_running = True
                            sub_font = pygame.font.SysFont(FONT_NAME, 32)
                            while bonus_running:
                                screen.fill((30, 30, 30))
                                bonus_text = sub_font.render("Pressione H para +5% HP ou M para +5% Mana", True, WHITE)
                                screen.blit(bonus_text, (WIDTH // 2 - bonus_text.get_width() // 2, HEIGHT // 2 - 50))
                                bonus_instructions = sub_font.render("Pressione I para cancelar", True, WHITE)
                                screen.blit(bonus_instructions, (WIDTH // 2 - bonus_instructions.get_width() // 2, HEIGHT // 2))
                                pygame.display.flip()
                                for bonus_event in pygame.event.get():
                                    if bonus_event.type == pygame.QUIT:
                                        pygame.quit()
                                        exit()
                                    elif bonus_event.type == pygame.KEYDOWN:
                                        if bonus_event.key == pygame.K_h:
                                            # Aplica bônus de HP
                                            bonus = int(player.max_health * 0.05)
                                            player.max_health += bonus
                                            player.health += bonus
                                            print(f"🏆 Bonus aplicado: +5% HP. Novo max HP: {player.max_health}")
                                            # Remove 10 Gold Coins do inventário
                                            for _ in range(10):
                                                self.remove_item("Gold Coin")
                                            bonus_running = False
                                        elif bonus_event.key == pygame.K_m:
                                            bonus = int(player.max_mana * 0.05)
                                            player.max_mana += bonus
                                            player.mana += bonus
                                            print(f"🏆 Bonus aplicado: +5% Mana. Novo max Mana: {player.max_mana}")
                                            for _ in range(10):
                                                self.remove_item("Gold Coin")
                                            bonus_running = False
                                        elif bonus_event.key == pygame.K_i:
                                            bonus_running = False
                    elif pygame.K_1 <= event.key <= pygame.K_9:
                        item_index = event.key - pygame.K_1
                        if item_index < len(visible_items):
                            item_name = visible_items[item_index][0]
                            self.use_item(item_name, player)

    def list_inventory(self):
        """
        Exibe todos os itens do inventário no console para debug.
        """
        if not self.items:
            print("📦 Inventário vazio.")
        else:
            print("🎒 Inventário:")
            for name, details in self.items.items():
                print(f"- {name} (x{details['quantity']})")
