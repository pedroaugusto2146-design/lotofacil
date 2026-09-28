import streamlit as st
import json
import random
import time
import requests
import urllib3
from collections import Counter

urllib3.disable_warnings() # Esconde avisos da Caixa

# Filtros Matemáticos
PRIMOS = {2, 3, 5, 7, 11, 13, 17, 19, 23}
FIBONACCI = {1, 2, 3, 5, 8, 13, 21}
MOLDURA = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}

st.set_page_config(page_title="Simony OS - Lotofácil", page_icon="💻", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; font-family: 'Courier New', Courier, monospace; }
    h1, h2, h3, p, div { color: #00ff00 !important; }
    .bilhete-box { background-color: #111111; border: 1px solid #00ff00; padding: 15px; border-radius: 8px; margin-bottom: 10px; font-size: 22px; text-align: center; letter-spacing: 3px; box-shadow: 0 0 10px #00ff0044; }
    [data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #00ff00; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 SIMONY OS | V3.1 (Auto-Sync)")
st.markdown("### 💻 Módulo de Extração e Engenharia Reversa de Loterias")

st.sidebar.header("⚙️ PAINEL DE COMANDO")
qtd_jogos = st.sidebar.slider("Quantos bilhetes forjar?", 1, 20, 10)
gerar_btn = st.sidebar.button("🚀 INICIAR FORÇA BRUTA")

st.sidebar.markdown("---")
# ==============================================================
# NOVO BOTÃO DE AUTOMAÇÃO E INTELIGÊNCIA DE SYNC
# ==============================================================
sync_btn = st.sidebar.button("🔄 SINCRONIZAR COM A CAIXA")

if sync_btn:
    with st.sidebar.status("Conectando aos servidores da Caixa..."):
        try:
            with open('lotofacil_dados.json', 'r', encoding='utf-8') as f:
                dados_locais = json.load(f)
            ultimo_salvo = dados_locais[0]['concurso']

            headers = {"User-Agent": "Mozilla/5.0"}
            url_base = "https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil/"
            req = requests.get(url_base, headers=headers, verify=False)
            ultimo_oficial = req.json()['numero']

            if ultimo_oficial > ultimo_salvo:
                st.write(f"Baixando atualizações: {ultimo_salvo + 1} até {ultimo_oficial}...")
                novos_dados = []
                for i in range(ultimo_oficial, ultimo_salvo, -1):
                    res = requests.get(f"{url_base}{i}", headers=headers, verify=False)
                    if res.status_code == 200:
                        d = res.json()
                        novos_dados.append({
                            "concurso": i,
                            "data": d['dataApuracao'],
                            "dezenas": d['listaDezenas']
                        })
                    time.sleep(0.2)
                
                # Junta os jogos novos com os jogos velhos e salva!
                dados_atualizados = novos_dados + dados_locais
                with open('lotofacil_dados.json', 'w', encoding='utf-8') as f:
                    json.dump(dados_atualizados, f, ensure_ascii=False, indent=4)
                    
                st.success("✅ Base Sincronizada com sucesso!")
                time.sleep(1)
                st.rerun() # Recarrega a página automaticamente
            else:
                st.success("✅ O Banco de Dados já está 100% atualizado!")
        except Exception as e:
            st.error(f"Erro na invasão: {e}")

st.sidebar.markdown("---")
st.sidebar.markdown("🛡️ **Filtros Ativos:**\n\n✔️ Ímpares/Pares\n\n✔️ Números Primos\n\n✔️ Seq. Fibonacci\n\n✔️ Moldura (Borda)\n\n✔️ Repetidas\n\n✔️ Limite de Soma")

try:
    with open('lotofacil_dados.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)
        
    ultimo_concurso = [int(n) for n in dados[0]['dezenas']]
    todas_as_dezenas = []
    for concurso in dados:
        todas_as_dezenas.extend([int(n) for n in concurso['dezenas']])

    frequencia = Counter(todas_as_dezenas)
    numeros_quentes = [num for num, cont in frequencia.most_common(21)]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Banco de Dados", f"{len(dados)} Sorteios")
    col2.metric("Último Concurso", f"Nº {dados[0]['concurso']}")
    col3.metric("Data da Última Coleta", f"{dados[0]['data']}")
    
    st.markdown("---")
    st.subheader("🔥 Mapa de Calor (Top 21 Números)")
    st.code(str(sorted(numeros_quentes)), language="python")
    
except FileNotFoundError:
    st.error("Erro: Arquivo lotofacil_dados.json não encontrado.")
    st.stop()

if gerar_btn:
    st.markdown("### 🛡️ Executando Quebra Criptográfica...")
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1)
        
    with st.spinner("Peneirando estatísticas em milhões de possibilidades..."):
        jogos_gerados = []
        tentativas_totais = 0
        
        while len(jogos_gerados) < qtd_jogos:
            tentativas_totais += 1
            jogo = random.sample(numeros_quentes, 15)
            
            impares = len([n for n in jogo if n % 2 != 0])
            primos = len([n for n in jogo if n in PRIMOS])
            fibo = len([n for n in jogo if n in FIBONACCI])
            moldura = len([n for n in jogo if n in MOLDURA])
            repetidas = len([n for n in jogo if n in ultimo_concurso])
            soma = sum(jogo)
            
            if not (impares == 7 or impares == 8): continue
            if not (4 <= primos <= 6): continue
            if not (3 <= fibo <= 5): continue
            if not (9 <= moldura <= 11): continue
            if not (8 <= repetidas <= 10): continue
            if not (180 <= soma <= 210): continue
            
            jogo.sort()
            if jogo not in jogos_gerados:
                jogos_gerados.append(jogo)

    st.success(f"Acesso Concedido. {tentativas_totais} combinações 'lixo' descartadas com sucesso.")
    st.markdown("### 🎯 ARSENAL DE BILHETES (PADRÃO OURO)")
    for idx, jogo in enumerate(jogos_gerados, 1):
        formatado = " - ".join([str(n).zfill(2) for n in jogo])
        st.markdown(f'<div class="bilhete-box">🎫 JOGO {idx:02d} | <b>{formatado}</b></div>', unsafe_allow_html=True)