import pygame
import sys
import os
from settings import WIDTH, HEIGHT

def draw_text(screen, text, font, color, x, y):
    """Desenha texto na tela."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def menu():
    """Tela inicial do menu."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RPG Game - Menu")
    
    # Carregar imagem de fundo
    menu_background_path = os.path.join(os.path.dirname(__file__), "assets", "menu.png")
    menu_background = pygame.image.load(menu_background_path).convert()

    # Definir fontes e cores
    font = pygame.font.SysFont("Arial", 36)
    white = (255, 255, 255)

    # Definir botões
    button_start = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    button_exit = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

    running = True
    while running:
        screen.blit(menu_background, (0, 0))  # Exibe a imagem de fundo

        # Desenhar botões
        pygame.draw.rect(screen, (50, 50, 50), button_start)
        pygame.draw.rect(screen, (50, 50, 50), button_exit)

        # Adicionar textos aos botões
        draw_text(screen, "Iniciar Jogo", font, white, WIDTH // 2, HEIGHT // 2 - 25)
        draw_text(screen, "Sair", font, white, WIDTH // 2, HEIGHT // 2 + 75)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_start.collidepoint(mouse_pos):
                    running = False  # Sai do menu e inicia o jogo
                elif button_exit.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()  # Fecha o jogo

    return True  # Retorna True para iniciar o jogo
