import socket

# Configurações do alvo[cite: 2]
IP_SERVIDOR = '127.0.0.1'  # Ou o seu IP na rede FURG
PORTA = 8080

# 1. Criação do socket TCP[cite: 2, 6]
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Conexão
cliente.connect((IP_SERVIDOR, PORTA))

# 3. Montagem manual da requisição HTTP
# Note a linha em branco entre o cabeçalho e o corpo (conforme slide da aula)
requisicao = (
    "GET / HTTP/1.1\r\n"
    f"Host: {IP_SERVIDOR}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

# 4. Envio e Recebimento[cite: 2]
cliente.send(requisicao.encode('utf-8'))
resposta = cliente.recv(4096)

print("--- Resposta do Servidor ---")
print(resposta.decode('utf-8'))

cliente.close()