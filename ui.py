CARD_CSS = """
<style>
@keyframes dealCard {
    0%   { opacity: 0; transform: translateY(-40px) rotateY(90deg) scale(0.7); }
    60%  { transform: translateY(4px) rotateY(0deg) scale(1.05); }
    100% { opacity: 1; transform: translateY(0) rotateY(0deg) scale(1); }
}
@keyframes dealHidden {
    0%   { opacity: 0; transform: translateY(-40px) scale(0.7); }
    60%  { transform: translateY(4px) scale(1.05); }
    100% { opacity: 1; transform: translateY(0) scale(1); }
}
.bj-card, .bj-card-hidden {
    border: 2px solid #ccc;
    border-radius: 8px;
    padding: 8px 14px;
    margin: 4px;
    font-size: 1.4rem;
    font-weight: bold;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
    min-width: 54px;
    text-align: center;
}
.bj-card {
    display: inline-block;
    background: white;
    line-height: 1.2;
    animation: dealCard 0.4s ease-out both;
}
.bj-card-hidden {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: #1a6b3c;
    color: white;
    min-height: 54px;
    animation: dealHidden 0.4s ease-out both;
}
</style>
"""

FIREWORKS_JS = """
<canvas id="fireworks-canvas" style="width:100%;height:100%;pointer-events:none;background:transparent;"></canvas>
<script>
(function() {
    const canvas = document.getElementById('fireworks-canvas');
    if (!canvas) return;
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width || 800;
    canvas.height = 400;
    const ctx = canvas.getContext('2d');
    const particles = [];
    const colors = ['#ff4757','#ffa502','#2ed573','#1e90ff','#ff6b81','#eccc68','#a29bfe','#fd79a8'];
    function createBurst(x, y) {
        for (let i = 0; i < 80; i++) {
            const angle = (Math.PI * 2 / 80) * i;
            const speed = 2 + Math.random() * 5;
            particles.push({
                x, y,
                vx: Math.cos(angle) * speed, vy: Math.sin(angle) * speed,
                alpha: 1, color: colors[Math.floor(Math.random() * colors.length)],
                radius: 3 + Math.random() * 3, gravity: 0.08
            });
        }
    }
    let bursts = 0;
    function scheduleBurst() {
        if (bursts >= 6) return;
        bursts++;
        createBurst(canvas.width * (0.2 + Math.random() * 0.6), canvas.height * (0.1 + Math.random() * 0.5));
        setTimeout(scheduleBurst, 400);
    }
    scheduleBurst();
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.x += p.vx; p.y += p.vy; p.vy += p.gravity; p.alpha -= 0.015;
            if (p.alpha <= 0) { particles.splice(i, 1); continue; }
            ctx.save(); ctx.globalAlpha = p.alpha; ctx.fillStyle = p.color;
            ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fill(); ctx.restore();
        }
        if (particles.length > 0) requestAnimationFrame(animate);
    }
    animate();
})();
</script>
"""


def render_card(label, index=0):
    rank, suit = label[:-1], label[-1]
    color = "red" if suit in ("♥", "♦") else "black"
    delay = f"{index * 0.12:.2f}s"
    return f'<div class="bj-card" style="color:{color};animation-delay:{delay};">{rank}<br>{suit}</div>'


def render_hidden_card(index=0):
    delay = f"{index * 0.12:.2f}s"
    return f'<div class="bj-card-hidden" style="animation-delay:{delay};">?</div>'


def render_hand(cards, revealed=True):
    if revealed:
        html = "".join(render_card(c, i) for i, c in enumerate(cards))
    else:
        html = render_card(cards[0], 0)
        html += "".join(render_hidden_card(i + 1) for i in range(len(cards) - 1))
    return f'<div style="display:flex;flex-wrap:wrap;">{html}</div>'


def render_stat_card(label, value, color):
    return f"""
    <div style="
        border: 2px solid {color}; border-radius: 12px;
        padding: 14px 10px; text-align: center;
        background: rgba(255,255,255,0.04);
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        font-family: 'Georgia', serif;
    ">
        <div style="font-size:0.78rem; letter-spacing:2px; text-transform:uppercase;
                    color:{color}; margin:4px 0 8px;">{label}</div>
        <div style="font-size:2rem; font-weight:bold; color:{color};">{value}</div>
    </div>
    """
