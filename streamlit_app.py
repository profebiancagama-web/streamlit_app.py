import streamlit as st

# --- CONFIGURAÇÃO DA TELA ---
st.set_page_config(page_title="Missão Yuri: Desvio Espacial!", page_icon="🚌", layout="centered")

# Injeta o jogo em JavaScript e HTML5 direto na tela do Streamlit
st.markdown(
    """
    <style>
    /* Esconde as coisas do Streamlit para focar só no jogo */
    #MainMenu, footer, header { visibility: hidden; }
    .stApp { background-color: #0f172a; text-align: center; }
    
    .titulo {
        color: #38bdf8;
        font-family: 'Comic Sans MS', sans-serif;
        font-size: 28px;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    
    /* Caixa do Jogo */
    #canvasContainer {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
    }
    
    canvas {
        background-color: #1e293b;
        border: 4px solid #38bdf8;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        display: block;
        touch-action: none; /* Impede o celular de puxar a página para baixo ao jogar */
    }

    /* Botões de controle para o celular */
    .controles {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-top: 15px;
    }
    
    .btn-jogo {
        background-color: #38bdf8;
        color: white;
        font-size: 35px;
        border: none;
        padding: 15px 40px;
        border-radius: 15px;
        box-shadow: 0 5px 10px rgba(56, 189, 248, 0.3);
        cursor: pointer;
        user-select: none;
        -webkit-user-select: none;
    }
    .btn-jogo:active { background-color: #0284c7; }
    </style>

    <div class="titulo">🚌 PILOTO YURI: DESVIE! 🦠</div>
    
    <div id="canvasContainer">
        <canvas id="gameCanvas" width="320" height="400"></canvas>
    </div>

    <div class="controles">
        <button class="btn-jogo" id="btnEsquerda" onmousedown="moverEsquerda()" ontouchstart="moverEsquerda()">◀️</button>
        <button class="btn-jogo" id="btnDireita" onmousedown="moverDireita()" ontouchstart="moverDireita()">▶️</button>
    </div>

    <script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    // Configurações do jogo
    let jogador = { x: 135, y: 330, largura: 50, altura: 50, velocidade: 25 };
    let obstaculos = [];
    let pontuacao = 0;
    let jogoAtivo = true;
    
    // Lista de emojis que vão cair (bactérias, vírus e pedras)
    const emojisObstaculos = ["🦠", "👾", "🪨", "🦠"];

    // Desenha o jogo
