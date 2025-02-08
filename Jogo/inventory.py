# inventory.py

class Inventory:
    def __init__(self):
        self.items = []  # lista de itens
    
    def add_item(self, item):
        self.items.append(item)
    
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
