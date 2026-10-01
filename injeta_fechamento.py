import sys

caminho = r'C:\Users\coimbra\Downloads\lotofacil\simony_app_v2.py'
with open(caminho, 'r', encoding='utf-8') as f:
    conteudo = f.read()

# Certifica de que itertools está importado
if 'import itertools' not in conteudo:
    conteudo = conteudo.replace('import random', 'import random\nimport itertools')

# O cdigo a ser injetado no final
nova_funcao = '''
st.sidebar.markdown("---")
desdobramento_btn = st.sidebar.button("💎 DESDOBRAMENTO TOTAL (18 Dezenas)")
st.sidebar.caption("Gera 816 combinações possíveis das 18 dezenas mais quentes e aplica os Filtros Matemáticos para extrair os Jogos de Elite.")

if desdobramento_btn:
    st.markdown("### 💎 CALCULANDO MATRIZ DE DESDOBRAMENTO (18 -> 15)")
    with st.spinner("Desdobrando 816 combinações e aplicando filtros pesados..."):
        # Pega as 18 mais quentes
        as_18_mais = sorted(numeros_quentes[:18])
        st.info(f"Dezenas escolhidas para o fechamento: {as_18_mais}")
        
        # Gera todas as combinações matemáticas de 15 números dentre as 18
        todas_combinacoes = list(itertools.combinations(as_18_mais, 15))
        
        jogos_de_elite = []
        descartados = 0
        
        for jogo in todas_combinacoes:
            jogo = list(jogo)
            impares = len([n for n in jogo if n % 2 != 0])
            primos = len([n for n in jogo if n in PRIMOS])
            fibo = len([n for n in jogo if n in FIBONACCI])
            moldura = len([n for n in jogo if n in MOLDURA])
            repetidas = len([n for n in jogo if n in ultimo_concurso])
            soma = sum(jogo)
            
            # Passando na peneira de filtros
            if not (impares == 7 or impares == 8): 
                descartados += 1; continue
            if not (4 <= primos <= 6): 
                descartados += 1; continue
            if not (3 <= fibo <= 5): 
                descartados += 1; continue
            if not (9 <= moldura <= 11): 
                descartados += 1; continue
            if not (8 <= repetidas <= 10): 
                descartados += 1; continue
            if not (180 <= soma <= 210): 
                descartados += 1; continue
                
            jogos_de_elite.append(jogo)

    st.success(f"Fechamento Concluído! Das 816 combinações matemáticas possíveis, os filtros descartaram {descartados} jogos com baixa probabilidade.")
    
    if len(jogos_de_elite) > 0:
        st.markdown(f"### 🎯 ENCONTRADOS {len(jogos_de_elite)} JOGOS DE ELITE")
        for idx, jogo in enumerate(jogos_de_elite, 1):
            formatado = " - ".join([str(n).zfill(2) for n in jogo])
            st.markdown(f'<div class="bilhete-box" style="border-color: #ffd700; box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);">💎 ELITE {idx:02d} | <b>{formatado}</b></div>', unsafe_allow_html=True)
    else:
        st.warning("Os filtros foram tão rígidos que destruíram todos os 816 jogos da matriz! Tente relaxar um pouco as regras ou gerar a força bruta padrão.")
'''

# Evita duplicao caso execute mais de uma vez
if 'DESDOBRAMENTO TOTAL' not in conteudo:
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo + "\n" + nova_funcao)
    print("Sucesso")
else:
    print("J existe")
