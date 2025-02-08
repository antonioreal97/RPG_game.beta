# settings.py

# Configurações da tela
WIDTH = 1024
HEIGHT = 768
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
YELLOW = (255, 255, 0)

# Configurações do jogador
PLAYER_SPEED = 5
PLAYER_HEALTH = 100
PLAYER_MANA = 50
PLAYER_ATTACK_COOLDOWN = 500  # milissegundos
PLAYER_DEFENSE_DURATION = 2  # Tempo de defesa em segundos ao pressionar "Q"
PLAYER_DEFENSE_REDUCTION = 0.5  # Reduz dano pela metade durante a defesa

# Configurações do inimigo
ENEMY_SPEED = 2
ENEMY_HEALTH = 50
ENEMY_ATTACK_COOLDOWN = 1000  # milissegundos
ENEMY_DROP_CHANCE = 0.3  # 30% de chance de dropar um item ao morrer

# Configurações de itens
ITEM_DROP_RATE = 6  # Um item cai a cada 6 inimigos mortos
SUPER_HEALTH_DROP_CHANCE = 0.5  # 50% de chance de dropar a Super Health Potion

# Fonte do jogo
FONT_NAME = 'arial'

# Música e Som
MUSIC_VOLUME = 0.1  # Volume da música (0.0 a 1.0)
SFX_VOLUME = 0.2  # Volume dos efeitos sonoros (ataque, dano, etc.)

