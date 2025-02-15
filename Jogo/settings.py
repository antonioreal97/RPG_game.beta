# settings.py

# ----------------------
# Display Settings
# ----------------------
WIDTH = 1024
HEIGHT = 768
FPS = 60  # Frames por segundo

# ----------------------
# Map Settings
# ----------------------
# Dimensões do mapa baseadas no arquivo large_background.png (1920x1080)
MAP_WIDTH = 1920
MAP_HEIGHT = 1080

# ----------------------
# Zoom Settings
# ----------------------
ZOOM_FACTOR = 1.0  # 1.0 = Sem zoom, >1.0 = Zoom In, <1.0 = Zoom Out

# ----------------------
# Color Definitions (RGB)
# ----------------------
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY   = (128, 128, 128)

# ----------------------
# Player Settings
# ----------------------
PLAYER_SPEED = 5
PLAYER_HEALTH = 100
PLAYER_MAX_HEALTH = 1000
PLAYER_MANA = 50
PLAYER_MAX_MANA = 300
PLAYER_ATTACK_COOLDOWN = 100       # milissegundos
PLAYER_DEFENSE_DURATION = 2          # segundos (ao pressionar "Q")
PLAYER_DEFENSE_REDUCTION = 0.5       # Reduz dano pela metade durante a defesa
PLAYER_DAMAGE = 25                   # Dano base do jogador
PLAYER_SPECIAL_DAMAGE = 65           # Dano do ataque especial
PLAYER_SPECIAL_COOLDOWN = 3000       # Tempo de recarga do ataque especial (ms)
PLAYER_MANA_COST = 10                # Custo de mana para ataque especial
PLAYER_XP_TO_NEXT_LEVEL = 100        # XP necessário para subir de nível
PLAYER_HEALTH_REGEN = 7              # HP regenerado a cada subida de nível
PLAYER_MANA_REGEN = 15               # Mana regenerada a cada subida de nível

# ----------------------
# Enemy Settings
# ----------------------
ENEMY_SPEED = 2
ENEMY_HEALTH = 50
ENEMY_DAMAGE = 7
ENEMY_ATTACK_COOLDOWN = 1000       # milissegundos
ENEMY_DROP_CHANCE = 0.3            # 30% de chance de dropar um item ao morrer
ENEMY_FREEZE_DURATION = 1500       # milissegundos que o inimigo fica congelado ao tomar dano

# ----------------------
# Round Settings
# ----------------------
ROUND_ENEMY_INCREMENT = 1          # Incrementa a quantidade de inimigos a cada round
ROUND_NPC_INTERVAL = 5             # NPCs aparecem a cada 3 rounds
ROUND_DELAY = 3000                 # Tempo de espera antes de iniciar um novo round (ms)

# ----------------------
# Item Settings
# ----------------------
ITEM_DROP_RATE = 6               # Um item cai a cada 6 inimigos mortos
SUPER_HEALTH_DROP_CHANCE = 0.3   # 30% de chance de dropar a Super Health Potion
ITEM_EFFECT_DURATION = 15        # Duração de efeitos especiais (segundos)
ITEM_TYPES = ["Health Potion", "Mana Potion", "Gold Coin", "Super Health Potion"]

# ----------------------
# NPC Settings
# ----------------------
NPC_SCALE_HEIGHT = 200           # Altura fixa dos NPCs (mantém a proporção)
NPC_DIALOGUE_DELAY = 2000        # Delay entre as falas dos NPCs (ms)
NPC_INTERACTION_DISTANCE = 100   # Distância mínima para interagir com NPCs

# ----------------------
# Audio Settings
# ----------------------
MUSIC_VOLUME = 0.1               # Volume da música de fundo (0.0 a 1.0)
SFX_VOLUME = 0.2                 # Volume dos efeitos sonoros (ataque, dano, etc.)

# ----------------------
# General Game Settings
# ----------------------
FONT_NAME = 'arial'
GAME_OVER_DELAY = 3000           # Delay antes de voltar ao menu após Game Over (ms)
