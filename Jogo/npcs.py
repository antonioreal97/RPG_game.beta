import os
import pygame
import random
from settings import WIDTH, HEIGHT, WHITE, BLACK, NPC_INTERACTION_DISTANCE, NPC_DIALOGUE_DELAY

# Cache global para evitar recarregamento repetido de imagens de NPCs
npc_image_cache = {}

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, name, image_path, dialogues):
        super().__init__()

        # Tenta obter a imagem do cache; se não existir, carrega e armazena
        if image_path in npc_image_cache:
            original_image = npc_image_cache[image_path]
        else:
            if os.path.exists(image_path):
                original_image = pygame.image.load(image_path).convert_alpha()
            else:
                print(f"⚠️ Imagem '{image_path}' não encontrada para o NPC '{name}'. Usando imagem padrão.")
                original_image = pygame.Surface((100, 100), pygame.SRCALPHA)
                original_image.fill((150, 150, 150))
            npc_image_cache[image_path] = original_image

        # Ajuste dinâmico do tamanho para manter a proporção (altura fixa de 200 pixels)
        scale_height = 200
        original_width, original_height = original_image.get_size()
        if original_height == 0:
            original_height = 1  # Evita divisão por zero
        scale_width = int((scale_height / original_height) * original_width)
        self.image = pygame.transform.scale(original_image, (scale_width, scale_height))
        self.rect = self.image.get_rect(center=pos)

        # Informações do NPC
        self.name = name
        self.dialogues = dialogues  # Lista de diálogos do NPC
        self.current_dialogue = 0   # Índice do diálogo atual
        self.interacting = False    # Indica se o NPC está em interação ativa
        self.player_near = False    # Indica se o jogador está próximo
        self.finished_interaction = False  # Indica se o diálogo já foi concluído

        # Tempo para aumentar o tempo do diálogo (delay entre avanços)
        self.dialogue_delay = NPC_DIALOGUE_DELAY  # 2000 ms de delay
        self.last_dialogue_advance_time = 0

    def check_proximity(self, player):
        """Verifica se o jogador está próximo do NPC para permitir a interação."""
        distance = pygame.math.Vector2(self.rect.center).distance_to(player.rect.center)
        self.player_near = distance < NPC_INTERACTION_DISTANCE

    def update(self, player=None):
        """Atualiza o estado do NPC, verificando automaticamente a proximidade do jogador, se fornecido."""
        if player is not None:
            self.check_proximity(player)

    def interact(self):
        """
        Inicia o diálogo com o NPC quando o jogador pressiona 'X',
        desde que o jogador esteja próximo e o diálogo ainda não tenha sido finalizado.
        """
        if self.player_near and not self.finished_interaction:
            self.interacting = True
            self.last_dialogue_advance_time = pygame.time.get_ticks()

    def advance_dialogue(self):
        """
        Avança para o próximo diálogo ao pressionar 'X'.
        Só avança se o tempo de delay tiver sido cumprido.
        Quando não houver mais diálogos, finaliza a interação e dropa um item.
        """
        if self.interacting:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_dialogue_advance_time >= self.dialogue_delay:
                if self.current_dialogue < len(self.dialogues) - 1:
                    self.current_dialogue += 1
                    self.last_dialogue_advance_time = current_time
                else:
                    self.end_interaction()

    def draw_dialogue_box(self, screen, font):
        """Desenha a caixa de diálogo na tela enquanto o NPC está interagindo."""
        if self.interacting:
            dialogue_text = self.dialogues[self.current_dialogue]

            # Configuração da caixa de diálogo
            box_width, box_height = WIDTH - 100, 100
            box_x, box_y = 50, HEIGHT - 150
            pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height))
            pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), 2)

            # Renderiza o texto do diálogo
            text_surface = font.render(f"{self.name}: {dialogue_text}", True, WHITE)
            screen.blit(text_surface, (box_x + 20, box_y + 30))

            # Instrução para continuar o diálogo
            continue_text = font.render("Pressione X para continuar...", True, WHITE)
            screen.blit(continue_text, (box_x + 20, box_y + 60))

    def draw_interaction_prompt(self, screen, font):
        """Exibe um prompt indicando que o jogador pode interagir com o NPC."""
        if self.player_near and not self.interacting and not self.finished_interaction:
            prompt_text = font.render("Pressione X para falar", True, WHITE)
            # Posiciona o prompt centralizado horizontalmente acima do NPC
            prompt_x = self.rect.centerx - prompt_text.get_width() // 2
            prompt_y = self.rect.top - 30
            screen.blit(prompt_text, (prompt_x, prompt_y))

    def drop_item(self):
        """Cria e retorna um item de Super Health Potion."""
        from item import Item
        item = Item(self.rect.center, "Super Health Potion", special=True)
        print("💖 Super Health Potion dropada!")
        return item

    def end_interaction(self):
        """
        Finaliza a interação do NPC, permitindo a progressão do jogo e dropando um item.
        Retorna o item dropado para que a lógica de nível possa adicioná-lo aos grupos.
        """
        self.interacting = False
        self.finished_interaction = True
        print(f"✅ {self.name}: Interação concluída!")
        return self.drop_item()

def spawn_npc():
    """Gera um NPC aleatório no mapa."""
    npc_list = [
        {
            "name": "Velho Sábio",
            "image": os.path.join(os.path.dirname(__file__), "assets", "npc1.png"),
            "dialogues": [
                "Os tempos antigos escondem segredos profundos...",
                "Houve uma guerra há séculos, e os ecos ainda ressoam...",
                "Se deseja sobreviver, deve aprender a usar suas habilidades com sabedoria."
            ]
        },
        {
            "name": "Mercador Misterioso",
            "image": os.path.join(os.path.dirname(__file__), "assets", "npc_merchant.png"),
            "dialogues": [
                "Hahaha! Você parece precisar de suprimentos, jovem guerreiro...",
                "Nem tudo que reluz é ouro. Às vezes, o verdadeiro poder está escondido nas sombras.",
                "Um bom aventureiro sempre tem uma poção extra."
            ]
        },
        {
            "name": "Guardião das Ruínas",
            "image": os.path.join(os.path.dirname(__file__), "assets", "npc_guardian.png"),
            "dialogues": [
                "Eu protejo este local há mais tempo do que você pode imaginar...",
                "Cuidado! Há criaturas nas profundezas que não deveriam ser despertadas.",
                "Se encontrar uma chave de runas, traga para mim. Posso lhe contar mais sobre."
            ]
        }
    ]

    chosen_npc = random.choice(npc_list)
    pos = (random.randint(200, WIDTH - 200), random.randint(200, HEIGHT - 200))
    return NPC(pos, chosen_npc["name"], chosen_npc["image"], chosen_npc["dialogues"])
