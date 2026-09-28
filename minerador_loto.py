import requests
import json
import time

def minerar_resultados():
    print("Iniciando invasão na API da Caixa...")
    
    # URL oficial da Caixa (pega o último concurso)
    url_base = "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil/"
    
    # Disfarce para o Firewall da Caixa achar que somos um navegador normal
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # 1. Pegar o último concurso para saber onde estamos
        req = requests.get(url_base, headers=headers, verify=False)
        ultimo_concurso = req.json()
        numero_atual = ultimo_concurso['numero']
        
        print(f"Alvo localizado! Último concurso: {numero_atual}")
        print("Iniciando extração dos últimos 10 concursos para calibração da IA...\n")

        base_de_dados = []

        # 2. Loop para baixar os últimos 10 jogos
        for i in range(numero_atual, 0, -1):
            url_concurso = f"{url_base}{i}"
            res = requests.get(url_concurso, headers=headers, verify=False)
            
            if res.status_code == 200:
                dados = res.json()
                dezenas = dados['listaDezenas']
                print(f"Concurso {i} extraído: {dezenas}")
                
                base_de_dados.append({
                    "concurso": i,
                    "data": dados['dataApuracao'],
                    "dezenas": dezenas
                })
            else:
                print(f"Erro ao extrair concurso {i}")
            
            # Dormir 1 segundo pra não alertar o servidor
            time.sleep(0.2)

        # 3. Salvar os dados (A gasolina da IA)
        with open('lotofacil_dados.json', 'w', encoding='utf-8') as f:
            json.dump(base_de_dados, f, ensure_ascii=False, indent=4)
            
        print("\nExtração concluída! Arquivo 'lotofacil_dados.json' gerado com sucesso.")
        print("A IA já tem o que comer.")

    except Exception as e:
        print(f"Erro na conexão: {e}")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings() # Esconde avisos de segurança de SSL da Caixa
    minerar_resultados()