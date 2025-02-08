import pygame
from settings import WIDTH, HEIGHT, MAP_WIDTH, MAP_HEIGHT, ZOOM_FACTOR

class Camera:
    def __init__(self, map_width, map_height):
        """Inicializa a câmera com as dimensões do mapa e o zoom."""
        self.camera_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.map_width = map_width
        self.map_height = map_height
        self.zoom_factor = ZOOM_FACTOR

    def apply(self, entity):
        """Aplica o deslocamento e o zoom da câmera à entidade."""
        new_x = (entity.rect.x - self.camera_rect.x) * self.zoom_factor
        new_y = (entity.rect.y - self.camera_rect.y) * self.zoom_factor
        new_w = int(entity.rect.width * self.zoom_factor)
        new_h = int(entity.rect.height * self.zoom_factor)
        return pygame.Rect(new_x, new_y, new_w, new_h)

    def update(self, target):
        """Centraliza a câmera no jogador e mantém dentro dos limites do mapa."""
        # Obtém a posição do jogador levando em conta o zoom
        player_x = target.rect.centerx - (WIDTH // 2)
        player_y = target.rect.centery - (HEIGHT // 2)

        # Garante que a câmera não saia dos limites do mapa
        max_x = self.map_width - WIDTH
        max_y = self.map_height - HEIGHT

        self.camera_rect.x = max(0, min(player_x, max_x))
        self.camera_rect.y = max(0, min(player_y, max_y))

    def apply_zoom_to_background(self, surface):
        """Aplica o zoom ao fundo do mapa, garantindo que a área da subsurface esteja dentro dos limites."""
        new_width = int(self.map_width * self.zoom_factor)
        new_height = int(self.map_height * self.zoom_factor)
        zoomed_bg = pygame.transform.smoothscale(surface, (new_width, new_height))

        # Ajusta a câmera para manter o fundo dentro da tela
        cam_x = max(0, min(self.camera_rect.x, new_width - WIDTH))
        cam_y = max(0, min(self.camera_rect.y, new_height - HEIGHT))

        camera_rect = pygame.Rect(cam_x, cam_y, WIDTH, HEIGHT)

        return zoomed_bg.subsurface(camera_rect).copy()
