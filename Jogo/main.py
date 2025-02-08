import os
import pygame
import sys
from settings import *
from player import Player
from level import Level
import inventory_db
from menu import menu  # Importando o menu inicial

def draw_hud(screen, player, font, level):
    """Desenha a interface do jogador (HP, Mana, XP, Nível, Round e Inventário)."""
    health_text = font.render(f'HP: {player.health}/{player.max_health}', True, WHITE)
    mana_text = font.render(f'Mana: {player.mana}/{player.max_mana}', True, WHITE)
    xp_text = font.render(f'XP: {player.xp}/{player.xp_to_next_level}', True, WHITE)
    level_text = font.render(f'Level: {player.level}', True, WHITE)
    round_text = font.render(f'Round: {level.round_number}', True, WHITE)

    screen.blit(health_text, (10, 10))
    screen.blit(mana_text, (10, 40))
    screen.blit(xp_text, (10, 70))
    screen.blit(level_text, (10, 100))
    screen.blit(round_text, (10, 130))

    # Exibir inventário na HUD
    inventory_text = font.render("Inventário:", True, WHITE)
    screen.blit(inventory_text, (10, 160))
    y_offset = 190
    for item_name, details in player.inventory.items.items():
        item_text = font.render(f"- {item_name} (x{details['quantity']})", True, WHITE)
        screen.blit(item_text, (10, y_offset))
        y_offset += 30

def play_music():
    """Toca a música de fundo."""
    music_path = os.path.join(os.path.dirname(__file__), "assets", "intro.mp3")
    if os.path.exists(music_path):
        pygame.mixer.init()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.1)  # Ajusta o volume (0.0 a 1.0)
        pygame.mixer.music.play(-1)  # Reproduz em loop infinito
    else:
        print("⚠️ Arquivo intro.mp3 não encontrado. Música não será reproduzida.")

def main():
    """Loop principal do jogo"""

    # Exibe o menu antes de iniciar
    if not menu():
        return  # Sai do jogo se o usuário escolher sair

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RPG Game - Prototype")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(FONT_NAME, 24)

    # Inicializa o banco de dados
    inventory_db.create_tables()

    # Carrega os backgrounds para alternar entre arenas
    backgrounds = [
        pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "background.png")).convert(),
        pygame.image.load(os.path.join(os.path.dirname(__file__), "assets", "background1.png")).convert()
    ]
    current_arena = 0  # Começa na primeira arena

    # Inicia a música apenas se ainda não estiver tocando
    if not pygame.mixer.get_init() or not pygame.mixer.music.get_busy():
        play_music()

    while True:
        # Grupos de sprites
        all_sprites = pygame.sprite.Group()
        enemies_group = pygame.sprite.Group()
        items_group = pygame.sprite.Group()

        # Criação do jogador
        player = Player((WIDTH // 2, HEIGHT // 2))
        all_sprites.add(player)

        # Criação do nível (controle de inimigos e itens)
        level = Level(player, all_sprites, enemies_group, items_group)

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
                    elif event.key == pygame.K_f:  # Ataque especial
                        player.special_attack(enemies_group)
                    elif event.key == pygame.K_i:
                        player.inventory.list_inventory()
                    elif event.key == pygame.K_h:
                        player.use_item("Health Potion")
                    elif event.key == pygame.K_m:
                        player.use_item("Mana Potion")
                    elif event.key == pygame.K_r:  # Reinicia o jogo ao morrer
                        print("🔄 Retornando ao menu...")
                        return main()  # Retorna ao menu inicial
                elif event.type == pygame.USEREVENT:
                    if event.dict.get("action") == "restart":
                        print("🔄 Reiniciando jogo...")
                        return main()  # Retorna ao menu inicial
                    elif event.dict.get("action") == "change_arena":
                        current_arena = event.dict.get("arena", 0)
                        print(f"🌍 Arena alterada para {current_arena}")

            player.update(keys)
            enemies_group.update(player)
            items_group.update()  # 🔥 Atualiza os itens corretamente
            level.update()

            # Verifica se o jogador coletou algum item
            collected_items = pygame.sprite.spritecollide(player, items_group, True)
            for item in collected_items:
                item.apply_effect(player)  # Aplica o efeito do item

            # Renderização
            screen.blit(backgrounds[current_arena], (0, 0))
            all_sprites.draw(screen)
            items_group.draw(screen)  # 🔥 Garante que os itens aparecem no mapa

            # Desenha barras de vida dos inimigos
            for enemy in enemies_group:
                enemy.draw_health_bar(screen)

            draw_hud(screen, player, font, level)
            pygame.display.flip()

if __name__ == "__main__":
    main()
