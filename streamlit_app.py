import streamlit as st
import os
import base64

# --- CONFIGURAÇÃO DA TELA ---
st.set_page_config(page_title="Missão Yuri: Desvio Espacial!", page_icon="🚌", layout="centered")

# Transforma a foto filho.jpg em formato que o jogo entende
imagem_base64 = ""
if os.path.exists("filho.jpg"):
    with open("filho.jpg", "rb") as img_file:
        imagem_base64 = base64.b64encode(img_file.read()).decode()

# Injeta o jogo com a foto de fundo
st.markdown(
    f"""
    <style>
    /* Oculta as barras do Streamlit */
    #MainMenu, footer, header {{ visibility: hidden; }}
    .stApp {{ background-color: #0f172a; text-align: center; }}
    
    .titulo {{
        color: #38bdf8;
        font-family: 'Comic Sans MS', sans-serif;
        font-size: 28px;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 5px;
    }}
    
    #canvasContainer {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
    }}
    
    canvas {{
        background-color: #1e293b;
        border: 4px solid #38bdf8;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        display: block;
        touch-action: none;
    }}

    .controles {{
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-top: 15px;
    }}
    
    .btn-jogo {{
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
    }}
    .btn-jogo:active {{ background-color: #0284c7; }}
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

    // Tenta carregar a foto do Yuri para o fundo
    const fotoFundo = new Image();
    let temFoto = false;
    
    if ("{imagem_base64}" !== "") {{
        fotoFundo.src = "data:image/jpeg;base64,{imagem_base64}";
        fotoFundo.onload = function() {{
            temFoto = true;
        }};
    }}

    // Configurações do jogo
    let jogador = { x: 135, y: 330, largura: 50, altura: 50, velocidade: 25 };
    let obstaculos = [];
    let pontuacao = 0;
    let jogoAtivo = true;
    
    const emojisObstaculos = ["🦠", "👾", "🪨", "🦠"];

    function desenhar() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 🖼️ SE TIVER A FOTO, DESENHA ELA NO FUNDO COM EFEITO SUAVE (OPACIDADE)
        if (temFoto) {{
            ctx.save();
            ctx.globalAlpha = 0.35; // Deixa a foto suave para dar para ver o ônibus e os vírus
            // Desenha a foto esticada certinho no tamanho da pista
            ctx.drawImage(fotoFundo, 0, 0, canvas.width, canvas.height);
            ctx.restore();
        }}

        // Desenha o Ônibus do Yuri
        ctx.font = "45px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText("🚌", jogador.x + 25, jogador.y + 25);

        // Desenha os obstáculos caindo
        for (let i = 0; i < obstaculos.length; i++) {{
            let obs = obstaculos[i];
            obs.y += obs.velocidade;

            ctx.font = "35px Arial";
            ctx.fillText(obs.emoji, obs.x + 15, obs.y + 15);

            // Verifica colisão
            if (obs.x < jogador.x + jogador.largura &&
                obs.x + 30 > jogador.x &&
                obs.y < jogador.y + jogador.altura &&
                obs.y + 30 > jogador.y) {{
                jogoAtivo = false;
            }}

            if (obs.y > canvas.height) {{
                pontuacao += 1;
                obstaculos.splice(i, 1);
                i--;
            }}
        }}

        // Placar
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 20px 'Comic Sans MS'";
        ctx.textAlign = "left";
        ctx.fillText("Pontos: " + pontuacao, 15, 25);

        // Game Over
        if (!jogoAtivo) {{
            ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = "#ef4444";
            ctx.font = "bold 32px 'Comic Sans MS'";
            ctx.textAlign = "center";
            ctx.fillText("BATEU! 💥", canvas.width / 2, canvas.height / 2 - 30);
            
            ctx.fillStyle = "#ffffff";
            ctx.font = "20px 'Comic Sans MS'";
            ctx.fillText("Toque na tela para", canvas.width / 2, canvas.height / 2 + 10);
            ctx.fillText("jogar de novo 🔄", canvas.width / 2, canvas.height / 2 + 35);
            return;
        }}

        requestAnimationFrame(desenhar);
    }

    function gerarObstaculos() {
        if (!jogoAtivo) return;
        
        let posicoesX = [30, 95, 160, 225, 280];
        let xAleatorio = posicoesX[Math.floor(Math.random() * posicoesX.length)];
        let emojiAleatorio = emojisObstaculos[Math.floor(Math.random() * emojisObstaculos.length)];
        let velAleatoria = 3 + Math.random() * 3;
        
        if (xAleatorio > canvas.width - 35) {{ xAleatorio = canvas.width - 45; }}

        obstaculos.push({
            x: xAleatorio,
            y: -40,
            emoji: emojiAleatorio,
            velocidade: velAleatoria
        });

        setTimeout(gerarObstaculos, 1100);
    }

    function moverEsquerda() {
        if (jogoAtivo && jogador.x > 10) {{
            jogador.x -= jogador.velocidade;
        }}
    }

    function moverDireita() {
        if (jogoAtivo && jogador.x < canvas.width - 60) {{
            jogador.x += jogador.velocidade;
        }}
    }

    window.addEventListener("keydown", function(e) {
        if (e.key === "ArrowLeft") moverEsquerda();
        if (e.key === "ArrowRight") moverDireita();
    });

    canvas.addEventListener("click", function() {
        if (!jogoAtivo) {{
            jogador.x = 135;
            obstaculos = [];
            pontuacao = 0;
            jogoAtivo = true;
            desenhar();
            gerarObstaculos();
        }}
    });

    desenhar();
    gerarObstaculos();
    </script>
    """,
    unsafe_allow_html=True
)
