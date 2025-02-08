from ursina import *
from game import RPGGame  # Importa o código do jogo

class MainMenu:
    def __init__(self):
        self.app = Ursina()

        # Configurações da Janela
        window.title = "Meu RPG 3D"
        window.borderless = False
        window.fullscreen = False
        window.exit_button.visible = False
        window.fps_counter.enabled = True

        # Cria a entidade de fundo.
        # Usamos z=-10 para garantir que fique atrás de todos os elementos da UI.
        self.fundo = Sprite(
            load_texture('background1.png'),
            parent=camera.ui,
            z=-10
        )
        self.atualizar_escala_fundo('background1.png')

        # Cria o texto de introdução.
        # O parâmetro z=1 garante que o texto fique na frente do fundo.
        self.intro_texto = Text(
            text="",
            origin=(0, 0),
            background=True,
            scale=1.5,
            z=1,
            color=color.white
        )
        # Ajuste a posição do texto conforme necessário.
        self.intro_texto.position = (0, 0.3)

        # Cria o menu inicial (inicia invisível).
        self.menu = Entity(parent=camera.ui, enabled=False)
        self.botao_iniciar = Button(
            text="Iniciar Jogo",
            scale=(0.2, 0.1),
            position=(0, 0.1),
            parent=self.menu,
            on_click=self.iniciar_jogo
        )
        self.botao_sair = Button(
            text="Sair",
            scale=(0.2, 0.1),
            position=(0, -0.1),
            parent=self.menu,
            on_click=application.quit
        )

        # Sequência de introdução com os textos fragmentados e imagens de fundo correspondentes.
        self.sequence = Sequence(
            Func(self.mostrar_intro,
                 "A long time ago, in the war-torn continent of Elanotria, chaos reigned supreme. "
                 "The sorcerer Ankalath stood among the ruins of Vharnost, his once-great city, now consumed by fire and darkness. "
                 "The Emperor of Shadows, Mal’Zirath, had unleashed horrors upon the world, wielding the abyssal power of the Tear of the Abyss.",
                 "background1.png"),
            Wait(4),
            Func(self.mostrar_intro,
                 "As the last hope of the realm, Ankalath led the Order of the Silver Sun against the tide of destruction. "
                 "But their forces crumbled, their allies fell, and despair loomed over the land. "
                 "With his magic nearly drained and the armies of men, elves, and dwarves shattered, Ankalath made a final, desperate stand.",
                 "background2.png"),
            Wait(4),
            Func(self.mostrar_intro,
                 "In a last act of defiance, he carved an ancient sigil into the ground, sealing the Tear of the Abyss beneath the ruins of Vharnost. "
                 "The earth trembled, the heavens roared, and the city vanished in a blinding light, severing Mal’Zirath’s dark dominion.",
                 "background3.png"),
            Wait(4),
            Func(self.mostrar_intro,
                 "For centuries, the legend of Ankalath’s sacrifice lived on. "
                 "But whispers speak of the Tear still slumbering beneath the ruins, waiting. "
                 "And when darkness rises again, a new hero must rise to finish what Ankalath began.",
                 "background4.png"),
            Wait(4),
            Func(self.exibir_menu)
        )
        self.sequence.start()

    def atualizar_escala_fundo(self, texture_path):
        """
        Carrega a textura e ajusta a escala da imagem para que ela caiba na tela
        (mantendo a proporção e sem zoom excessivo).
        """
        texture = load_texture(texture_path)
        image_aspect = texture.width / texture.height

        # Área disponível na UI (camera.ui varia de -aspect_ratio a aspect_ratio no eixo x e de -1 a 1 no eixo y).
        ui_width = 0.5 * camera.aspect_ratio  # largura total
        ui_height = 0.5                     # altura total

        if image_aspect > (ui_width / ui_height):
            scale_x = ui_width
            scale_y = ui_width / image_aspect
        else:
            scale_y = ui_height
            scale_x = ui_height * image_aspect

        self.fundo.texture = texture
        self.fundo.scale = (scale_x, scale_y)

    def mostrar_intro(self, texto, fundo_texture):
        """Atualiza o texto da introdução e a imagem de fundo (com escala ajustada)."""
        self.intro_texto.text = texto
        self.atualizar_escala_fundo(fundo_texture)

    def exibir_menu(self):
        """Exibe o menu inicial após a introdução."""
        self.intro_texto.visible = False
        self.menu.enabled = True

    def iniciar_jogo(self):
        """Inicia o jogo, removendo o menu."""
        self.menu.enabled = False
        self.jogo = RPGGame()  # Inicia o jogo chamando a classe RPGGame

    def run(self):
        """Executa a engine Ursina."""
        self.app.run()

if __name__ == '__main__':
    menu = MainMenu()
    menu.run()
