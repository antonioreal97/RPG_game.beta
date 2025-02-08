from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

class RPGGame(Entity):
    def __init__(self):
        super().__init__()

        # Criar o jogador (Primeira Pessoa)
        self.player = FirstPersonController()

        # Criar o terreno
        self.chao = Entity(
            model="plane",
            texture="grass",
            collider="box",
            scale=(20, 1, 20)
        )

        # Criar NPC
        self.npc = Entity(
            model="cube",
            texture="white_cube",
            color=color.azure,
            scale=(1, 2, 1),
            position=(3, 1, 3),
            collider="box",
            on_click=self.interagir
        )

        # Criar um inimigo
        self.inimigo = Entity(
            model="cube",
            color=color.red,
            scale=(1.5, 2, 1.5),
            position=(6, 1, 6),
            collider="box",
            on_click=self.iniciar_batalha
        )

        # Criar sistema de diálogo
        self.dialogo_texto = Text(
            text="",
            origin=(0, 0),
            background=True,
            scale=2,
            visible=False
        )

        # Variáveis do jogo
        self.em_dialogo = False
        self.batalha_ativa = False
        self.vida_jogador = 100
        self.vida_inimigo = 50

    def interagir(self):
        """Ativa o diálogo com o NPC se o jogador estiver próximo."""
        if distance(self.player.position, self.npc.position) < 2:
            self.em_dialogo = True
            self.dialogo_texto.text = "NPC: Olá, aventureiro!\nPressione 'E' para continuar."
            self.dialogo_texto.visible = True

    def iniciar_batalha(self):
        """Inicia uma batalha se o jogador estiver próximo do inimigo."""
        if distance(self.player.position, self.inimigo.position) < 2:
            self.batalha_ativa = True
            self.dialogo_texto.text = "BATALHA INICIADA!\nPressione 'Space' para atacar!"
            self.dialogo_texto.visible = True

    def atacar(self):
        """Realiza um turno de combate, aplicando dano aleatório ao jogador e ao inimigo."""
        if self.batalha_ativa:
            dano_jogador = random.randint(5, 15)
            dano_inimigo = random.randint(3, 10)

            self.vida_inimigo -= dano_jogador
            self.vida_jogador -= dano_inimigo

            self.dialogo_texto.text = (
                f"Você causou {dano_jogador} de dano!\n"
                f"O inimigo causou {dano_inimigo} de dano!\n"
                f"Vida Inimigo: {self.vida_inimigo} - Vida Jogador: {self.vida_jogador}"
            )

            if self.vida_inimigo <= 0:
                self.dialogo_texto.text = "Você venceu a batalha!\nPressione 'R' para continuar."
                self.batalha_ativa = False
            elif self.vida_jogador <= 0:
                self.dialogo_texto.text = "Você foi derrotado...\nPressione 'R' para tentar novamente."
                self.batalha_ativa = False

    def resetar(self):
        """Reseta os valores da batalha."""
        self.vida_jogador = 100
        self.vida_inimigo = 50
        self.batalha_ativa = False
        self.dialogo_texto.visible = False

    def input(self, key):
        """Método chamado quando uma tecla é pressionada."""
        if key == 'e' and self.em_dialogo:
            self.dialogo_texto.visible = False
            self.em_dialogo = False

        if key == 'f' and not self.batalha_ativa:
            self.iniciar_batalha()

        if key == 'space' and self.batalha_ativa:
            self.atacar()

        if key == 'r':
            self.resetar()

        if key == 'escape':
            application.quit()
