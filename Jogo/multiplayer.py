import pygame
import socket
import threading
import pickle
import sys
import os
import time

from player import Player
from level import Level
from multienemy import MultiEnemyManager
from settings import WIDTH, HEIGHT, FPS, MAP_WIDTH, MAP_HEIGHT, WHITE, RED, BLACK, MUSIC_VOLUME
from camera import Camera

# Configurações do servidor
SERVER_IP_DEFAULT = '127.0.0.1'
PORT = 5555
COLOR_REMOTE = (255, 0, 0)

def start_local_server():
    """Inicia o servidor local executando server.py em uma thread separada."""
    try:
        import server
        threading.Thread(target=server.start_server, daemon=True).start()
        print("[SERVER] Servidor local iniciado.")
    except Exception as e:
        print(f"[ERROR] Não foi possível iniciar o servidor local: {e}")

def play_intro_music():
    """
    Toca a música intro.mp3 se estiver disponível em 'assets/intro.mp3'.
    """
    music_path = os.path.join(os.path.dirname(__file__), "assets", "intro.mp3")
    if os.path.exists(music_path):
        # Inicializa mixer (se ainda não estiver inicializado)
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        # Carrega e reproduz a música
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)  # Ex.: 0.1 no settings
        pygame.mixer.music.play(-1)  # -1 = loop infinito
        print("🎵 Tocando intro.mp3 no modo Multiplayer.")
    else:
        print("⚠️ Arquivo intro.mp3 não encontrado. Música não será reproduzida no multiplayer.")

class MultiplayerGame:
    def __init__(self, screen):
        """
        Gera a tela principal para as entradas iniciais
        (se o jogador quer ser host, IP do servidor, nome do player).
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.server_ip = None
        self.player_id = None
        self.running = True

    def draw_input_screen(self, prompt):
        """
        Desenha uma tela de entrada para coletar dados do usuário (host ou IP, nome do player).
        """
        input_text = ""
        font = pygame.font.SysFont("arial", 30)

        while True:
            self.screen.fill(BLACK)
            prompt_text = font.render(prompt, True, WHITE)
            self.screen.blit(prompt_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))

            input_surface = font.render(input_text, True, WHITE)
            self.screen.blit(input_surface, (WIDTH // 2 - 100, HEIGHT // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return input_text.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

    def setup_connection(self):
        """Pergunta se o jogador é host e obtém o IP/nome do jogador."""
        choice = self.draw_input_screen("Você deseja ser o host? (s/n)")
        if choice.lower() == 's':
            start_local_server()
            self.server_ip = SERVER_IP_DEFAULT
        else:
            self.server_ip = self.draw_input_screen("Digite o IP do servidor:")

        self.player_id = self.draw_input_screen("Digite seu nome:")

    def start_game(self):
        """
        Cria a instância da sessão multiplayer e inicia o loop de jogo.
        Também toca a música de fundo intro.mp3, se existir.
        """
        play_intro_music()  # <-- Toca a música antes de entrar no loop do game
        game_instance = MultiplayerSession(self.server_ip, PORT, self.player_id, self.screen)
        game_instance.run()

class MultiplayerSession:
    def __init__(self, server_ip, port, player_id, screen):
        self.server_ip = server_ip
        self.port = port
        self.player_id = player_id
        self.screen = screen
        self.running = True

        # Inicializa o jogador local
        self.player = Player((MAP_WIDTH // 2, MAP_HEIGHT // 2))
        self.remote_players = {}  # Dicionário de jogadores remotos

        # Carrega o background do mapa
        background_path = os.path.join(os.path.dirname(__file__), "assets", "large_background.png")
        if os.path.exists(background_path):
            self.background = pygame.image.load(background_path).convert()
            self.background = pygame.transform.scale(self.background, (MAP_WIDTH, MAP_HEIGHT))
        else:
            self.background = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
            self.background.fill(BLACK)

        # Câmera
        self.camera = Camera(MAP_WIDTH, MAP_HEIGHT)

        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.items_group = pygame.sprite.Group()
        self.npc_group = pygame.sprite.Group()

        self.all_sprites.add(self.player)

        # Gerenciador de inimigos para multiplayer
        self.enemy_manager = MultiEnemyManager(self.all_sprites, self.enemies_group, self.items_group)

        # Inicializa o nível
        self.level = Level(self.player, self.all_sprites, self.enemies_group, self.items_group, self.npc_group)

        # Socket para comunicação com o servidor
        self.client = None
        self.connect_to_server()

    def connect_to_server(self):
        """Conecta ao servidor e envia as informações do jogador."""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.server_ip, self.port))
            print(f"[CONNECTED] Conectado ao servidor {self.server_ip}:{self.port}")
        except Exception as e:
            print(f"[ERROR] Erro ao conectar ao servidor: {e}")
            sys.exit()

        init_pos = {"x": self.player.rect.x, "y": self.player.rect.y}
        self.send_data({
            "action": "register",
            "player_id": self.player_id,
            "position": init_pos
        })

    def listen_for_updates(self):
        """Recebe atualizações do servidor e atualiza jogadores e inimigos."""
        while self.running:
            try:
                data = self.client.recv(4096)
                if data:
                    state = pickle.loads(data)
                    players = state.get("players", {})
                    enemies = state.get("enemies", {})

                    # Atualiza lista de jogadores remotos
                    for pid, pos in players.items():
                        if pid != self.player_id:
                            self.remote_players[pid] = pos

                    # Atualiza inimigos localmente (posições, HP, etc.)
                    self.enemy_manager.sync_enemies(enemies)
                else:
                    print("[DISCONNECTED] Conexão encerrada pelo servidor.")
                    self.running = False
                    break
            except Exception as e:
                print(f"[ERROR] Erro ao receber dados: {e}")
                self.running = False
                break

    def send_data(self, data):
        """Envia dados (posições, ações) para o servidor."""
        try:
            serialized_data = pickle.dumps(data)
            self.client.send(serialized_data)
        except Exception as e:
            print(f"[ERROR] Erro ao enviar dados: {e}")

    def process_events(self):
        """Captura e processa os eventos do jogador local."""
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # Envia posição atual
        pos = {"x": self.player.rect.x, "y": self.player.rect.y}
        self.send_data({"action": "move", "player_id": self.player_id, "position": pos})

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.attack(self.enemies_group)
                elif event.key == pygame.K_f:
                    self.player.special_attack(self.enemies_group)

    def draw_hud(self):
        """Desenha informações (HP, Mana, XP, Level, Round) do jogador local."""
        font = pygame.font.SysFont("arial", 24)
        texts = [
            f'HP: {self.player.health}/{self.player.max_health}',
            f'Mana: {self.player.mana}/{self.player.max_mana}',
            f'XP: {self.player.xp}/{self.player.xp_to_next_level}',
            f'Level: {self.player.level}',
            f'Round: {self.level.round_number}'
        ]
        y = 10
        for text in texts:
            self.screen.blit(font.render(text, True, WHITE), (10, y))
            y += 30

    def render(self):
        """Renderiza cenário, inimigos, jogadores e HUD."""
        self.camera.update(self.player)
        zoomed_background = self.camera.apply_zoom_to_background(self.background)
        self.screen.blit(zoomed_background, (0, 0))

        # Desenha inimigos
        for enemy in self.enemies_group:
            zoomed_rect = self.camera.apply(enemy)
            self.screen.blit(enemy.image, zoomed_rect)
            enemy.draw_health_bar(self.screen, zoomed_rect)

        # Desenha jogadores remotos
        for pid, pos in self.remote_players.items():
            # Converte coords do mundo => coords da tela
            zoomed_x = int((pos["x"] - self.camera.camera_rect.x) * self.camera.zoom_factor)
            zoomed_y = int((pos["y"] - self.camera.camera_rect.y) * self.camera.zoom_factor)
            pygame.draw.circle(self.screen, COLOR_REMOTE, (zoomed_x, zoomed_y), 20)

        # Desenha jogador local
        zoomed_rect = self.camera.apply(self.player)
        scaled_player = pygame.transform.scale(self.player.image, (zoomed_rect.width, zoomed_rect.height))
        self.screen.blit(scaled_player, zoomed_rect)

        self.draw_hud()
        pygame.display.flip()

    def run(self):
        """Loop principal do multiplayer."""
        listener_thread = threading.Thread(target=self.listen_for_updates, daemon=True)
        listener_thread.start()

        while self.running:
            self.process_events()
            # Atualiza inimigos localmente
            players_list = [self.player]
            self.enemy_manager.update(players_list)

            self.render()

        pygame.quit()
        self.client.close()
