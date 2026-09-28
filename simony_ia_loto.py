import json
import random
from collections import Counter

# Filtros Matemáticos da Lotofácil
PRIMOS = {2, 3, 5, 7, 11, 13, 17, 19, 23}
FIBONACCI = {1, 2, 3, 5, 8, 13, 21}
MOLDURA = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}

def simony_v3_analisador():
    print("Iniciando SIMONY V3 (O Motor Definitivo)...\n")
    
    try:
        with open('lotofacil_dados.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except FileNotFoundError:
        print("Arquivo JSON não encontrado! Rode o minerador primeiro.")
        return

    # 1. Analisar Último Concurso (Índice 0 é o mais recente baixado)
    ultimo_concurso = [int(n) for n in dados[0]['dezenas']]
    
    # 2. Analisar o Histórico de 1.000 jogos
    todas_as_dezenas = []
    for concurso in dados:
        todas_as_dezenas.extend([int(n) for n in concurso['dezenas']])

    frequencia = Counter(todas_as_dezenas)
    
    # Vamos pegar os 21 números mais quentes para a matemática ter espaço para rodar
    numeros_quentes = [num for num, cont in frequencia.most_common(21)]
    
    print(f"📌 Último Concurso Analisado: {sorted(ultimo_concurso)}")
    print(f"🔥 Base Quente (Histórico): {sorted(numeros_quentes)}")
    print("\nIniciando Força Bruta para encontrar 10 Jogos Padrão Ouro...\n")

    jogos_gerados = []
    tentativas_totais = 0

    while len(jogos_gerados) < 10:
        tentativas_totais += 1
        
        # Gera uma aposta a partir dos 21 números mais quentes
        jogo = random.sample(numeros_quentes, 15)
        
        # Conta a matemática do jogo
        impares = len([n for n in jogo if n % 2 != 0])
        primos = len([n for n in jogo if n in PRIMOS])
        fibo = len([n for n in jogo if n in FIBONACCI])
        moldura = len([n for n in jogo if n in MOLDURA])
        repetidas = len([n for n in jogo if n in ultimo_concurso])
        soma = sum(jogo)
        
        # ========================================================
        # O PAREDÃO: Só passa se obedecer TODAS as 6 regras
        # ========================================================
        if not (impares == 7 or impares == 8): continue
        if not (4 <= primos <= 6): continue
        if not (3 <= fibo <= 5): continue
        if not (9 <= moldura <= 11): continue
        if not (8 <= repetidas <= 10): continue
        if not (180 <= soma <= 210): continue
        
        # Se passou em todos os filtros, formata e salva o jogo
        jogo.sort()
        if jogo not in jogos_gerados:
            jogos_gerados.append(jogo)
            print(f"✅ Bilhete Ouro {len(jogos_gerados)} encontrado (após {tentativas_totais} tentativas totais)")

    print("\n==============================================")
    print("🧠 SIMONY SYSTEM V3 - ARSENAL DE 10 JOGOS")
    print("==============================================")
    for idx, jogo in enumerate(jogos_gerados, 1):
        formatado = [str(n).zfill(2) for n in jogo]
        print(f"Jogo {idx:02d}: {', '.join(formatado)}")
    print("==============================================\n")
    print(f"🛡️ Resumo do Processador:")
    print(f"A Simony gerou e deletou {tentativas_totais - 10} combinações estatisticamente 'lixo' em milissegundos até conseguir montar esses 10 bilhetes perfeitos.")

if __name__ == "__main__":
    simony_v3_analisador()