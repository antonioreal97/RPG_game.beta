# RPG_game.beta
RPG Game in Python
Um protótipo inspirado em Diablo 3 feito em Python usando Pygame, com movimentação, IA de inimigos, ataques, inventário e integração com banco de dados SQLite.

📌 Índice
Visão Geral
Funcionalidades
Tecnologias Usadas
Estrutura do Projeto
Como Executar
Capturas de Tela
Próximos Passos
🎯 Visão Geral
Este projeto simula um RPG de ação no estilo Diablo, com:

Movimentação do jogador com controles W, A, S, D
Ataques básicos (SPACE)
Inimigos que perseguem o jogador
Sistema de inventário
Banco de dados SQLite para gerenciamento de itens
⚔️ Funcionalidades
✔️ Personagem principal movimentável
✔️ Inimigos com IA simples (seguem o jogador)
✔️ Ataques corpo a corpo (com cooldown)
✔️ Inventário para armazenar itens
✔️ Banco de dados SQLite para registrar itens
✔️ Interface HUD com HP, Mana e Inventário

🛠 Tecnologias Usadas
Python 3.11
Pygame 2.6.1 (para gráficos e jogabilidade)
SQLite3 (para armazenar os itens do jogo)
📂 Estrutura do Projeto
plaintext
Copiar
Editar
diablo3_clone/
├── assets/                 # Imagens do jogo
│   ├── background.png
│   ├── enemy.png
│   ├── item.png
│   ├── player.png
│   ├── player1.png
│   ├── player2.png
├── enemy.py                # Classe dos inimigos
├── inventory.py            # Sistema de inventário
├── inventory_db.py         # Banco de dados dos itens
├── item.py                 # Definição dos itens coletáveis
├── level.py                # Gerenciamento do mapa/nível
├── main.py                 # Arquivo principal do jogo
├── player.py               # Classe do jogador
└── settings.py             # Configurações globais do jogo
▶️ Como Executar
1️⃣ Clone o repositório
sh
Copiar
Editar
git clone https://github.com/seuusuario/diablo3-clone.git
cd diablo3-clone
2️⃣ Instale as dependências
Certifique-se de que tem o Python instalado e instale o Pygame:

sh
Copiar
Editar
pip install pygame
3️⃣ Execute o jogo
sh
Copiar
Editar
python main.py
🖼 Capturas de Tela


🚀 Próximos Passos
🔹 Adicionar animações ao jogador e inimigos
🔹 Melhorar IA dos inimigos (patrulha, ataques)
🔹 Criar diferentes tipos de itens e armas
🔹 Implementar um sistema de progressão (XP e níveis)
🔹 Melhorar o sistema de colisão e física

📜 Licença
Este projeto é open-source e pode ser utilizado para aprendizado.