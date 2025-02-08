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

            # Exemplo de efeito de uso de item
            if item_name == "Health Potion":
                player.health = min(player.health + 30, PLAYER_HEALTH)
                print("❤️ Jogador usou uma Poção de Vida e recuperou 30 HP!")
            
            elif item_name == "Mana Potion":
                player.mana = min(player.mana + 20, PLAYER_MANA)
                print("🔵 Jogador usou uma Poção de Mana e recuperou 20 MP!")

            self.remove_item(item_name)  # Remove um item após o uso
        else:
            print(f"⚠ {item_name} não está disponível para uso.")

    def list_inventory(self):
        """Exibe todos os itens do inventário."""
        if not self.items:
            print("📦 Inventário vazio.")
        else:
            print("🎒 Inventário:")
            for name, details in self.items.items():
                print(f"- {name} (x{details['quantity']})")
