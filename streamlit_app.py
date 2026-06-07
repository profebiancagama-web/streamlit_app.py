import streamlit as st
import random
import os

# --- CONFIGURAÇÃO DA TELA ---
st.set_page_config(page_title="Estacionamento das Cores", page_icon="🚌", layout="centered")

# CSS para sumir com botões feios de computador e focar só no desenho e na cor
st.markdown(
    """
    <style>
    .stApp { background-color: #ffffff; }
    
    /* Título e Nome */
    .titulo-jogo { text-align: center; color: #64748b; font-family: 'Comic Sans MS', sans-serif; font-size: 24px; }
    .nome-crianca { text-align: center; font-family: 'Comic Sans MS', sans-serif; font-size: 55px; font-weight: bold; margin-top: -10px; }
    
    /* Cores do Nome */
    .nome-azul { color: #1d4ed8; }
    .nome-amarelo { color: #eab308; }

    /* Estilo dos Ônibus Desenhados (Botões Invisíveis por trás, Visual Puro por fora) */
    .div-onibus-azul { background-color: #1d4ed8; font-size: 90px; text-align: center; padding: 20px; border-radius: 30px; box-shadow: 0 15px 25px rgba(29, 78, 216, 0.4); cursor: pointer; }
    .div-onibus-amarelo { background-color: #eab308; font-size: 90px; text-align: center; padding: 20px; border-radius: 30px; box-shadow: 0 15px 25px rgba(234, 179, 8, 0.4); cursor: pointer; }
    
    /* Esconde o texto padrão do botão do streamlit */
    .stButton > button { background: transparent !important; border: none !important; width: 100% !important; height: 100% !important; padding: 0 !important; }
    .stButton > button:hover { background: transparent !important; }
    
    .mensagem-sucesso { font-size: 60px; text-align: center; color: #10b981; font-family: 'Comic Sans MS', sans-serif; font-weight: bold; margin-top: 20px; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='titulo-jogo'>Estacionamento das Cores 🚌</div>", unsafe_allow_html=True)

# =========================================================
# ✏️ CONFIGURAÇÃO DO NOME DO SEU FILHO:
NOME_DO_FILHO = "Emanuel"
# =========================================================

# --- INICIALIZAÇÃO DO JOGO ---
if "cor_atual" not in st.session_state:
    st.session_state.cor_atual = random.choice(["AZUL", "AMARELO"])
if "acertou" not in st.session_state:
    st.session_state.acertou = False

# --- EXIBIÇÃO DO NOME GIGANTE ---
classe_nome = "nome-azul" if st.session_state.cor_atual == "AZUL" else "nome-amarelo"
st.markdown(f"<div class='nome-crianca {classe_nome}'>{NOME_DO_FILHO}</div>", unsafe_allow_html=True)

# --- FOTO CENTRAL COM MOLDURA FORTE ---
col_foto_centro, _ = st.columns([1, 0.01])
with col_foto_centro:
    if os.path.exists("filho.jpg"):
        st.image("filho.jpg", use_container_width=True)
        if st.session_state.cor_atual == "AZUL":
            st.markdown("<style>img { border: 20px solid #1d4ed8; border-radius: 40px; }</style>", unsafe_allow_html=True)
        else:
            st.markdown("<style>img { border: 20px solid #eab308; border-radius: 40px; }</style>", unsafe_allow_html=True)
    else:
        # Bloco reserva caso a foto não carregue
        if st.session_state.cor_atual == "AZUL":
            st.markdown("<div style='background:#1d4ed8; height:200px; border-radius:30px; text-align:center; line-height:200px; font-size:80px;'>👦</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='background:#eab308; height:200px; border-radius:30px; text-align:center; line-height:200px; font-size:80px;'>👦</div>", unsafe_allow_html=True)

st.write(" ")
st.write(" ")

# --- OS DOIS ÔNIBUS GIGANTES (ÁREA DE CLIQUE) ---
col1, col2 = st.columns(2)

with col1:
    # Cria o visual do Ônibus Azul gigante
    st.markdown("<div class='div-onibus-azul'>🚌</div>", unsafe_allow_html=True)
    # Coloca o clique invisível em cima dele
    if st.button("", key="clique_azul"):
        if st.session_state.cor_atual == "AZUL":
            st.session_state.acertou = True

with col2:
    # Cria o visual do Ônibus Amarelo gigante
    st.markdown("<div class='div-onibus-amarelo'>🚌</div>", unsafe_allow_html=True)
    # Coloca o clique invisível em cima dele
    if st.button("", key="clique_amarelo"):
        if st.session_state.cor_atual == "AMARELO":
            st.session_state.acertou = True

# --- TELA DE SUCESSO ---
if st.session_state.acertou:
    st.markdown("<div class='mensagem-sucesso'>🌟 PARABÉNS! 🌟</div>", unsafe_allow_html=True)
    st.session_state.cor_atual = random.choice(["AZUL", "AMARELO"])
    st.session_state.acertou = False
    import time
    time.sleep(1.3)
    st.rerun()
