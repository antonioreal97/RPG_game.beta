import pygame
import random
from enemy import Enemy
from item import Item
from npcs import spawn_npc
from settings import WIDTH, HEIGHT, NPC_INTERACTION_DISTANCE

class Level:
    def __init__(self, player, all_sprites, enemies_group, items_group, npc_group):
        self.player = player
        self.all_sprites = all_sprites
        self.enemies_group = enemies_group
        self.items_group = items_group
        self.npc_group = npc_group
        self.enemies_killed = 0
        self.round_number = 1
        self.enemy_spawn_rate = 3
        self.round_active = True
        self.npc_active = False
        self.current_npc = None
        self.dialogue_active = False
        self.pending_enemies = []  # Armazena inimigos para spawn após interação
        self.create_level()

    def create_level(self):
        """Cria os inimigos iniciais do nível se não houver NPC ativo."""
        if not self.npc_active:  
            for _ in range(self.enemy_spawn_rate):
                self.spawn_enemy()

    def update(self):
        """Atualiza o nível, verifica mortes de inimigos e gerencia a progressão dos rounds."""
        if self.dialogue_active:  
            return  # Se houver diálogo ativo, pausa apenas os inimigos

        enemies_to_remove = []

        # Verifica quais inimigos foram mortos
        for enemy in self.enemies_group:
            if enemy.health <= 0:
                self.player.gain_xp(enemy.xp_reward)
                self.enemies_killed += 1
                enemies_to_remove.append(enemy)

        # Remove os inimigos mortos
        for enemy in enemies_to_remove:
            enemy.kill()
            self.enemies_group.remove(enemy)

        # Gera um item a cada 6 inimigos mortos
        if self.enemies_killed > 0 and self.enemies_killed % 6 == 0:
            self.spawn_item()

        if len(self.enemies_group) == 0 and self.round_active and not self.npc_active:
            self.next_round()

    def spawn_enemy(self):
        """Gera um inimigo aleatório no mapa se não houver NPC ativo."""
        if self.npc_active:  
            return  

        pos = self.get_random_spawn_position()
        enemy = Enemy(pos, self.round_number, self.all_sprites, self.items_group)
        enemy.xp_reward = random.randint(15, 30)

        self.all_sprites.add(enemy)
        self.enemies_group.add(enemy)
        print(f"👿 Novo inimigo spawnado! Vida: {enemy.health}, XP: {enemy.xp_reward}")

    def spawn_item(self):
        """Gera um item aleatório no mapa."""
        pos = self.get_random_spawn_position()
        item_name = "Super Health Potion" if random.random() < 0.5 else random.choice(["Health Potion", "Mana Potion", "Gold Coin"])
        item = Item(pos, item_name)

        # Adiciona o item ao jogo
        self.all_sprites.add(item)
        self.items_group.add(item)
        print(f"🆕 Item Spawnado: {item_name} na posição {pos}")

    def spawn_npc(self):
        """Gera um NPC a cada 3 rodadas e pausa os inimigos enquanto ele estiver no mapa."""
        if self.round_number % 3 == 0:
            npc = spawn_npc()
            self.all_sprites.add(npc)
            self.npc_group.add(npc)
            self.current_npc = npc
            self.npc_active = True  
            print(f"🧙 NPC '{npc.name}' apareceu no mapa!")

            # Remove todos os inimigos temporariamente
            for enemy in self.enemies_group:
                self.all_sprites.remove(enemy)
            self.enemies_group.empty()

    def handle_npc_interaction(self, keys):
        """Gerencia a interação do jogador com o NPC ao pressionar 'X'."""
        if self.current_npc:
            self.current_npc.check_proximity(self.player)

            if self.current_npc.player_near and keys[pygame.K_x]:  
                if not self.dialogue_active:
                    self.dialogue_active = True
                    self.current_npc.interact()
                else:
                    self.current_npc.advance_dialogue()

                if not self.current_npc.interacting:
                    self.end_npc_interaction()

    def end_npc_interaction(self):
        """Finaliza a interação com o NPC e libera os inimigos novamente."""
        if self.current_npc:
            print(f"✅ Diálogo com {self.current_npc.name} concluído! Inimigos podem reaparecer.")
            self.npc_group.remove(self.current_npc)
            self.all_sprites.remove(self.current_npc)
            self.current_npc = None
            self.dialogue_active = False  
            self.npc_active = False  

            # Libera os inimigos pendentes
            for enemy in self.pending_enemies:
                self.all_sprites.add(enemy)
                self.enemies_group.add(enemy)
                print(f"👿 {enemy.type} apareceu após o NPC! Vida: {enemy.health}")

            self.pending_enemies = []  

            # Se não houver inimigos, inicia o próximo round
            if len(self.enemies_group) == 0:
                self.next_round()

    def next_round(self):
        """Inicia um novo round se o NPC não estiver interagindo."""
        if self.dialogue_active or self.npc_active:
            return

        self.round_active = False
        self.round_number += 1
        self.enemy_spawn_rate += 1

        print(f"🔥 Novo Round {self.round_number}! Agora teremos {self.enemy_spawn_rate} inimigos!")

        pygame.time.delay(1000)  

        self.spawn_npc()

        if not self.npc_active:
            for _ in range(self.enemy_spawn_rate):
                self.spawn_enemy()

        self.round_active = True

    def get_random_spawn_position(self):
        """Gera uma posição aleatória no mapa sem sobrepor o jogador."""
        while True:
            pos = (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
            if abs(pos[0] - self.player.rect.x) > 100 and abs(pos[1] - self.player.rect.y) > 100:
                return pos
