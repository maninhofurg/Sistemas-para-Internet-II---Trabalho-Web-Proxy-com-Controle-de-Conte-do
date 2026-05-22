# Web Proxy com Controle de Conteúdo
**Disciplina:** Sistemas para Internet II (2026/1)  
**Professor:** Dr. André Prisco Vargas  
**Estudante:** Alessandro Goldas da Cruz - 166600
**Estudante:** Lucas de Gesu - 162668

## 1. Descrição do Projeto
Este projeto consiste na implementação de um **Web Proxy** didático desenvolvido em Python. O servidor atua como um intermediário entre um cliente e a Internet, processando requisições HTTP e aplicando regras de segurança e filtragem baseadas em ficheiros de configuração JSON.

### Funcionalidades Implementadas:
* **Modo Transparente:** Repasse de conteúdo original para sites que não possuem restrições.
* **Bloqueio de Sites:** Interceção de domínios listados em `blocked.json`, retornando uma página HTML personalizada com status **403 Forbidden**.
* **Filtro de Conteúdo:** Substituição dinâmica de termos baseada no dicionário `words.json`.
* **Log de Acessos:** Registo automático de data, hora, URL e ação executada no ficheiro `log.txt`.

## 2. Tecnologias e Arquitetura
* **Backend (Proxy):** Framework **Flask** para gestão de rotas e interceção.
* **Comunicação Externa:** Biblioteca `requests` para buscar conteúdo nos servidores de origem.
* **Cliente de Teste:** Implementado via **Sockets TCP** puros para demonstrar a montagem manual de cabeçalhos HTTP.


## 3. Estrutura do Repositório
* `proxy_server.py`: Código principal do servidor proxy.
* `cliente.py`: Script de testes automatizados.
* `blocked.json`: Lista de domínios bloqueados.
* `words.json`: Regras de substituição de palavras.
* `log.txt`: Histórico de requisições.

## 4. Como Executar
1. Instale as dependências: `pip install flask requests`
2. Inicie o servidor: `python3 proxy_server.py`
3. Execute os testes: `python3 cliente.py`

## 5. Fundamentação Técnica: Limitações do HTTPS
Este proxy opera na camada de aplicação para o protocolo HTTP. O filtro de conteúdo e o bloqueio detalhado por URL **não funcionam com tráfego HTTPS**.
**Justificativa:** O HTTPS utiliza criptografia SSL/TLS ponta-a-ponta. Como o proxy não possui as chaves privadas do servidor de destino, ele não consegue inspecionar ou modificar o corpo da resposta sem quebrar a cadeia de confiança do certificado digital (gerando erros de segurança).

## 6. Transparência no uso de IA
O desenvolvimento contou com o auxílio da IA **Gemini (Google)** para:
* [cite_start]Estruturar o laço de repetição no script de cliente[cite: 310].
* Refinar a lógica de substituição de termos no filtro.
* [cite_start]Organizar a documentação técnica e formatar este README[cite: 312].
* [cite_start]Validar conceitos de Sockets TCP e códigos de status HTTP[cite: 313].

---
**Status do Projeto:** Finalizado e Validado.