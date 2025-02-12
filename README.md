# RPG_game.beta
RPG Game in Python

# 🎮 RPG game (Python + Pygame)

![Game Screenshot](assets/large_background.png)

Um protótipo inspirado em *Diablo 3* feito em **Python** usando **Pygame**, com movimentação, IA de inimigos, ataques, inventário e integração com banco de dados MongoDB.

---

## 📌 Índice
- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Usadas](#tecnologias-usadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar](#como-executar)
- [Capturas de Tela](#capturas-de-tela)
- [Próximos Passos](#próximos-passos)

---

## 🎯 Visão Geral
Este projeto é um protótipo de um **RPG de ação**, semelhante a *Diablo*, com:
- **Movimentação do jogador** com controles `W, A, S, D`
- **Ataques básicos** (`SPACE`)
- **Ataque especial** (`F`)
- **Defesa de golpes** (`Q`)
- **Inventáriopara armazenar itens** (`I`)
- **Inimigos que perseguem o jogador**
- **Sistema de inventário**
- **Banco de dados MongoDB para gerenciamento de itens** ('Em breve...')

---

## ⚔️ Funcionalidades
✅ **Personagem principal movimentável**  
✅ **Inimigos com IA simples (seguem o jogador)**  
✅ **Ataques corpo a corpo (com cooldown)**  
✅ **Inventário para armazenar itens**  
✅ **Banco de dados MongoDB para registrar os itens**  
✅ **Interface HUD com HP, Mana e Inventário**  

---

## 🛠 Tecnologias Usadas
- **Python 3.11**
- **Pygame 2.6.1** (para gráficos e jogabilidade)
- **MongoDB** (para armazenar os itens do jogo)

---

## 💂🏻🛡️ Capturas de Tela

### 📌 Menu Inicial
![Tela Menu](prints/1-Tela_Menu.png)

### 🎮 Seleção de Modo de Jogo
![Game Mode](prints/2-Game_mode.png)

### 🔥 Gameplay
![Game Play](prints/3-Game_Play.png)

### 🧑‍🎒 Inventário
![Inventário](prints/4-Inventario.png)

### ☠️ Tela de Game Over
![Game Over](prints/5-Game_Over.png)

---

## 📂 Estrutura do Projeto
```plaintext
Jogo/
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
```

---

## ▶️ Como Executar

### 1️⃣ Clone o repositório
```sh
git clone https://github.com/antonioreal97/RPG_game.beta.git
cd diablo3-clone
```

### 2️⃣ Instale as dependências
Certifique-se de que tem o Python instalado e instale o Pygame:
```sh
pip install pygame
```

### 3️⃣ Execute o jogo
```sh
python main.py
```

