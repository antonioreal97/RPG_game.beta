import socket
import threading
import pickle

def connect_to_server(server_ip, port):
    """
    Cria um socket de cliente e tenta se conectar ao servidor usando
    o IP e a porta informados.
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, port))
        print(f"[CONNECTED] Conectado ao servidor {server_ip}:{port}")
    except Exception as e:
        print(f"[ERROR] Erro ao conectar ao servidor: {e}")
        exit()
    return client

def listen_for_updates(client):
    """
    Função executada em uma thread separada para receber atualizações do servidor.
    Os dados recebidos são desserializados com pickle e impressos no console.
    """
    while True:
        try:
            data = client.recv(4096)
            if data:
                game_state = pickle.loads(data)
                print("[UPDATE RECEIVED]", game_state)
            else:
                print("[DISCONNECTED] Conexão encerrada pelo servidor.")
                break
        except Exception as e:
            print(f"[ERROR] Erro ao receber dados: {e}")
            break

def send_input(client, input_data):
    """
    Serializa (usando pickle) e envia os dados de input (por exemplo, comandos do jogador)
    para o servidor.
    """
    try:
        data = pickle.dumps(input_data)
        client.send(data)
    except Exception as e:
        print(f"[ERROR] Erro ao enviar dados: {e}")

def main():
    # Solicita ao usuário o IP do servidor e a porta (ex.: os valores fornecidos pelo ngrok)
    server_ip = input("Digite o endereço IP do servidor (ex: 0.tcp.sa.ngrok.io): ").strip()
    port_str = input("Digite a porta do servidor (ex: 15067): ").strip()
    try:
        port = int(port_str)
    except ValueError:
        print("Porta inválida.")
        return

    client = connect_to_server(server_ip, port)

    # Inicia a thread para receber atualizações do servidor
    listener_thread = threading.Thread(target=listen_for_updates, args=(client,), daemon=True)
    listener_thread.start()

    # Loop principal para enviar comandos do usuário
    while True:
        user_input = input("Digite um comando (ou 'sair' para encerrar): ")
        if user_input.lower() == "sair":
            print("[EXIT] Encerrando o cliente...")
            break
        send_input(client, {"action": user_input})
    
    client.close()

if __name__ == "__main__":
    main()
