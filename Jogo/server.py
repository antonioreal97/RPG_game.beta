import socket
import threading
import pickle

# Configurações do servidor
# Para aceitar conexões de qualquer IP, use '0.0.0.0'. 
# Se você estiver apenas testando localmente, pode usar '127.0.0.1'.
SERVER_IP = '127.0.0.1'
PORT = 5555

# Lista para armazenar as conexões dos clientes
clients = []

def handle_client(conn, addr):
    """
    Lida com a comunicação com um cliente.
    Recebe dados, desserializa e faz broadcast para os outros clientes.
    """
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            data = conn.recv(4096)
            if not data:
                # Se não receber dados, o cliente desconectou
                print(f"[DISCONNECTED] {addr} disconnected.")
                break
            # Desserializa os dados recebidos (estado do jogo ou input do jogador)
            game_state = pickle.loads(data)
            print(f"[RECEIVED] Data from {addr}: {game_state}")
            # Envia os dados para todos os outros clientes
            broadcast(game_state, sender=conn)
        except Exception as e:
            print(f"[ERROR] Error handling client {addr}: {e}")
            break
    # Remove o cliente da lista e fecha a conexão
    if conn in clients:
        clients.remove(conn)
    conn.close()

def broadcast(game_state, sender=None):
    """
    Serializa e envia o game_state para todos os clientes conectados,
    exceto aquele que enviou a mensagem (sender).
    """
    try:
        data = pickle.dumps(game_state)
    except Exception as e:
        print(f"[ERROR] Failed to serialize game_state: {e}")
        return

    for client in clients:
        if client != sender:
            try:
                client.send(data)
            except Exception as e:
                print(f"[ERROR] Failed to send data to a client: {e}")

def start_server():
    """
    Inicializa o servidor, escuta conexões e cria uma thread para cada novo cliente.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, PORT))
    server.listen()
    print(f"[STARTED] Server started on {SERVER_IP}:{PORT}")
    
    while True:
        try:
            conn, addr = server.accept()
            clients.append(conn)
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True  # Permite que o programa feche mesmo se as threads estiverem rodando
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {len(clients)}")
        except Exception as e:
            print(f"[ERROR] Error accepting connections: {e}")

if __name__ == "__main__":
    start_server()
