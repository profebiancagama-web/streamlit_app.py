import streamlit as st
import random
import os

# --- CONFIGURAÇÃO DA TELA ---
st.set_page_config(page_title="Missão Yuri: Desvio Espacial!", page_icon="🚌", layout="centered")

# --- ESTILIZAÇÃO DO AMBIENTE (Sem f-strings para evitar erros) ---
st.markdown(
    """
    <style>
    /* Esconde as barras do Streamlit */
    #MainMenu, footer, header { visibility: hidden; }
    .stApp { background-color: #0f172a; text-align: center; }
    
    .titulo {
        color: #38bdf8;
        font-family: 'Comic Sans MS', sans-serif;
        font-size: 28px;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 5px;
        text-align: center;
    }
    
    /* Centraliza os botões e o jogo na tela do notebook */
    .block-container {
        max-width: 400px !important;
        padding-top: 2rem !important;
    }
    
    /* Deixa os botões de seta bonitos e grandes */
    .stButton > button {
        background-color: #38bdf8 !important;
        color: white !important;
        font-size: 30px !important;
        border-radius: 15px !important;
        padding: 10px 0px !important;
        border: none !important;
    }
    .stButton > button:active { background-color: #0284c7 !important; }
    
    /* Estilo da foto do Yuri */
    img { 
        border: 8px solid #38bdf8 !important; 
        border-radius: 20px !important; 
        margin: 0 auto !important; 
        display: block !important; 
    }
    </style>
    <div class="titulo">🚌 PILOTO YURI: DESVIE! 🦠</div>
    """,
    unsafe_allow_html=True
)

# --- INICIALIZAÇÃO DO ESTADO DO JOGO ---
if "yuri_x" not in st.session_state:
    st.session_state.yuri_x = 2  # Começa na pista do meio (0, 1, 2, 3, 4)
if "pontos" not in st.session_state:
    st.session_state.pontos = 0
if "pos_obstaculos" not in st.session_state:
    st.session_state.pos_obstaculos = [random.randint(0, 4) for _ in range(3)]

# --- LÓGICA DE MOVIMENTAÇÃO ---
col_esq, col_dir = st.columns(2)

with col_esq:
    if st.button("◀️", key="btn_esq", use_container_width=True):
        if st.session_state.yuri_x > 0:
            st.session_state.yuri_x -= 1
            st.session_state.pos_obstaculos.pop()
            st.session_state.pos_obstaculos.insert(0, random.randint(0, 4))
            st.session_state.pontos += 1

with col_dir:
    if st.button("▶️", key="btn_dir", use_container_width=True):
        if st.session_state.yuri_x < 4:
            st.session_state.yuri_x += 1
            st.session_state.pos_obstaculos.pop()
            st.session_state.pos_obstaculos.insert(0, random.randint(0, 4))
            st.session_state.pontos += 1

st.write(" ")

# --- VERIFICAÇÃO DE BATIDA (COLISÃO) ---
if st.session_state.yuri_x == st.session_state.pos_obstaculos[-1]:
    st.markdown("<h2 style='text-align:center; color:#ef4444; font-family:Comic Sans MS;'>💥 BATEU! 💥</h2>", unsafe_allow_html=True)
    if st.button("Jogar de Novo 🔄", use_container_width=True):
        st.session_state.pontos = 0
        st.session_state.yuri_x = 2
        st.session_state.pos_obstaculos = [random.randint(0, 4) for _ in range(3)]
        st.rerun()
else:
    # --- DESENHA A PISTA DO JOGO ---
    pista_1 = ["⬛", "⬛", "⬛", "⬛", "⬛"]
    pista_1[st.session_state.pos_obstaculos[0]] = "🦠"
    
    pista_2 = ["⬛", "⬛", "⬛", "⬛", "⬛"]
    pista_2[st.session_state.pos_obstaculos[1]] = "👾"
    
    pista_3 = ["⬛", "⬛", "⬛", "⬛", "⬛"]
    pista_3[st.session_state.yuri_x] = "🚌"

    # Mostra os pontos em formato amigável
    st.markdown(f"<h3 style='text-align:center; color:white;'>Pontos: {st.session_state.pontos}</h3>", unsafe_allow_html=True)

    # Exibe o cenário do jogo
    st.markdown(f"<h2 style='text-align:center; letter-spacing: 10px;'>{''.join(pista_1)}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center; letter-spacing: 10px;'>{''.join(pista_2)}</h2>", unsafe_allow_html=True)
    
    # Adiciona a foto do Yuri no
