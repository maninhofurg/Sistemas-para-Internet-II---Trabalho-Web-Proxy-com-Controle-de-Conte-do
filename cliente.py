import socket
import sys

def testar_proxy(url_alvo):
    HOST = '127.0.0.1'
    PORTA = 5000 
    
    # Remove o prefixo http:// para enviar de forma limpa ao Flask
    url_limpa = url_alvo.replace("http://", "")
    
    print(f"\n>>> TESTANDO ACESSO A: {url_alvo}")
    
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.settimeout(5)
        cliente.connect((HOST, PORTA))

        # Envia apenas a URL limpa após o GET /
        requisicao = f"GET /{url_limpa} HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n"

        cliente.sendall(requisicao.encode())

        resposta = b""
        while True:
            dados = cliente.recv(4096)
            if not dados: break
            resposta += dados
        
        print("--- RESPOSTA RECEBIDA ---")
        # Imprime os primeiros caracteres da resposta para não poluir o terminal
        print(resposta.decode(errors='ignore')[:500] + "...\n")
        print("-" * 50)
        cliente.close()
        
    except Exception as e:
        print(f"Erro ao conectar com {url_alvo}: {e}\n")
        print("-" * 50)

# --- MENU INTERATIVO ---
if __name__ == "__main__":
    print("="*50)
    print("  CLIENTE DE TESTE TCP - WEB PROXY SI II")
    print("  Digite 'sair' a qualquer momento para encerrar.")
    print("="*50)

    while True:
        # Pede para o usuário digitar o site
        entrada_site = input("\nDigite a URL para testar (ex: http://www.example.com): ").strip()
        
        # Condição de parada
        if entrada_site.lower() == 'sair':
            print("Encerrando o cliente de testes. Até logo!")
            sys.exit(0)
            
        # Ignora se o usuário apertar Enter sem digitar nada
        if not entrada_site:
            continue
            
        # Executa o teste com o site digitado
        testar_proxy(entrada_site)
