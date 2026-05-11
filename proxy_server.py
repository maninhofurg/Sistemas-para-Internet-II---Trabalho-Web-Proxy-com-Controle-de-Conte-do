import json
import datetime
from flask import Flask, request
import requests

app = Flask(__name__)

# Função auxiliar para salvar logs em log.txt
def salvar_log(url, acao):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] URL: {url} | Ação: {acao}\n"
    with open("log.txt", "a") as f:
        f.write(log_entry)

@app.route('/<path:url_alvo>')
def proxy(url_alvo):
    # Garante que a URL alvo tenha o protocolo
    if not url_alvo.startswith('http'):
        url_alvo = 'http://' + url_alvo

    try:
        # 1. Carregar lista de Bloqueados
        with open('blocked.json', 'r') as f:
            config_bloqueio = json.load(f)
        
        # Verificar se a URL contém algum domínio bloqueado
        for site in config_bloqueio.get('bloqueados', []):
            if site in url_alvo:
                salvar_log(url_alvo, "BLOQUEADO")
                return """
                    <html>
                        <body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
                            <h1 style="color: red;">ACESSO BLOQUEADO</h1>
                            <p>O domínio solicitado está na lista negra do Proxy SI II.</p>
                            <hr>
                            <small>Servidor Proxy de Alessandro - Engenharia de Computação FURG</small>
                        </body>
                    </html>
                """, 403

        # 2. Modo Transparente (Buscar conteúdo na Internet)
        # O proxy age como cliente aqui usando a biblioteca requests
        resposta_real = requests.get(url_alvo)
        conteudo = resposta_real.text
        
        # 3. Filtro de Conteúdo (Substituição de palavras)
        with open('words.json', 'r') as f:
            substituicoes = json.load(f)
        
        alterado = False
        for original, substituta in substituicoes.items():
            # Verifica se a palavra existe no conteúdo (case-insensitive)
            if original.lower() in conteudo.lower():
                # Faz a substituição real
                conteudo = conteudo.replace(original, substituta)
                alterado = True
        
        acao = "FILTRADO" if alterado else "PERMITIDO"
        salvar_log(url_alvo, acao)
        
        return conteudo

    except json.JSONDecodeError:
        erro_msg = "ERRO: Falha ao ler arquivos de configuração (JSON inválido)"
        salvar_log(url_alvo, erro_msg)
        return erro_msg, 500
    except Exception as e:
        erro_msg = f"ERRO: {str(e)}"
        salvar_log(url_alvo, erro_msg)
        return erro_msg, 500

if __name__ == '__main__':
    # Roda na porta 5000 conforme especificado no trabalho
    app.run(host='0.0.0.0', port=5000)