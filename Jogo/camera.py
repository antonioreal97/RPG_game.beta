import pygame
from settings import WIDTH, HEIGHT, MAP_WIDTH, MAP_HEIGHT, ZOOM_FACTOR

class Camera:
    def __init__(self, map_width, map_height):
        """
        Inicializa a câmera usando as dimensões do mapa e o fator de zoom.
        O retângulo da câmera é definido em coordenadas do mundo, tendo largura e altura
        iguais à área visível dividida pelo zoom.
        """
        self.zoom_factor = ZOOM_FACTOR
        # A área visível em coordenadas do mundo:
        view_width = int(WIDTH / self.zoom_factor)
        view_height = int(HEIGHT / self.zoom_factor)
        self.camera_rect = pygame.Rect(0, 0, view_width, view_height)

        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity):
        """
        Aplica o deslocamento da câmera e o zoom à entidade.
        Converte as coordenadas do mundo para as coordenadas da tela.
        """
        new_x = (entity.rect.x - self.camera_rect.x) * self.zoom_factor
        new_y = (entity.rect.y - self.camera_rect.y) * self.zoom_factor
        new_w = int(entity.rect.width * self.zoom_factor)
        new_h = int(entity.rect.height * self.zoom_factor)
        return pygame.Rect(new_x, new_y, new_w, new_h)

    def update(self, target):
        """
        Centraliza a câmera no alvo (por exemplo, o jogador) e garante que ela permaneça
        dentro dos limites do mapa.
        """
        # Área visível (em coordenadas do mundo)
        view_width = self.camera_rect.width
        view_height = self.camera_rect.height

        # Calcula a posição centralizada do alvo
        centered_x = target.rect.centerx - view_width // 2
        centered_y = target.rect.centery - view_height // 2

        # Limites para que a câmera não ultrapasse as bordas do mapa
        max_x = self.map_width - view_width
        max_y = self.map_height - view_height

        # Atualiza a posição da câmera, garantindo que ela fique dentro dos limites
        self.camera_rect.x = max(0, min(centered_x, max_x))
        self.camera_rect.y = max(0, min(centered_y, max_y))

    def apply_zoom_to_background(self, surface):
        """
        Aplica o zoom ao fundo do mapa. Primeiro, redimensiona a imagem do fundo
        considerando o zoom. Em seguida, extrai a área correspondente à câmera,
        garantindo que ela esteja dentro dos limites da imagem redimensionada.
        """
        # Redimensiona o fundo para o zoom desejado
        zoomed_width = int(self.map_width * self.zoom_factor)
        zoomed_height = int(self.map_height * self.zoom_factor)
        zoomed_bg = pygame.transform.smoothscale(surface, (zoomed_width, zoomed_height))

        # Converte a posição da câmera para as coordenadas do fundo redimensionado
        cam_x = int(self.camera_rect.x * self.zoom_factor)
        cam_y = int(self.camera_rect.y * self.zoom_factor)

        # Garante que a área da câmera não ultrapasse os limites do fundo
        cam_x = max(0, min(cam_x, zoomed_width - WIDTH))
        cam_y = max(0, min(cam_y, zoomed_height - HEIGHT))

        camera_rect_zoom = pygame.Rect(cam_x, cam_y, WIDTH, HEIGHT)
        return zoomed_bg.subsurface(camera_rect_zoom).copy()
