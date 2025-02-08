import os
import pygame
import sys
from settings import *
from player import Player
from enemy import Enemy
import inventory_db

def draw_hud(screen, player, font):
    """Desenha a interface do jogador, incluindo vida e inventário."""
    health_text = font.render(f'HP: {player.health}', True, WHITE)
    mana_text = font.render(f'Mana: {player.mana}', True, WHITE)
    screen.blit(health_text, (10, 10))
    screen.blit(mana_text, (10, 40))

    inventory_text = font.render("Inventário:", True, WHITE)
    screen.blit(inventory_text, (10, 70))

    for i, item in enumerate(player.inventory.items):
        item_text = font.render(f"- {item.name} ({item.rarity})", True, WHITE)
        screen.blit(item_text, (10, 100 + i * 30))

def main():
    """Loop principal do jogo"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Diablo 3 - Prototype")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(FONT_NAME, 24)

    # Inicializa o banco de dados
    inventory_db.create_tables()

    # Carrega o background corretamente
    background_path = os.path.join(os.path.dirname(__file__), "assets", "background.png")
    background = pygame.image.load(background_path).convert()

    # Criação dos grupos de sprites
    all_sprites = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()

    # Criação do jogador
    player = Player((WIDTH // 2, HEIGHT // 2))
    all_sprites.add(player)

    # Criação dos inimigos
    enemy_positions = [(100, 100), (900, 200), (500, 600)]
    for pos in enemy_positions:
        enemy = Enemy(pos)
        all_sprites.add(enemy)
        enemies_group.add(enemy)

    running = True
    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.attack(enemies_group)

        # Atualização do jogador (corrigido para evitar erro de argumento)
        player.update(keys)

        # Atualização dos inimigos (agora recebe o jogador como referência)
        enemies_group.update(player)

        # Renderização
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        draw_hud(screen, player, font)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
