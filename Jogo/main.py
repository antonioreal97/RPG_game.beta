import os
import pygame
import sys
from settings import *
from player import Player
from level import Level
import inventory_db
from menu import menu, save_record
from camera import Camera

def draw_hud(screen, player, font, level):
    """Desenha a interface do jogador (HP, Mana, XP, Nível, Round e Inventário)."""
    health_text = font.render(f'HP: {player.health}/{player.max_health}', True, WHITE)
    mana_text = font.render(f'Mana: {player.mana}/{player.max_mana}', True, WHITE)
    xp_text = font.render(f'XP: {player.xp}/{player.xp_to_next_level}', True, WHITE)
    level_text = font.render(f'Level: {player.level}', True, RED)
    round_text = font.render(f'Round: {level.round_number}', True, WHITE)

    screen.blit(health_text, (10, 10))
    screen.blit(mana_text, (10, 40))
    screen.blit(xp_text, (10, 70))
    screen.blit(level_text, (10, 100))
    screen.blit(round_text, (10, 130))

    # Exibe o inventário na HUD
    inventory_text = font.render("Inventário:", True, WHITE)
    screen.blit(inventory_text, (10, 160))
    y_offset = 190
    for item_name, details in player.inventory.items.items():
        item_text = font.render(f"- {item_name} (x{details['quantity']})", True, WHITE)
        screen.blit(item_text, (10, y_offset))
        y_offset += 30

def draw_player_health_bar(screen, player):
    """Desenha a barra de vida do jogador no canto superior direito da tela com cores dinâmicas."""
    bar_width = 200
    bar_height = 20
    x = WIDTH - bar_width - 20  # Posiciona no canto superior direito
    y = 20  # Distância do topo

    # Calcula a largura da barra de vida proporcional à vida do jogador
    health_ratio = player.health / player.max_health
    fill_width = int(bar_width * health_ratio)

    # Define a cor com base na porcentagem de vida
    if health_ratio > 0.5:
        health_color = (0, 0, 255)  # Azul (100% até 51%)
    elif health_ratio > 0.3:
        health_color = (128, 0, 128)  # Roxo (50% até 31%)
    else:
        health_color = (255, 0, 0)  # Vermelho (30% ou menos)

    # Desenha o contorno e a barra de vida com a cor correspondente
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill_width, bar_height)

    pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)  # Contorno branco
    pygame.draw.rect(screen, health_color, fill_rect)  # Barra de vida colorida

def play_music():
    """Toca a música de fundo."""
    music_path = os.path.join(os.path.dirname(__file__), "assets", "intro.mp3")
    if os.path.exists(music_path):
        pygame.mixer.init()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)
    else:
        print("⚠️ Arquivo intro.mp3 não encontrado. Música não será reproduzida.")

def get_player_name(screen, font):
    """Exibe uma caixa de entrada para o jogador inserir seu nome ao morrer."""
    name = ""
    input_active = True

    while input_active:
        screen.fill(BLACK)
        prompt_text = font.render("Digite seu nome para salvar o recorde:", True, WHITE)
        screen.blit(prompt_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))

        name_text = font.render(name, True, WHITE)
        screen.blit(name_text, (WIDTH // 2 - 100, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

    return None

def main():
    """Loop principal do jogo"""

    # Exibe o menu antes de iniciar
    if not menu():
        return  

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RPG Game - Prototype")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)

    inventory_db.create_sample_items()  

    # Carrega o background do mapa grande
    background_path = os.path.join(os.path.dirname(__file__), "assets", "large_background.png")
    if os.path.exists(background_path):
        background = pygame.image.load(background_path).convert()
        background = pygame.transform.scale(background, (MAP_WIDTH, MAP_HEIGHT))
    else:
        background = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        background.fill(GRAY)

    # Inicializa a câmera
    camera = Camera(MAP_WIDTH, MAP_HEIGHT)

    if not pygame.mixer.get_init() or not pygame.mixer.music.get_busy():
        play_music()

    while True:
        # Cria os grupos de sprites
        all_sprites = pygame.sprite.Group()
        enemies_group = pygame.sprite.Group()
        items_group = pygame.sprite.Group()
        npc_group = pygame.sprite.Group()

        # Cria o jogador (posicionado no centro do mapa)
        player = Player((MAP_WIDTH // 2, MAP_HEIGHT // 2))
        all_sprites.add(player)

        # Cria o nível (controle de inimigos, itens e NPCs)
        level = Level(player, all_sprites, enemies_group, items_group, npc_group)

        running = True
        while running:
            clock.tick(FPS)
            keys = pygame.key.get_pressed()

            # Processamento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.attack(enemies_group)
                    elif event.key == pygame.K_f:
                        player.special_attack(enemies_group)
                    elif event.key == pygame.K_x:
                        level.handle_npc_interaction(keys)
                    elif event.key == pygame.K_i:
                        player.inventory.list_inventory()
                    elif event.key == pygame.K_h:
                        player.use_item("Health Potion")
                    elif event.key == pygame.K_m:
                        player.use_item("Mana Potion")
                    elif event.key == pygame.K_r:
                        print("🔄 Retornando ao menu...")
                        return main()
                elif event.type == pygame.USEREVENT:
                    if event.dict.get("action") == "restart":
                        print("🔄 Reiniciando jogo...")
                        return main()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Ajusta o zoom com o scroll do mouse:
                    # event.button == 4 -> scroll up (aumenta zoom)
                    # event.button == 5 -> scroll down (diminui zoom)
                    if event.button == 4:
                        camera.zoom_factor = min(2.0, camera.zoom_factor + 0.1)
                    elif event.button == 5:
                        camera.zoom_factor = max(0.5, camera.zoom_factor - 0.1)

            # Atualiza apenas se o NPC não estiver interagindo
            if not level.npc_active:
                player.update(keys)
                enemies_group.update(player)
                items_group.update()
                level.update()

            npc_group.update()

            # Verifica se o jogador morreu
            if player.health <= 0:
                player_name = get_player_name(screen, font)
                if player_name:
                    save_record(player_name, level.round_number)
                print("🔄 Voltando ao menu...")
                return main()

            # Verifica se o jogador coletou algum item
            collected_items = pygame.sprite.spritecollide(player, items_group, True)
            for item in collected_items:
                item.apply_effect(player)

            # Atualiza a câmera para centralizar o jogador (offset calculado sem zoom)
            camera.update(player)

            screen.fill(BLACK)

            # Aplica o zoom ao background e extrai a parte visível
            zoomed_background = camera.apply_zoom_to_background(background)
            screen.blit(zoomed_background, (0, 0))

            # Desenha os sprites com o zoom aplicado
            for sprite in all_sprites:
                zoomed_rect = camera.apply(sprite)
                zoomed_sprite = pygame.transform.scale(sprite.image, (zoomed_rect.width, zoomed_rect.height))
                screen.blit(zoomed_sprite, zoomed_rect)
            for sprite in items_group:
                zoomed_rect = camera.apply(sprite)
                zoomed_sprite = pygame.transform.scale(sprite.image, (zoomed_rect.width, zoomed_rect.height))
                screen.blit(zoomed_sprite, zoomed_rect)
            for sprite in npc_group:
                zoomed_rect = camera.apply(sprite)
                zoomed_sprite = pygame.transform.scale(sprite.image, (zoomed_rect.width, zoomed_rect.height))
                screen.blit(zoomed_sprite, zoomed_rect)

            # Desenha a caixa de diálogo do NPC se ele estiver interagindo
            if level.current_npc and level.dialogue_active:
                level.current_npc.draw_dialogue_box(screen, font)

            # Desenha as barras de vida dos inimigos usando a posição "zoomada"
            for enemy in enemies_group:
                zoomed_rect = camera.apply(enemy)
                bar_width = int(50 * camera.zoom_factor)
                bar_height = int(5 * camera.zoom_factor)
                fill = (enemy.health / enemy.max_health) * bar_width
                outline_rect = pygame.Rect(zoomed_rect.centerx - bar_width // 2, zoomed_rect.top - int(10 * camera.zoom_factor), bar_width, bar_height)
                fill_rect = pygame.Rect(zoomed_rect.centerx - bar_width // 2, zoomed_rect.top - int(10 * camera.zoom_factor), fill, bar_height)
                pygame.draw.rect(screen, (255, 255, 255), outline_rect)
                pygame.draw.rect(screen, (255, 0, 0), fill_rect)
                pygame.draw.rect(screen, (0, 0, 0), outline_rect, 1)

            draw_hud(screen, player, font, level)
            draw_player_health_bar(screen, player)  
            pygame.display.flip()

if __name__ == "__main__":
    main()
