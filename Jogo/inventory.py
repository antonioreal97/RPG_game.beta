import pygame
import os
from settings import WIDTH, HEIGHT, FONT_NAME, WHITE, BLACK

class Inventory:
    def __init__(self, capacity=10):
        """Inicializa o inventário com um limite de espaço."""
        self.capacity = capacity  # Define o tamanho máximo do inventário
        self.items = {}  # Dicionário para armazenar itens e quantidades

    def add_item(self, item):
        """Adiciona um item ao inventário, empilhando se já existir."""
        if len(self.items) < self.capacity or item.name in self.items:
            if item.name in self.items:
                self.items[item.name]["quantity"] += 1  # Aumenta a contagem do item
            else:
                self.items[item.name] = {"object": item, "quantity": 1}  # Novo item
            print(f"🆕 {item.name} adicionado ao inventário! ({self.items[item.name]['quantity']}x)")
        else:
            print("❌ Inventário cheio! Não é possível carregar mais itens.")

    def remove_item(self, item_name):
        """Remove um item do inventário (ou reduz a quantidade se for empilhável)."""
        if item_name in self.items:
            if self.items[item_name]["quantity"] > 1:
                self.items[item_name]["quantity"] -= 1  # Reduz quantidade
            else:
                del self.items[item_name]  # Remove o item completamente
            print(f"🗑 {item_name} removido do inventário.")
        else:
            print(f"⚠ {item_name} não está no inventário.")

    def use_item(self, item_name, player):
        """Usa um item (exemplo: cura ou mana)."""
        if item_name in self.items:
            item = self.items[item_name]["object"]

            # Aplica os efeitos dos itens no jogador
            if item_name == "Health Potion":
                player.restore_health(30)
                print("❤️ Jogador usou uma Poção de Vida e recuperou 30 HP!")

            elif item_name == "Mana Potion":
                player.restore_mana(20)
                print("🔵 Jogador usou uma Poção de Mana e recuperou 20 MP!")

            elif item_name == "Super Health Potion":
                player.activate_super_health()
                print("💖 Jogador usou uma Poção de Vida Especial!")

            self.remove_item(item_name)  # Remove um item após o uso
        else:
            print(f"⚠ {item_name} não está disponível para uso.")

    def open_inventory(self, screen, player):
        """Pausa o jogo e exibe o inventário na tela."""
        running = True
        font = pygame.font.Font(FONT_NAME, 28)
        clock = pygame.time.Clock()

        while running:
            screen.fill((30, 30, 30))  # Fundo do inventário
            title = font.render("🎒 Inventário", True, WHITE)
            screen.blit(title, (WIDTH // 2 - 80, 50))

            y_offset = 120
            for idx, (item_name, details) in enumerate(self.items.items()):
                text = font.render(f"{idx + 1}. {item_name} (x{details['quantity']})", True, WHITE)
                screen.blit(text, (WIDTH // 2 - 150, y_offset))
                y_offset += 40

            instructions = font.render("Pressione 1-9 para usar itens | Pressione I para sair", True, WHITE)
            screen.blit(instructions, (WIDTH // 2 - 250, HEIGHT - 100))

            pygame.display.flip()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        return  # Fecha o inventário e retorna ao jogo
                    
                    # Verifica se o jogador pressionou um número para usar um item
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        item_index = event.key - pygame.K_1  # Converte a tecla para índice
                        if item_index < len(self.items):
                            item_name = list(self.items.keys())[item_index]
                            self.use_item(item_name, player)

    def list_inventory(self):
        """Exibe todos os itens do inventário no console."""
        if not self.items:
            print("📦 Inventário vazio.")
        else:
            print("🎒 Inventário:")
            for name, details in self.items.items():
                print(f"- {name} (x{details['quantity']})")
