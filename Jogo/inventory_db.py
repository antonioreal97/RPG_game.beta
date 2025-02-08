import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Obtém os dados de conexão do MongoDB do .env
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Conectar ao MongoDB
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # Timeout de 5 segundos
db = client[DB_NAME]
items_collection = db[COLLECTION_NAME]

# Testar conexão antes de executar qualquer operação
try:
    client.server_info()  # Teste de conexão
    print("✅ Conectado ao MongoDB!")
except Exception as e:
    print(f"❌ Erro ao conectar ao MongoDB: {e}")
    exit()

def create_sample_items():
    """Adiciona itens ao banco de dados se a coleção estiver vazia."""
    if items_collection.count_documents({}) == 0:
        items_collection.insert_many([
            {"name": "Health Potion", "description": "Restaura 50 HP", "rarity": "Common", "value": 10},
            {"name": "Mana Potion", "description": "Restaura 30 MP", "rarity": "Common", "value": 12},
            {"name": "Gold Coin", "description": "Uma moeda valiosa", "rarity": "Uncommon", "value": 50},
        ])
        print("🆕 Itens padrão adicionados ao banco de dados!")

create_sample_items()
