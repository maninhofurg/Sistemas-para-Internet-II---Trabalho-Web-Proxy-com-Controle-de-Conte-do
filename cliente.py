# Nome do arquivo: cliente.py
import socket

def testar_proxy(url_alvo):
    HOST = '127.0.0.1'
    PORTA = 5000 
    
    print(f"\n>>> TESTANDO ACESSO A: {url_alvo}")
    
    try:
        # 1. Criando o Socket TCP
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.settimeout(5) # Timeout de 5 segundos para não travar
        cliente.connect((HOST, PORTA))

        # 2. Montando a requisição HTTP manualmente
        requisicao = (
            f"GET /{url_alvo} HTTP/1.1\r\n"
            f"Host: {HOST}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        # 3. Enviar
        cliente.sendall(requisicao.encode())

        # 4. Receber a resposta
        resposta = b""
        while True:
            dados = cliente.recv(4096)
            if not dados: break
            resposta += dados
        
        # Exibe apenas o início da resposta para não inundar o terminal
        resultado = resposta.decode(errors='ignore')
        print("--- RESPOSTA RECEBIDA ---")
        print(resultado[:500] + "...") # Mostra os primeiros 500 caracteres
        
        cliente.close()
    except Exception as e:
        print(f"Erro ao conectar no proxy: {e}")

# --- LISTA DE TESTES ---
sites_para_testar = [
    "http://www.facebook.com",    # Deve ser BLOQUEADO
    "http://www.uol.com.br",      # Deve ser BLOQUEADO
    "http://www.example.com",     # Deve ser PERMITIDO e FILTRADO
    "http://www.google.com"       # Deve ser PERMITIDO (Modo Transparente)
]

# --- LAÇO FOR ---
for site in sites_para_testar:
    testar_proxy(site)
    print("-" * 50)