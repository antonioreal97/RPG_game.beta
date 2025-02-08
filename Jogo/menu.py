import pygame
import sys
import os
from settings import WIDTH, HEIGHT, WHITE, BLACK

RECORDS_FILE = "records.txt"

def draw_text(screen, text, font, color, x, y):
    """Desenha texto na tela."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def save_record(player_name, rounds_survived):
    """Salva o recorde do jogador no arquivo records.txt"""
    if player_name.strip():  # Apenas salva se o jogador inserir um nome válido
        with open(RECORDS_FILE, "a") as file:
            file.write(f"{player_name},{rounds_survived}\n")

def load_records():
    """Carrega os recordes salvos e os ordena do maior para o menor"""
    if not os.path.exists(RECORDS_FILE):
        return []
    
    with open(RECORDS_FILE, "r") as file:
        records = [line.strip().split(",") for line in file.readlines()]
    
    records = [(name, int(rounds)) for name, rounds in records]
    records.sort(key=lambda x: x[1], reverse=True)  # Ordena pelo maior número de rounds
    return records

def show_records(screen):
    """Exibe a tela de recordes"""
    running = True
    font = pygame.font.SysFont("arial", 30)  # Usa fonte do sistema
    records = load_records()
    
    while running:
        screen.fill((30, 30, 30))  # Fundo escuro
        draw_text(screen, "🏆 Recordes", font, WHITE, WIDTH // 2, 50)

        y_offset = 120
        if records:
            for idx, (name, rounds) in enumerate(records[:10]):  # Mostra os 10 melhores
                text = f"{idx + 1}. {name} - {rounds} Rounds"
                draw_text(screen, text, font, WHITE, WIDTH // 2, y_offset)
                y_offset += 40
        else:
            draw_text(screen, "Nenhum recorde salvo.", font, WHITE, WIDTH // 2, 120)

        draw_text(screen, "Pressione ESC para voltar", font, WHITE, WIDTH // 2, HEIGHT - 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Volta ao menu principal

def menu():
    """Tela inicial do menu."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RPG Game - Menu")
    
    # Carregar imagem de fundo
    menu_background_path = os.path.join(os.path.dirname(__file__), "assets", "menu.png")
    if os.path.exists(menu_background_path):
        menu_background = pygame.image.load(menu_background_path).convert()
    else:
        menu_background = pygame.Surface((WIDTH, HEIGHT))
        menu_background.fill(BLACK)  # Fundo preto caso a imagem não seja encontrada

    # Definir fontes e cores
    font = pygame.font.SysFont("arial", 36)

    # Definir botões
    button_start = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 80, 200, 50)
    button_records = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    button_exit = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50)

    running = True
    while running:
        screen.blit(menu_background, (0, 0))  # Exibe a imagem de fundo

        # Desenhar botões
        pygame.draw.rect(screen, (50, 50, 50), button_start)
        pygame.draw.rect(screen, (50, 50, 50), button_records)
        pygame.draw.rect(screen, (50, 50, 50), button_exit)

        # Adicionar textos aos botões
        draw_text(screen, "Iniciar Jogo", font, WHITE, WIDTH // 2, HEIGHT // 2 - 55)
        draw_text(screen, "Recordes", font, WHITE, WIDTH // 2, HEIGHT // 2 + 25)
        draw_text(screen, "Sair", font, WHITE, WIDTH // 2, HEIGHT // 2 + 105)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_start.collidepoint(mouse_pos):
                    running = False  # Sai do menu e inicia o jogo
                elif button_records.collidepoint(mouse_pos):
                    show_records(screen)  # Exibe os recordes
                elif button_exit.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()  # Fecha o jogo

    return True  # Retorna True para iniciar o jogoimport pygame
import sys
import os
from settings import WIDTH, HEIGHT, WHITE, BLACK

RECORDS_FILE = "records.txt"

def draw_text(screen, text, font, color, x, y):
    """Desenha texto na tela."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def save_record(player_name, rounds_survived):
    """Salva o recorde do jogador no arquivo records.txt"""
    if player_name.strip():  # Apenas salva se o jogador inserir um nome válido
        with open(RECORDS_FILE, "a") as file:
            file.write(f"{player_name},{rounds_survived}\n")

def load_records():
    """Carrega os recordes salvos e os ordena do maior para o menor"""
    if not os.path.exists(RECORDS_FILE):
        return []
    
    with open(RECORDS_FILE, "r") as file:
        records = [line.strip().split(",") for line in file.readlines()]
    
    records = [(name, int(rounds)) for name, rounds in records]
    records.sort(key=lambda x: x[1], reverse=True)  # Ordena pelo maior número de rounds
    return records

def show_records(screen):
    """Exibe a tela de recordes com fundo `background1.png`"""
    running = True
    font = pygame.font.SysFont("arial", 30)
    records = load_records()

    # Carregar imagem de fundo para os recordes
    records_background_path = os.path.join(os.path.dirname(__file__), "assets", "background1.png")
    if os.path.exists(records_background_path):
        records_background = pygame.image.load(records_background_path).convert()
    else:
        records_background = pygame.Surface((WIDTH, HEIGHT))
        records_background.fill(BLACK)  # Fundo preto caso a imagem não seja encontrada
    
    while running:
        screen.blit(records_background, (0, 0))  # Exibe o fundo personalizado

        draw_text(screen, "🏆 Recordes", font, WHITE, WIDTH // 2, 50)

        y_offset = 120
        if records:
            for idx, (name, rounds) in enumerate(records[:10]):  # Mostra os 10 melhores
                text = f"{idx + 1}. {name} - {rounds} Rounds"
                draw_text(screen, text, font, WHITE, WIDTH // 2, y_offset)
                y_offset += 40
        else:
            draw_text(screen, "Nenhum recorde salvo.", font, WHITE, WIDTH // 2, 120)

        draw_text(screen, "Pressione ESC para voltar", font, WHITE, WIDTH // 2, HEIGHT - 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Volta ao menu principal

def menu():
    """Tela inicial do menu."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RPG Game - Menu")
    
    # Carregar imagem de fundo para o menu
    menu_background_path = os.path.join(os.path.dirname(__file__), "assets", "menu.png")
    if os.path.exists(menu_background_path):
        menu_background = pygame.image.load(menu_background_path).convert()
    else:
        menu_background = pygame.Surface((WIDTH, HEIGHT))
        menu_background.fill(BLACK)  # Fundo preto caso a imagem não seja encontrada

    # Definir fontes e cores
    font = pygame.font.SysFont("arial", 36)

    # Definir botões
    button_start = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 80, 200, 50)
    button_records = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    button_exit = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50)

    running = True
    while running:
        screen.blit(menu_background, (0, 0))  # Exibe a imagem de fundo

        # Desenhar botões
        pygame.draw.rect(screen, (50, 50, 50), button_start)
        pygame.draw.rect(screen, (50, 50, 50), button_records)
        pygame.draw.rect(screen, (50, 50, 50), button_exit)

        # Adicionar textos aos botões
        draw_text(screen, "Iniciar Jogo", font, WHITE, WIDTH // 2, HEIGHT // 2 - 55)
        draw_text(screen, "Recordes", font, WHITE, WIDTH // 2, HEIGHT // 2 + 25)
        draw_text(screen, "Sair", font, WHITE, WIDTH // 2, HEIGHT // 2 + 105)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_start.collidepoint(mouse_pos):
                    running = False  # Sai do menu e inicia o jogo
                elif button_records.collidepoint(mouse_pos):
                    show_records(screen)  # Exibe os recordes com fundo `background1.png`
                elif button_exit.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()  # Fecha o jogo

    return True  # Retorna True para iniciar o jogo

