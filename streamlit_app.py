import streamlit as st
import os
import base64

# --- CONFIGURAÇÃO DA TELA ---
st.set_page_config(page_title="Jogo do Yuri", page_icon="🚌", layout="centered")

# Carrega a foto do Yuri de um jeito mais seguro
imagem_base64 = ""
if os.path.exists("filho.jpg"):
    try:
        with open("filho.jpg", "rb") as img_file:
            imagem_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    except Exception:
        pass

# Todo o jogo empacotado para rodar direto no celular sem travar
html_jogo = f"""
<div class="titulo">🚌 PILOTO YURI: DESVIE! 🦠</div>

<div id="canvasContainer">
    <canvas id="gameCanvas" width="320" height="400"></canvas>
</div>

<div class="controles">
    <button class="btn-jogo" id="btnEsquerda">◀️</button>
    <button class="btn-jogo" id="btnDireita">▶️</button>
</div>

<style>
#MainMenu, footer, header {{ visibility: hidden; }}
.stApp {{ background-color: #0f172a; text-align: center; }}

.titulo {{
    color: #38bdf8;
    font-family: 'Comic Sans MS', sans-serif;
    font-size: 28px;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 15px;
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
    margin-top: 20px;
}}

.btn-jogo {{
    background-color: #38bdf8;
    color: white;
    font-size: 35px;
    border: none;
    padding: 15px 45px;
    border-radius: 15px;
    cursor: pointer;
    user-select: none;
    -webkit-user-select: none;
}}
.btn-jogo:active {{ background-color: #0284c7; }}
</style>

<script>
(function() {{
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    // Configurações do Yuri e dos obstáculos
    let jogador = {{ x: 135, y: 330, largura: 50, altura: 50, velocidade: 25 }};
    let obstaculos = [];
    let pontuacao = 0;
    let jogoAtivo = true;
    const emojis = ["🦠", "👾", "🪨"];

    // Puxa a foto do fundo se ela existir
    const fotoFundo = new Image();
    let temFoto = false;
    const imgStr = "{imagem_base64}";
    
    if (imgStr !== "") {{
        fotoFundo.src = "data:image/jpeg;base64," + imgStr;
        fotoFundo.onload = function() {{
            temFoto = true;
        }};
    }}

    function desenhar() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Desenha a foto do Yuri no fundo
        if (temFoto) {{
            ctx.save();
            ctx.globalAlpha = 0.40;
            ctx.drawImage(fotoFundo, 0, 0, canvas.width, canvas.height);
            ctx.restore();
        }}

        // Desenha o Ônibus
        ctx.font = "45px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText("🚌", jogador.x + 25, jogador.y + 25);

        // Desenha e move os vírus caindo
        for (let i = 0; i < obstaculos.length; i++) {{
            let obs = obstaculos[i];
            obs.y += obs.velocidade;

            ctx.font = "35px Arial";
            ctx.fillText(obs.emoji, obs.x + 15, obs.y + 15);

            // Colisão
            if (obs.x < jogador.x + jogador.largura &&
                obs.x + 30 > jogador.x &&
                obs.y < jogador.y + jogador.altura &&
                obs.y + 30 > jogador.y) {{
                jogoAtivo = false;
            }}

            // Ponto
            if (obs.y > canvas.height) {{
                pontuacao++;
                obstaculos.splice(i, 1);
                i--;
            }}
        }}

        // Placar
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 20px 'Comic Sans MS'";
        ctx.textAlign = "left";
        ctx.fillText("Pontos: " + pontuacao, 15, 25);

        if (!jogoAtivo) {{
            ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#ef4444";
            ctx.font = "bold 32px 'Comic Sans MS'";
            ctx.textAlign = "center";
            ctx.fillText("BATEU! 💥", canvas.width / 2, canvas.height / 2 - 30);
            ctx.fillStyle = "#ffffff";
            ctx.font = "18px 'Comic Sans MS'";
            ctx.fillText("Toque na tela para reiniciar 🔄", canvas.width / 2, canvas.height / 2 + 20);
            return;
        }}

        requestAnimationFrame(desenhar);
    }

    function criarObstaculo() {{
        if (!jogoAtivo) return;
        let posicoesX = [25, 90, 155, 220, 270];
        let xAleatorio = posicoesX[Math.floor(Math.random() * posicoesX.length)];
        let emojiAleatorio = emojis[Math.floor(Math.random() * emojis.length)];
        
        obstaculos.push({{
            x: xAleatorio,
            y: -40,
            emoji: emojiAleatorio,
            velocidade: 4 + Math.random() * 3
        }});
        setTimeout(criarObstaculo, 1000);
    }

    // Comandos de toque corrigidos para celular
    document.getElementById("btnEsquerda").addEventListener("click", function() {{
        if (jogoAtivo && jogador.x > 10) jogador.x -= jogador.velocidade;
    }});
    
    document.getElementById("btnDireita").addEventListener("click", function() {{
        if (jogoAtivo && jogador.x < canvas.width - 60) jogador.x += jogador.velocidade;
    }});

    canvas.addEventListener("click", function() {{
        if (!jogoAtivo) {{
            jogador.x = 135;
            obstaculos = [];
            pontuacao = 0;
            jogoAtivo = true;
            desenhar();
            criarObstaculo();
        }}
    }});

    desenhar();
    criarObstaculo();
}})();
</script>
"""

# Mostra o jogo na tela de forma direta e blindada
st.components.v1.html(html_jogo, height=520, scrolling=False)
