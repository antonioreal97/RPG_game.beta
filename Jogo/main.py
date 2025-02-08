import os
import pygame
import sys
from settings import *
from player import Player
from level import Level
import inventory_db
from menu import menu, save_record  # Importando o menu e função para salvar recordes

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
                    return name.strip()  # Retorna o nome sem espaços extras
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]  # Apaga um caractere
                else:
                    name += event.unicode  # Adiciona a tecla pressionada ao nome

    return None

def main():
    """Loop principal do jogo"""

    # Exibe o menu antes de iniciar
    if not menu():
        return  # Sai do jogo se o usuário escolher sair

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RPG Game - Prototype")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)

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
        npc_group = pygame.sprite.Group()  # Adicionando grupo de NPCs

        # Criação do jogador
        player = Player((WIDTH // 2, HEIGHT // 2))
        all_sprites.add(player)

        # Criação do nível (controle de inimigos, itens e NPCs)
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
                    elif event.key == pygame.K_f:  # Ataque especial
                        player.special_attack(enemies_group)
                    elif event.key == pygame.K_x:  # Interação com NPCs
                        level.handle_npc_interaction(keys)  # 🔥 Corrigido para passar 'keys'
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

            # Atualiza apenas se o NPC não estiver interagindo
            if not level.npc_active:
                player.update(keys)
                enemies_group.update(player)
                items_group.update()
                level.update()

            npc_group.update()  # Atualiza NPCs

            # Verifica se o jogador morreu
            if player.health <= 0:
                player_name = get_player_name(screen, font)
                if player_name:  # Só salva o recorde se o jogador digitou um nome
                    save_record(player_name, level.round_number)
                print("🔄 Voltando ao menu...")
                return main()

            # Verifica se o jogador coletou algum item
            collected_items = pygame.sprite.spritecollide(player, items_group, True)
            for item in collected_items:
                item.apply_effect(player)  # Aplica o efeito do item

            # Renderização
            screen.blit(backgrounds[current_arena], (0, 0))
            all_sprites.draw(screen)
            items_group.draw(screen)
            npc_group.draw(screen)  # Desenha os NPCs

            # Desenha a caixa de diálogo do NPC se ele estiver interagindo
            if level.current_npc and level.dialogue_active:
                level.current_npc.draw_dialogue_box(screen, font)

            # Desenha barras de vida dos inimigos
            for enemy in enemies_group:
                enemy.draw_health_bar(screen)

            draw_hud(screen, player, font, level)
            pygame.display.flip()

if __name__ == "__main__":
    main()
