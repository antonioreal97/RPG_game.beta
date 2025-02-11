import pygame
import sys
import os
from settings import WIDTH, HEIGHT, WHITE, BLACK

RECORDS_FILE = "records.txt"

def draw_text(screen, text, font, color, x, y):
    """Desenha texto na tela, centralizado na posição (x, y)."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def save_record(player_name, rounds_survived):
    """Salva o recorde do jogador no arquivo records.txt."""
    if player_name.strip():  # Apenas salva se o jogador inserir um nome válido
        with open(RECORDS_FILE, "a") as file:
            file.write(f"{player_name},{rounds_survived}\n")

def load_records():
    """Carrega os recordes salvos e os ordena do maior para o menor."""
    if not os.path.exists(RECORDS_FILE):
        return []
    
    with open(RECORDS_FILE, "r") as file:
        records = [line.strip().split(",") for line in file.readlines()]
    
    records = [(name, int(rounds)) for name, rounds in records]
    records.sort(key=lambda x: x[1], reverse=True)  # Ordena pelo maior número de rounds
    return records

def show_records(screen):
    """Exibe a tela de recordes com um fundo personalizado."""
    running = True
    font = pygame.font.SysFont("arial", 30)
    records = load_records()

    # Carrega imagem de fundo para os recordes
    records_background_path = os.path.join(os.path.dirname(__file__), "assets", "background1.png")
    if os.path.exists(records_background_path):
        records_background = pygame.image.load(records_background_path).convert()
        records_background = pygame.transform.scale(records_background, (WIDTH, HEIGHT))
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

def game_mode_menu(screen):
    """
    Exibe um sub-menu para o jogador escolher entre Singleplayer e Multiplayer,
    utilizando a imagem de fundo 'background.png'.
    Retorna uma string indicando o modo selecionado.
    """
    running = True
    font = pygame.font.SysFont("arial", 36)
    
    # Carrega a imagem de fundo para o sub-menu
    background_path = os.path.join(os.path.dirname(__file__), "assets", "background.png")
    if os.path.exists(background_path):
        background = pygame.image.load(background_path).convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    else:
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill((30, 30, 30))
    
    # Define os botões para os modos de jogo
    button_single = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    button_multi = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
    
    while running:
        screen.blit(background, (0, 0))
        draw_text(screen, "Escolha o Modo de Jogo", font, WHITE, WIDTH // 2, HEIGHT // 2 - 120)
        
        pygame.draw.rect(screen, (50, 50, 50), button_single)
        pygame.draw.rect(screen, (50, 50, 50), button_multi)
        
        draw_text(screen, "Singleplayer", font, WHITE, WIDTH // 2, HEIGHT // 2 - 25)
        draw_text(screen, "Multiplayer", font, WHITE, WIDTH // 2, HEIGHT // 2 + 45)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_single.collidepoint(mouse_pos):
                    return "singleplayer"
                elif button_multi.collidepoint(mouse_pos):
                    return "multiplayer"

def menu():
    """Exibe a tela principal do menu e retorna o modo de jogo selecionado (se Iniciar Jogo for escolhido)."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RPG Game - Menu")
    
    # Carrega a imagem de fundo para o menu (pode ser diferente se desejado)
    menu_background_path = os.path.join(os.path.dirname(__file__), "assets", "menu.png")
    if os.path.exists(menu_background_path):
        menu_background = pygame.image.load(menu_background_path).convert()
    else:
        menu_background = pygame.Surface((WIDTH, HEIGHT))
        menu_background.fill(BLACK)
    
    font = pygame.font.SysFont("arial", 36)

    # Define os botões do menu
    button_start = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 80, 200, 50)
    button_records = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    button_exit = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50)

    running = True
    mode = None  # Armazena o modo de jogo escolhido
    while running:
        screen.blit(menu_background, (0, 0))

        pygame.draw.rect(screen, (50, 50, 50), button_start)
        pygame.draw.rect(screen, (50, 50, 50), button_records)
        pygame.draw.rect(screen, (50, 50, 50), button_exit)

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
                    # Ao clicar em Iniciar Jogo, exibe o sub-menu de modos de jogo
                    mode = game_mode_menu(screen)
                    running = False
                elif button_records.collidepoint(mouse_pos):
                    show_records(screen)
                elif button_exit.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
    return mode

if __name__ == "__main__":
    selected_mode = menu()
    print(f"Modo de jogo selecionado: {selected_mode}")
    # Aqui você pode iniciar o jogo singleplayer ou multiplayer com base em selected_mode.
