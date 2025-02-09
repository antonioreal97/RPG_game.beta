import os
import pygame
import random
from settings import WIDTH, HEIGHT, WHITE, BLACK, NPC_INTERACTION_DISTANCE

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, name, image_path, dialogues):
        super().__init__()

        # Tenta carregar a imagem do NPC; se não encontrar, usa uma imagem padrão
        if os.path.exists(image_path):
            original_image = pygame.image.load(image_path).convert_alpha()
        else:
            print(f"⚠️ Imagem '{image_path}' não encontrada para o NPC '{name}'. Usando imagem padrão.")
            original_image = pygame.Surface((100, 100))
            original_image.fill((150, 150, 150))

        # Ajuste dinâmico do tamanho para manter a proporção
        scale_height = 200  # Altura fixa para NPCs
        original_width, original_height = original_image.get_size()
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

    def check_proximity(self, player):
        """Verifica se o jogador está próximo do NPC para permitir a interação."""
        distance = pygame.math.Vector2(self.rect.center).distance_to(player.rect.center)
        self.player_near = distance < NPC_INTERACTION_DISTANCE

    def interact(self):
        """
        Inicia o diálogo com o NPC quando o jogador pressiona 'X',
        desde que o jogador esteja próximo e o diálogo ainda não tenha sido finalizado.
        """
        if self.player_near and not self.finished_interaction:
            self.interacting = True

    def advance_dialogue(self):
        """
        Avança para o próximo diálogo ao pressionar 'X'.
        Finaliza a interação quando não houver mais diálogos.
        """
        if self.interacting:
            if self.current_dialogue < len(self.dialogues) - 1:
                self.current_dialogue += 1
            else:
                self.interacting = False
                self.finished_interaction = True

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

    def end_interaction(self):
        """Finaliza a interação do NPC, permitindo a progressão do jogo."""
        self.interacting = False
        self.finished_interaction = True
        print(f"✅ {self.name}: Interação concluída!")

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
                "Se encontrar uma chave de runas, traga para mim. Posso lhe contar mais sobre o que aconteceu aqui."
            ]
        }
    ]

    chosen_npc = random.choice(npc_list)
    pos = (random.randint(200, WIDTH - 200), random.randint(200, HEIGHT - 200))
    return NPC(pos, chosen_npc["name"], chosen_npc["image"], chosen_npc["dialogues"])
