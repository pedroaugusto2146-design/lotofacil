import re

caminho = r'C:\Users\coimbra\Downloads\lotofacil\simony_app_v2.py'
with open(caminho, 'r', encoding='utf-8') as f:
    conteudo = f.read()

novo_heatmap = '''
    st.markdown("---")
    st.subheader("🔥 Mapa de Calor do Volante (1 a 25)")
    
    max_f = max(frequencia.values())
    min_f = min(frequencia.values())
    
    heatmap_html = '<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 450px; margin-bottom: 30px;">'
    for i in range(1, 26):
        qtd = frequencia.get(i, 0)
        # Calcula opacidade de 0.2 a 1.0 (brilho verde neon)
        if max_f == min_f:
            opacidade = 0.5
        else:
            opacidade = 0.15 + 0.85 * ((qtd - min_f) / (max_f - min_f))
        
        # Borda grossa nos top 15
        top_15 = [n for n, c in frequencia.most_common(15)]
        borda = "solid 2px #00ff00" if i in top_15 else "solid 1px #004400"
        
        heatmap_html += f\'\'\'
        <div style="background-color: rgba(0, 255, 0, {opacidade:.2f}); 
                    border: {borda}; border-radius: 8px; 
                    padding: 10px; text-align: center; color: white;
                    box-shadow: 0 0 10px rgba(0, 255, 0, {(opacidade/2):.2f});">
            <b style="font-size: 20px;">{i:02d}</b><br>
            <span style="font-size: 11px; opacity: 0.9;">{qtd}x</span>
        </div>
        \'\'\'
    heatmap_html += '</div>'
    
    st.markdown(heatmap_html, unsafe_allow_html=True)
'''

# Expressão regular para achar onde injetar
conteudo_novo = re.sub(
    r'st\.subheader\([^)]*Mapa de Calor[^)]*\).*?st\.code\([^)]*\)', 
    novo_heatmap.strip(), 
    conteudo, 
    flags=re.DOTALL
)

with open(caminho, 'w', encoding='utf-8') as f:
    f.write(conteudo_novo)
