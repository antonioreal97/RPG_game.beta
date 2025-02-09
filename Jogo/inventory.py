import pygame
import os
from settings import WIDTH, HEIGHT, FONT_NAME, WHITE, BLACK

class Inventory:
    def __init__(self, capacity=10):
        """Inicializa o inventário com um limite de espaço."""
        self.capacity = capacity  # Tamanho máximo do inventário
        self.items = {}  # Dicionário para armazenar itens e quantidades
        self.scroll_offset = 0  # Controle de rolagem para inventários grandes

    def add_item(self, item):
        """
        Adiciona um item ao inventário, empilhando se já existir.
        O objeto 'item' deve possuir, pelo menos, o atributo 'name'.
        """
        # Permite adicionar o item se já existe ou se ainda há espaço
        if len(self.items) < self.capacity or item.name in self.items:
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

            # Aplica os efeitos do item de acordo com seu nome
            if item_name == "Health Potion":
                player.restore_health(50)  # Restaurando 50 HP conforme DB
                print("❤️ Jogador usou uma Health Potion e recuperou 50 HP!")
            elif item_name == "Mana Potion":
                player.restore_mana(30)  # Restaurando 30 MP conforme DB
                print("🔵 Jogador usou uma Mana Potion e recuperou 30 MP!")
            elif item_name == "Super Health Potion":
                player.activate_super_health()
                print("💖 Jogador usou uma Super Health Potion!")
            elif item_name == "Gold Coin":
                # Geralmente, moedas são tratadas como moeda e não como consumíveis
                print("💰 Gold Coin não pode ser usada diretamente!")
                return
            else:
                print(f"⚠ Efeito do item {item_name} não está definido.")
                return

            # Remove o item após o uso (se consumível)
            self.remove_item(item_name)
        else:
            print(f"⚠ {item_name} não está disponível para uso.")

    def open_inventory(self, screen, player):
        """
        Pausa o jogo e exibe o inventário na tela.
        Permite a rolagem (setas ↑/↓) e o uso de itens (teclas 1-9).
        """
        running = True
        font = pygame.font.Font(FONT_NAME, 32)  # Utiliza a fonte definida em settings
        clock = pygame.time.Clock()

        visible_slots = 7  # Número de itens visíveis simultaneamente na tela

        while running:
            screen.fill((30, 30, 30))  # Fundo escuro para o inventário

            # Título centralizado
            title = font.render("🎒 Inventário", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

            y_offset = 120
            items_list = list(self.items.items())
            # Calcula os itens visíveis com base no scroll
            visible_items = items_list[self.scroll_offset:self.scroll_offset + visible_slots]

            for idx, (item_name, details) in enumerate(visible_items):
                # Se o objeto possuir o atributo 'description', exibe-o junto ao item
                desc = getattr(details["object"], "description", "")
                text_str = f"{idx + 1}. {item_name} (x{details['quantity']})"
                if desc:
                    text_str += f" - {desc}"
                text = font.render(text_str, True, WHITE)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
                y_offset += 40

            instructions = font.render("↑/↓ para rolar | 1-9 para usar item | I para sair", True, WHITE)
            screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT - 80))

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
                    # Verifica se o jogador pressionou uma tecla de 1 a 9 para usar um item
                    elif pygame.K_1 <= event.key <= pygame.K_9:
                        item_index = event.key - pygame.K_1
                        if item_index < len(visible_items):
                            # Usa o item conforme sua posição na lista visível
                            item_name = visible_items[item_index][0]
                            self.use_item(item_name, player)

    def list_inventory(self):
        """
        Exibe todos os itens do inventário no console.
        Útil para debug ou testes.
        """
        if not self.items:
            print("📦 Inventário vazio.")
        else:
            print("🎒 Inventário:")
            for name, details in self.items.items():
                print(f"- {name} (x{details['quantity']})")
