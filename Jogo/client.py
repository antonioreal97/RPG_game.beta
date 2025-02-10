import socket
import threading
import pickle

# Configurações do servidor
# Para uso em ambiente de desenvolvimento local, mantenha '127.0.0.1'
# Para uso com ngrok, altere SERVER_IP e PORT para os valores retornados pelo comando "ngrok tcp 5555"
SERVER_IP = '0.tcp.ngrok.io'  # Exemplo: '0.tcp.ngrok.io' se estiver usando ngrok com túnel TCP
PORT = 13028              # Exemplo: 12345 se o ngrok retornar tcp://0.tcp.ngrok.io:12345

def connect_to_server():
    """
    Cria um socket de cliente e tenta se conectar ao servidor.
    Retorna o socket conectado.
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_IP, PORT))
        print(f"[CONNECTED] Conectado ao servidor {SERVER_IP}:{PORT}")
    except Exception as e:
        print(f"[ERROR] Erro ao conectar ao servidor: {e}")
        exit()
    return client

def listen_for_updates(client):
    """
    Função executada em uma thread separada para receber atualizações do servidor.
    Os dados recebidos são desserializados com pickle e podem ser usados para atualizar o estado do jogo.
    """
    while True:
        try:
            data = client.recv(4096)
            if data:
                game_state = pickle.loads(data)
                # Aqui você atualizaria o estado do jogo com as informações recebidas.
                # Por enquanto, vamos apenas imprimir o game_state.
                print("[UPDATE RECEIVED]", game_state)
            else:
                # Se não houver dados, significa que a conexão foi fechada.
                print("[DISCONNECTED] Conexão encerrada pelo servidor.")
                break
        except Exception as e:
            print(f"[ERROR] Erro ao receber dados: {e}")
            break

def send_input(client, input_data):
    """
    Serializa (usando pickle) e envia os dados de input (por exemplo, comandos do jogador) para o servidor.
    """
    try:
        data = pickle.dumps(input_data)
        client.send(data)
    except Exception as e:
        print(f"[ERROR] Erro ao enviar dados: {e}")

def main():
    client = connect_to_server()

    # Inicia a thread de recepção de atualizações do servidor
    listener_thread = threading.Thread(target=listen_for_updates, args=(client,), daemon=True)
    listener_thread.start()

    # Loop principal do cliente: aqui você pode integrar com o seu jogo (ex.: Pygame)
    # Neste exemplo, usamos o input do console para simular comandos do jogador.
    while True:
        user_input = input("Digite um comando (ou 'sair' para encerrar): ")
        if user_input.lower() == "sair":
            print("[EXIT] Encerrando o cliente...")
            break
        # Exemplo: envia um dicionário contendo o comando do jogador
        send_input(client, {"action": user_input})
    
    client.close()

if __name__ == "__main__":
    main()
