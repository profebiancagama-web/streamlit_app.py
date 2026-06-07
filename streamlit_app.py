import streamlit as st
import random
import os

# --- CONFIGURAÇÃO DA TELA ---
st.set_page_config(page_title="Estacionamento das Cores", page_icon="🚌", layout="centered")

# =========================================================
# ✏️ CONFIGURAÇÃO DO NOME DO SEU FILHO (ATUALIZADO!)
NOME_DO_FILHO = "Yuri"
# =========================================================

# --- INICIALIZAÇÃO DO ESTADO DO JOGO ---
if "cor_atual" not in st.session_state:
    st.session_state.cor_atual = random.choice(["AZUL", "AMARELO"])

# --- LÓGICA DE VERIFICAÇÃO (Captura o clique do JavaScript) ---
parametros = st.query_params
if "clique" in parametros:
    cor_clicada = parametros["clique"]
    st.query_params.clear()
    
    if cor_clicada == st.session_state.cor_atual:
        st.markdown("<h1 style='text-align:center; font-size:60px; color:#10b981; font-family:Comic Sans MS;'>🌟 PARABÉNS! 🌟</h1>", unsafe_allow_html=True)
        st.balloons()
        st.session_state.cor_atual = random.choice(["AZUL", "AMARELO"])
        import time
        time.sleep(1.0)
        st.rerun()

# --- CORES E CONFIGURAÇÕES VISUAIS DA RODADA ---
if st.session_state.cor_atual == "AZUL":
    cor_codigo = "#1d4ed8"
    classe_nome = "color: #1d4ed8;"
else:
    cor_codigo = "#eab308"
    classe_nome = "color: #eab308;"

# --- ESTILIZAÇÃO DO JOGO (Visual Limpo e Sem Botões de Sistema) ---
st.markdown(
    f"""
    <style>
    .stApp {{ background-color: #ffffff; }}
    .titulo-jogo {{ text-align: center; color: #64748b; font-family: 'Comic Sans MS', sans-serif; font-size: 20px; }}
    .nome-crianca {{ text-align: center; font-family: 'Comic Sans MS', sans-serif; font-size: 50px; font-weight: bold; margin-top: -10px; margin-bottom: 15px; {classe_nome} }}
    
    /* Moldura Controlada da Foto */
    .moldura-foto {{
        display: block;
        margin: 0 auto;
        width: 180px;
        height: 180px;
        border: 12px solid {cor_codigo};
        border-radius: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        object-fit: cover;
    }}
    
    /* Bloco reserva caso a foto não carregue */
    .avatar-reserva {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        width: 180px;
        height: 180px;
        background-color: {cor_codigo};
        border-radius: 30px;
        font-size: 80px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }}

    /* Container dos Ônibus */
    .estacionamento-container {{
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 40px;
    }}

    /* Os Ônibus Reais de Toque Direto */
    .onibus-link {{
        text-decoration: none !important;
        -webkit-tap-highlight-color: transparent;
    }}
    .onibus-azul {{
        background-color: #1d4ed8;
        font-size: 50px;
        padding: 15px 35px;
        border-radius: 20px;
        box-shadow: 0 8px 15px rgba(29, 78, 216, 0.3);
        display: inline-block;
    }}
    .onibus-amarelo {{
        background-color: #eab308;
        font-size: 50px;
        padding: 15px 35px;
        border-radius: 20px;
        box-shadow: 0 8px 15px rgba(234, 179, 8, 0.3);
        display: inline-block;
    }}
    
    /* Oculta barras do Streamlit */
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """,
    unsafe_allow_html=True
)

# --- CORPO INTERATIVO EM HTML PURO ---
st.markdown("<div class='titulo-jogo'>Estacionamento das Cores</div>", unsafe_allow_html=True)
st.markdown(f"<div class='nome-crianca'>{NOME_DO_FILHO}</div>", unsafe_allow_html=True)

# Exibe a foto ou o avatar reserva
if os.path.exists("filho.jpg"):
    import base64
    with open("filho.jpg", "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    st.markdown(f"<img src='data:image/jpeg;base64,{img_base64}' class='moldura-foto'>", unsafe_allow_html=True)
else:
    st.markdown("<div class='avatar-reserva'>👦</div>", unsafe_allow_html=True)

# Os Ônibus de toque instantâneo
st.markdown(
    """
    <div class='estacionamento-container'>
        <a href='?clique=AZUL' target='_self' class='onibus-link'>
            <div class='onibus-azul'>🚌</div>
        </a>
        <a href='?clique=AMARELO' target='_self' class='onibus-link'>
            <div class='onibus-amarelo'>🚌</div>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
