# settings.py

# 📏 Configurações da Tela
WIDTH = 1024
HEIGHT = 768
FPS = 60  # Frames por segundo

# 🎨 Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# 🏃 Configurações do Jogador
PLAYER_SPEED = 5
PLAYER_HEALTH = 100
PLAYER_MAX_HEALTH = 100
PLAYER_MANA = 50
PLAYER_MAX_MANA = 50
PLAYER_ATTACK_COOLDOWN = 500  # milissegundos
PLAYER_DEFENSE_DURATION = 2  # Tempo de defesa em segundos ao pressionar "Q"
PLAYER_DEFENSE_REDUCTION = 0.5  # Reduz dano pela metade durante a defesa
PLAYER_DAMAGE = 20  # Dano base do jogador
PLAYER_SPECIAL_DAMAGE = 50  # Dano do ataque especial
PLAYER_SPECIAL_COOLDOWN = 3000  # Tempo de recarga do ataque especial (ms)
PLAYER_MANA_COST = 30  # Custo de mana para ataque especial
PLAYER_XP_TO_NEXT_LEVEL = 100  # XP necessário para subir de nível
PLAYER_HEALTH_REGEN = 5  # HP regenerado a cada subida de nível
PLAYER_MANA_REGEN = 10  # Mana regenerada a cada subida de nível

# 😈 Configurações do Inimigo
ENEMY_SPEED = 2
ENEMY_HEALTH = 50
ENEMY_DAMAGE = 10
ENEMY_ATTACK_COOLDOWN = 1000  # milissegundos
ENEMY_DROP_CHANCE = 0.3  # 30% de chance de dropar um item ao morrer
ENEMY_FREEZE_DURATION = 1500  # Inimigo fica congelado por 1.5 segundos ao tomar dano

# 🔥 Configurações do Round
ROUND_ENEMY_INCREMENT = 1  # A cada round, aumenta a quantidade de inimigos
ROUND_NPC_INTERVAL = 3  # NPCs aparecem a cada 3 rounds
ROUND_DELAY = 1000  # Tempo de espera antes de iniciar um novo round (ms)

# 🎁 Configurações de Itens
ITEM_DROP_RATE = 6  # Um item cai a cada 6 inimigos mortos
SUPER_HEALTH_DROP_CHANCE = 0.3  # 30% de chance de dropar a Super Health Potion
ITEM_EFFECT_DURATION = 10  # Duração de efeitos especiais (segundos)
ITEM_TYPES = ["Health Potion", "Mana Potion", "Gold Coin"]  # Tipos de itens

# 📜 Configurações de NPCs
NPC_SCALE_HEIGHT = 200  # Altura fixa dos NPCs (mantém a proporção)
NPC_DIALOGUE_DELAY = 1000  # Delay entre falas do NPC (ms)
NPC_INTERACTION_DISTANCE = 100  # Distância mínima para interagir com NPCs

# 🔊 Música e Som
MUSIC_VOLUME = 0.1  # Volume da música de fundo (0.0 a 1.0)
SFX_VOLUME = 0.2  # Volume dos efeitos sonoros (ataque, dano, etc.)

# 🏆 Configurações do Jogo
FONT_NAME = 'arial'
GAME_OVER_DELAY = 2000  # Delay antes de voltar ao menu após Game Over (ms)
