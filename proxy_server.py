import json
import datetime
import re
from flask import Flask, request, Response
import requests

app = Flask(__name__)

def salvar_log(url, acao):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] URL: {url} | Ação: {acao}\n"
    with open("log.txt", "a") as f:
        f.write(log_entry)

@app.route('/')
def index():
    return "<h1>Proxy SI II Online</h1><p>Use /http://site.com para testar.</p>"

@app.route('/<path:url_alvo>')
def proxy(url_alvo):
    # 1. Ignora requisições de favicon para manter o log limpo
    if "favicon.ico" in url_alvo:
        return "", 204

    # 2. Garante que a URL alvo tenha o protocolo
    if not url_alvo.startswith('http'):
        url_alvo = 'http://' + url_alvo

    try:
        # 3. Bloqueio de Sites
        with open('blocked.json', 'r') as f:
            config_bloqueio = json.load(f)
        
        for site in config_bloqueio.get('bloqueados', []):
            if site in url_alvo:
                salvar_log(url_alvo, "BLOQUEADO")
                return """
                    <html><body><h1 style="color: red;">ACESSO BLOQUEADO</h1>
                    <p>O domínio solicitado está na lista negra.</p></body></html>
                """, 403

        # 4. Requisição ao site original
        resposta_real = requests.get(url_alvo, timeout=10)
        conteudo_bruto = resposta_real.content
        content_type = resposta_real.headers.get('Content-Type', '')
        
        # 5. Se for HTML, aplica o Filtro e corrige o Visual
        if 'text/html' in content_type.lower():
            texto_html = resposta_real.text
            
            with open('words.json', 'r') as f:
                substituicoes = json.load(f)
            
            alterado = False
            # Filtro Case-Insensitive usando Regex
            for original, substituta in substituicoes.items():
                if re.search(re.escape(original), texto_html, re.IGNORECASE):
                    texto_html = re.sub(re.escape(original), substituta, texto_html, flags=re.IGNORECASE)
                    alterado = True
            
            # Injeta a tag <base> para o navegador achar o CSS e as Imagens originais
            base_tag = f'<base href="{resposta_real.url}">'
            texto_html = re.sub(r'<head>', f'<head>\n    {base_tag}\n', texto_html, flags=re.IGNORECASE)
            
            acao = "FILTRADO" if alterado else "PERMITIDO"
            salvar_log(url_alvo, acao)
            
            # Retorna o HTML formatado
            return Response(texto_html, content_type=content_type)
        
        else:
            # 6. Se for Imagem, CSS ou JS, apenas repassa (Modo Transparente absoluto)
            salvar_log(url_alvo, "PERMITIDO (Recurso)")
            return Response(conteudo_bruto, content_type=content_type)

    except Exception as e:
        erro_msg = f"ERRO: {str(e)}"
        salvar_log(url_alvo, erro_msg)
        return erro_msg, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
