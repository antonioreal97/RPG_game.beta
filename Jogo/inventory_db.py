# inventory_db.py
import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), "game.db")

def get_connection():
    """Retorna uma conexão com o banco de dados."""
    return sqlite3.connect(DATABASE)

def create_tables():
    """Cria a tabela de itens no banco de dados, caso não exista."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            rarity TEXT,
            value INTEGER
        )
    """)
    conn.commit()
    conn.close()

def insert_item(name, description, rarity, value):
    """Insere um item no banco de dados."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO items (name, description, rarity, value)
        VALUES (?, ?, ?, ?)
    """, (name, description, rarity, value))
    conn.commit()
    conn.close()

def get_all_items():
    """Retorna todos os itens cadastrados no banco de dados."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, description, rarity, value FROM items")
    items = cur.fetchall()
    conn.close()
    return items
