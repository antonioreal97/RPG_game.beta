from ursina import *
import os

app = Ursina()

# Obtém o diretório base (onde o image.py está localizado)
base_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(base_dir, "assets", "images", "imagem1.png")
print("Tentando carregar a imagem de:", img_path)

if os.path.exists(img_path):
    texture = load_texture(img_path)
    print("Imagem carregada com sucesso!")
    # Cria um Sprite para exibir a imagem na UI.
    # Na UI do Ursina, o sistema de coordenadas tem altura 2 e largura 2*aspect_ratio.
    img_sprite = Sprite(
        texture=texture,
        parent=camera.ui,
        position=(0,0),  # Centro da tela
        scale=(2 * window.aspect_ratio, 2)
    )
else:
    print("⚠️ Imagem não encontrada:", img_path)

app.run()
