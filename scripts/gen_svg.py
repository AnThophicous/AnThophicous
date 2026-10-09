#!/usr/bin/env python3
"""Gera os SVGs animados do README (header, criação de adão, neofetch, fios, footer).

uso:  python3 scripts/gen_svg.py      -> escreve tudo em assets/
"""
import os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'assets')
FONT = "'JetBrains Mono','Fira Code','DejaVu Sans Mono',Menlo,Consolas,'Courier New',monospace"
random.seed(1998)  # ano de lançamento de serial experiments lain


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def lines_svg(lines, x, y, cw, lh, cls='', keep=None):
    """Cada linha vira um <text> com largura fixa (textLength) => alinhamento perfeito em qualquer fonte mono."""
    out = []
    for i, l in enumerate(lines):
        if keep is not None:
            l = ''.join(c if c in keep else ' ' for c in l)
        l = l.rstrip()
        if not l.strip():
            continue
        out.append(f'<text x="{x:.1f}" y="{y + i * lh:.1f}" textLength="{len(l) * cw:.1f}" '
                   f'lengthAdjust="spacingAndGlyphs" class="{cls}">{esc(l)}</text>')
    return '\n'.join(out)


def typing(text, x, y, cw, cls, dur, start=0.0, end=0.55, idd='t'):
    """Texto que é 'digitado' caractere por caractere (SMIL, funciona dentro de <img> no GitHub)."""
    n = len(text)
    vals = ';'.join(f'{i * cw:.1f}' for i in range(n + 1)) + f';{n * cw:.1f};0'
    kts = [start + (end - start) * i / n for i in range(n + 1)] + [0.97, 1.0]
    kts = ';'.join(f'{k:.4f}' for k in kts)
    return (f'<clipPath id="{idd}"><rect x="{x}" y="{y - 20}" width="0" height="28">'
            f'<animate attributeName="width" values="{vals}" keyTimes="{kts}" dur="{dur}s" '
            f'calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>'
            f'<text x="{x}" y="{y}" class="{cls}" clip-path="url(#{idd})" xml:space="preserve">{esc(text)}</text>')


def svg(w, h, body, css, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<style>
text {{ font-family: {FONT}; white-space: pre; }}
{css}
</style>
{body}
</svg>
'''


def write(name, content):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(content)
    print('ok', name, len(content.encode()) // 1024, 'KB')


def scanlines(w, h, idp='scan'):
    return (f'<pattern id="{idp}" width="4" height="4" patternUnits="userSpaceOnUse">'
            f'<rect width="4" height="2" fill="#000" opacity=".28"/></pattern>'
            f'<rect width="{w}" height="{h}" fill="url(#{idp})" pointer-events="none"/>'
            f'<rect class="sweep" x="0" y="-60" width="{w}" height="60" fill="url(#sweepg)"/>')


SWEEP = '''<linearGradient id="sweepg" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".85" stop-color="#fff" stop-opacity=".05"/>
<stop offset="1" stop-color="#fff" stop-opacity=".12"/></linearGradient>'''


def stars(w, h, n, avoid=None):
    s = []
    for _ in range(n):
        x, y = random.uniform(0, w), random.uniform(0, h)
        if avoid and avoid(x, y):
            continue
        r = random.choice([.6, .8, 1, 1.3])
        d = random.uniform(0, 6)
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" class="star" style="animation-delay:-{d:.2f}s"/>')
    return '\n'.join(s)


# ───────────────────────────────────────────────────────────── header ──
def header():
    W, H = 900, 330
    name = open(os.path.join(HERE, 'name.txt'), encoding='utf-8').read().rstrip('\n').split('\n')
    cw, lh = 8.6, 17.2
    nx = (W - max(map(len, name)) * cw) / 2
    ny = 128
    art = lines_svg(name, nx, ny, cw, lh)
    css = '''
.bg{fill:#07070b}
.dim{fill:#5c5c6e;font-size:12px}
.red{fill:#ff2e4d}
.cmd{fill:#d8d8e6;font-size:15px}
.sub{fill:#9a9ab0;font-size:14px;letter-spacing:.5px}
.name text{font-size:16px}
.main{fill:url(#ng)}
.gr{fill:#ff2e4d;opacity:0;mix-blend-mode:screen;animation:g1 5s infinite steps(1)}
.gc{fill:#2ef0ff;opacity:0;mix-blend-mode:screen;animation:g2 5s infinite steps(1)}
.jit{animation:jit 5s infinite steps(1)}
@keyframes g1{0%,84%,100%{opacity:0;transform:none}85%{opacity:.85;transform:translate(-5px,1px)}87%{opacity:.85;transform:translate(4px,-2px)}89%{opacity:.7;transform:translate(-2px,0)}91%{opacity:0}}
@keyframes g2{0%,84%,100%{opacity:0;transform:none}85%{opacity:.85;transform:translate(5px,-1px)}87%{opacity:.85;transform:translate(-3px,2px)}89%{opacity:.7;transform:translate(3px,0)}91%{opacity:0}}
@keyframes jit{0%,84%,92%,100%{transform:none}86%{transform:translate(2px,0) skewX(-6deg)}88%{transform:translate(-3px,0)}90%{transform:translate(1px,0) skewX(4deg)}}
.blink{animation:blink 1s infinite steps(1)}
@keyframes blink{50%{opacity:0}}
.flick{animation:flick 7s infinite}
@keyframes flick{0%,100%{opacity:1}42%{opacity:1}43%{opacity:.2}44%{opacity:1}46%{opacity:.4}47%{opacity:1}}
.sweep{animation:sweep 6s linear infinite}
@keyframes sweep{from{transform:translateY(0)}to{transform:translateY(400px)}}
.wire{stroke:#2a2a36;stroke-width:1;fill:none}
.pulse{fill:#ff2e4d}
'''
    wires = []
    for i, (y0, y1) in enumerate([(38, 70), (300, 268), (318, 290)]):
        d = f'M -10 {y0} Q 450 {y1} 910 {y0}'
        wires.append(f'<path id="w{i}" class="wire" d="{d}"/>'
                     f'<circle r="2" class="pulse"><animateMotion dur="{3 + i}s" repeatCount="indefinite" '
                     f'begin="-{i}s"><mpath href="#w{i}"/></animateMotion></circle>')
    body = f'''<defs>
<linearGradient id="ng" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="#ffd6de"/><stop offset=".5" stop-color="#ff2e4d"/>
<stop offset=".55" stop-color="#ffd6de"/><stop offset="1" stop-color="#ffffff"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="6s" repeatCount="indefinite"/>
</linearGradient>{SWEEP}</defs>
<rect class="bg" width="{W}" height="{H}" rx="14"/>
{''.join(wires)}
<text x="22" y="30" class="dim">LAYER:01 // WEIRD</text>
<text x="{W - 22}" y="30" class="dim" text-anchor="end">NAVI ▸ <tspan class="red blink">●</tspan> CONNECTED</text>
{typing('$ ./present_day --present-time --user=anthophicous', 40, 82, 9.0, 'cmd', 9, idd='tp')}
<g class="name jit">
<g class="gr">{art}</g><g class="gc">{art}</g><g class="main">{art}</g>
</g>
<text x="{W / 2}" y="{ny + 6 * lh + 22}" class="sub" text-anchor="middle">dev brasileiro · <tspan class="red">16 anos</tspan> · front-end → backend · ia · cybersec · linux</text>
<text x="{W / 2}" y="{ny + 6 * lh + 50}" class="dim flick" text-anchor="middle" style="font-size:13px">&gt; no matter where you go, everyone's connected<tspan class="red blink">█</tspan></text>
{scanlines(W, H)}'''
    write('header.svg', svg(W, H, body, css, 'AnThophicous — present day, present time'))


# ──────────────────────────────────────────────────── criação de adão ──
def creation():
    W, H = 900, 360
    art = open(os.path.join(HERE, 'adam.txt'), encoding='utf-8').read().rstrip('\n').split('\n')
    cols = max(map(len, art))
    art = [l.ljust(cols) for l in art]
    SPLIT = 110  # coluna do vão entre os dedos
    cw, lh = 4.75, 8.4
    x0 = (W - cols * cw) / 2
    y0 = 120
    adam = lines_svg([l[:SPLIT] for l in art], x0, y0, cw, lh)
    god = lines_svg([l[SPLIT:] for l in art], x0 + SPLIT * cw, y0, cw, lh)
    gapx = x0 + (SPLIT - 1) * cw
    gapy = y0 + 7 * lh
    css = '''
.bg{fill:#07070b}
.art text{font-size:8.6px;font-weight:700}
.adam{fill:url(#skinA);animation:adam 7s ease-in-out infinite}
.god{fill:url(#skinG);animation:god 7s ease-in-out infinite}
@keyframes adam{0%,100%{transform:translateX(0)}50%{transform:translateX(7px)}}
@keyframes god{0%,100%{transform:translateX(0)}50%{transform:translateX(-8px)}}
.spark{animation:spark 7s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes spark{0%,30%,70%,100%{opacity:.08;transform:scale(.4)}50%{opacity:1;transform:scale(1.25)}}
.star{fill:#fff;animation:tw 6s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.08}50%{opacity:.7}}
.t1{fill:#efe6d8;font-size:20px;letter-spacing:9px}
.t2{fill:#7d7a74;font-size:11px;letter-spacing:3px}
.t3{fill:#cfc6b8;font-size:13px;font-style:italic}
.t4{fill:#5f5c58;font-size:11px}
.red{fill:#ff2e4d}
.bit{fill:#ffcf8a;font-size:9px;opacity:0;animation:flow 4.2s linear infinite}
@keyframes flow{0%{opacity:0;transform:translate(0,0)}12%{opacity:.9}85%{opacity:.9}100%{opacity:0;transform:translate(-300px,-14px)}}
.sweep{animation:sweep 8s linear infinite}
@keyframes sweep{from{transform:translateY(0)}to{transform:translateY(440px)}}
'''
    bits = []
    for i in range(14):
        bx = random.uniform(gapx + 320, gapx + 380)
        by = random.uniform(gapy - 26, gapy + 6)
        bits.append(f'<text x="{bx:.0f}" y="{by:.0f}" class="bit" style="animation-delay:-{i * .3:.1f}s">'
                    f'{random.choice("01")}</text>')
    body = f'''<defs>
<linearGradient id="skinA" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a88466"/><stop offset=".7" stop-color="#f0d2b4"/><stop offset="1" stop-color="#fff3e2"/></linearGradient>
<linearGradient id="skinG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff6ea"/><stop offset=".5" stop-color="#f3d7bb"/><stop offset="1" stop-color="#b08a6c"/></linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="#fff2d2" stop-opacity=".95"/><stop offset=".25" stop-color="#ffcf8a" stop-opacity=".55"/><stop offset="1" stop-color="#ff9a3c" stop-opacity="0"/></radialGradient>
<radialGradient id="halo" cx=".5" cy=".55" r=".6"><stop offset="0" stop-color="#3a2a18" stop-opacity=".55"/><stop offset="1" stop-color="#07070b" stop-opacity="0"/></radialGradient>
{SWEEP}</defs>
<rect class="bg" width="{W}" height="{H}" rx="14"/>
<rect width="{W}" height="{H}" fill="url(#halo)" rx="14"/>
{stars(W, H, 90, avoid=lambda x, y: 105 < y < 280)}
<text x="{W / 2}" y="44" class="t1" text-anchor="middle">A CRIAÇÃO DE ADÃO</text>
<text x="{W / 2}" y="66" class="t2" text-anchor="middle">MICHELANGELO · CAPELA SISTINA · c.1512 · <tspan class="red">LAYER:04 RELIGION</tspan></text>
<g class="art"><g class="adam">{adam}</g><g class="god">{god}</g></g>
{''.join(bits)}
<circle class="spark" cx="{gapx + 2:.1f}" cy="{gapy:.1f}" r="22" fill="url(#glow)"/>
<text x="{W / 2}" y="{H - 52}" class="t3" text-anchor="middle">“quase se tocam — e é nesse espaço que tudo é criado.”</text>
<text x="{W / 2}" y="{H - 26}" class="t4" text-anchor="middle">$ ping adam  →  64 bytes from adam: icmp_seq=1 ttl=∞ time=0.0001 ms  <tspan class="red">(distância: nunca zero)</tspan></text>
{scanlines(W, H)}'''
    write('creation.svg', svg(W, H, body, css, 'A Criação de Adão em ASCII — as mãos quase se tocam'))


# ─────────────────────────────────────────────────────────── neofetch ──
# Tux em pixel art. K=corpo  G=brilho  W=barriga  E=olho  P=pupila  Y=bico/pés  D=sombra amarela
TUX = '''
...........KKKKKK...........
.........KKKKKKKKKK.........
........KKKKKKKKKKKK........
.......KKKGKKKKKKKKKK.......
.......KKGKKKKKKKKKKK.......
.......KKEEEKKKKEEEKK.......
.......KEEEEEKKEEEEEK.......
.......KEEPPEKKEPPEEK.......
.......KEEPPEKKEPPEEK.......
.......KKEEEDYYDEEEKK.......
.......KKKDYYYYYYDKKK.......
.......KKYYYYYYYYYYKK.......
......KKKDYYYYYYYYDKKK......
......KKWWDDYYYYDDWWKK......
.....KKWWWWDDDDDDWWWWKK.....
.....KKWWWWWWWWWWWWWWKK.....
....KKWWWWWWWWWWWWWWWWKK....
....KGWWWWWWWWWWWWWWWWGK....
...KKGWWWWWWWWWWWWWWWWGKK...
...KGWWWWWWWWWWWWWWWWWWGK...
..KKGWWWWWWWWWWWWWWWWWWGKK..
..KGKWWWWWWWWWWWWWWWWWWKGK..
..KGKWWWWWWWWWWWWWWWWWWKGK..
..KKKWWWWWWWWWWWWWWWWWWKKK..
...KKWWWWWWWWWWWWWWWWWWKK...
...YYYKWWWWWWWWWWWWWWKYYY...
..YYYYYYKWWWWWWWWWWKYYYYYY..
.YYYYYYYYKKKKKKKKKKYYYYYYYY.
.DYYYYYYYD........DYYYYYYYD.
..DDDDDDD..........DDDDDDD..
'''.strip('\n').split('\n')

TUX_COLORS = {'O': '#4b4b60', 'K': '#1c1c26', 'G': '#4a4a5e', 'W': '#f0f0f6', 'w': '#c9c9d6',
              'E': '#ffffff', 'P': '#101016', 'Y': '#f6c343', 'D': '#d68c14'}


def tux_pixels(x0, y0, px):
    # contorno automático (pra o corpo preto não sumir no fundo escuro) + sombra na barriga
    g = ['.' * (len(TUX[0]) + 2)] + ['.' + l + '.' for l in TUX] + ['.' * (len(TUX[0]) + 2)]
    g = [list(l) for l in g]
    H, W = len(g), len(g[0])
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' and any(0 <= y + dy < H and 0 <= x + dx < W and g[y + dy][x + dx] not in '.O'
                                      for dy in (-1, 0, 1) for dx in (-1, 0, 1)):
                g[y][x] = 'O'
    for y in range(H):
        for x in range(W):
            if g[y][x] == 'W' and (g[y][x + 1] not in 'Ww' or g[y + 1][x] not in 'Ww'):
                g[y][x] = 'w'
    rects, lids = {}, []
    for y in range(H):
        for x in range(W):
            c = g[y][x]
            if c == '.':
                continue
            r = f'<rect x="{x0 + x * px}" y="{y0 + y * px}" width="{px - .6}" height="{px - .6}"/>'
            rects.setdefault(c, []).append(r)
            if c in 'EP':
                lids.append(r)
    out = ''.join(f'<g fill="{TUX_COLORS[c]}">{"".join(r)}</g>' for c, r in rects.items())
    return out + f'<g class="lid" fill="{TUX_COLORS["K"]}">{"".join(lids)}</g>'


INFO = [
    ('OS', 'Brasil (BR) x86_64'),
    ('Host', 'The Wired · Layer 07'),
    ('Kernel', '16.0.0-adolescente'),
    ('Uptime', '16 anos, 0 desistências'),
    ('Shell', 'curiosidade (desde os 10)'),
    ('Packages', 'html css js ts node c++ c#'),
    ('Installing', 'rust · backend · cybersec · ia'),
    ('DE', 'front-end'),
    ('WM', 'engenharia de prompt (T.I.C.)'),
    ('Terminal', 'NAVI'),
    ('Target', 'google · microsoft · openai · anthropic'),
    ('Motto', 'aprender. construir. evoluir.'),
]


def neofetch():
    W, H = 900, 400
    tux = tux_pixels(28, 76, 8.6)
    ix, iy = 330, 92
    rows = [f'<text x="{ix}" y="{iy}" class="k" style="animation-delay:1.0s">anthophicous<tspan class="v">@</tspan>wired</text>',
            f'<text x="{ix}" y="{iy + 20}" class="v" style="animation-delay:1.1s">────────────────────</text>']
    for i, (k, v) in enumerate(INFO):
        y = iy + 42 + i * 19.5
        rows.append(f'<text x="{ix}" y="{y}" style="animation-delay:{1.2 + i * .12:.2f}s">'
                    f'<tspan class="k">{esc(k)}</tspan><tspan class="v" x="{ix + 110}">{esc(v)}</tspan></text>')
    # barra de progresso do "Installing"
    by = iy + 42 + 6 * 19.5 - 9
    bar = (f'<rect x="{ix + 455}" y="{by:.0f}" width="100" height="10" class="barbg"/>'
           f'<rect x="{ix + 455}" y="{by:.0f}" width="0" height="10" class="bar">'
           f'<animate attributeName="width" values="0;72;64;100;0" keyTimes="0;.4;.5;.9;1" dur="8s" repeatCount="indefinite"/></rect>')
    cols = ['#0b0b10', '#ff2e4d', '#3ddc84', '#f7df1e', '#3b82f6', '#c084fc', '#2ef0ff', '#e6e6f0']
    blocks = ''.join(f'<rect x="{ix + i * 30}" y="{iy + 42 + len(INFO) * 19.5 + 4:.0f}" width="26" height="14" fill="{c}" rx="2"/>'
                     for i, c in enumerate(cols))
    css = '''
.bg{fill:#0b0b10}
.bar0{fill:#16161e}
.dot{opacity:.9}
.ttl{fill:#6d6d80;font-size:12px}
.p{fill:#d8d8e6;font-size:15px}
.ps{fill:#ff2e4d}
.lid{opacity:0;animation:lid 4.5s infinite steps(1)}
@keyframes lid{0%,92%,100%{opacity:0}93%,95%{opacity:1}}
.tux{animation:bob 3s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
.info text{font-size:14px;animation:in .35s ease-out backwards}
@keyframes in{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}
.k{fill:#ff2e4d;font-weight:700}
.v{fill:#d8d8e6}
.barbg{fill:#1d1d27}
.bar{fill:#ff2e4d}
.blink{animation:blink 1s infinite steps(1)}
@keyframes blink{50%{opacity:0}}
.sweep{animation:sweep 7s linear infinite}
@keyframes sweep{from{transform:translateY(0)}to{transform:translateY(480px)}}
'''
    body = f'''<defs>{SWEEP}</defs>
<rect class="bg" width="{W}" height="{H}" rx="14"/>
<rect class="bar0" width="{W}" height="34" rx="14"/><rect class="bar0" y="20" width="{W}" height="14"/>
<circle cx="22" cy="17" r="6" fill="#ff5f57"/><circle cx="42" cy="17" r="6" fill="#febc2e"/><circle cx="62" cy="17" r="6" fill="#28c840"/>
<text x="{W / 2}" y="21" class="ttl" text-anchor="middle">anthophicous@wired: ~</text>
<text x="24" y="64" class="p"><tspan class="ps">❯</tspan></text>
{typing('neofetch', 44, 64, 9.0, 'p', 30, start=0.0, end=0.025, idd='nf')}
<g class="tux">{tux}</g>
<g class="info">{''.join(rows)}</g>
{bar}
{blocks}
<text x="24" y="{H - 18}" class="p"><tspan class="ps">❯</tspan> <tspan class="blink">█</tspan></text>
{scanlines(W, H)}'''
    write('neofetch-tux.svg', svg(W, H, body, css, 'neofetch — anthophicous@wired, 16 anos'))


# ───────────────────────────────────────────── divisor: postes e fios ──
def wires():
    W, H = 900, 90
    poles = [90, 450, 810]
    parts = []
    for px in poles:
        parts.append(f'<line x1="{px}" y1="8" x2="{px}" y2="{H}" class="pole"/>'
                     f'<line x1="{px - 34}" y1="18" x2="{px + 34}" y2="18" class="pole"/>'
                     f'<line x1="{px - 24}" y1="30" x2="{px + 24}" y2="30" class="pole"/>')
        for dx in (-30, -12, 12, 30):
            parts.append(f'<rect x="{px + dx - 2}" y="13" width="4" height="5" class="ins"/>')
    k = 0
    for dx, y in ((-30, 18), (-12, 18), (12, 18), (30, 18), (-24, 30), (24, 30)):
        pts = [-80] + poles + [980]
        for a, b in zip(pts, pts[1:]):
            sag = 22 if dx < 0 else 16
            d = f'M {a + dx} {y} Q {(a + b) / 2 + dx} {y + sag} {b + dx} {y}'
            parts.append(f'<path id="p{k}" d="{d}" class="wire"/>')
            if random.random() < .45:
                dur = random.uniform(1.6, 3.2)
                parts.append(f'<circle r="1.8" class="pulse"><animateMotion dur="{dur:.2f}s" '
                             f'begin="-{random.uniform(0, dur):.2f}s" repeatCount="indefinite"><mpath href="#p{k}"/></animateMotion></circle>')
            k += 1
    css = '''
.pole{stroke:#8a8a99;stroke-width:2}
.ins{fill:#8a8a99}
.wire{stroke:#8a8a99;stroke-width:1;fill:none;opacity:.7}
.pulse{fill:#ff2e4d}
.hum{fill:#8a8a99;font-size:10px;letter-spacing:4px;animation:hum 2.4s ease-in-out infinite}
@keyframes hum{0%,100%{opacity:.25}50%{opacity:.8}}
'''
    body = ''.join(parts) + f'<text x="{W / 2}" y="{H - 6}" class="hum" text-anchor="middle">ブーーーーーン</text>'
    write('wires.svg', svg(W, H, body, css, 'postes e fios — the wired'))


# ───────────────────────────────────────────────────────────── footer ──
def footer():
    W, H = 900, 150
    css = '''
.bg{fill:#07070b}
.a,.b{font-size:30px;letter-spacing:6px;fill:#e6e6f0;font-weight:700}
.a{animation:fa 6s infinite steps(1)}
.b{animation:fb 6s infinite steps(1);fill:#ff2e4d}
@keyframes fa{0%,45%{opacity:1}46%{opacity:0}47%{opacity:1}50%,100%{opacity:0}}
@keyframes fb{0%,49%{opacity:0}50%,95%{opacity:1}96%{opacity:0}97%{opacity:1}100%{opacity:0}}
.s{fill:#5c5c6e;font-size:12px;letter-spacing:2px}
.red{fill:#ff2e4d}
.sweep{animation:sweep 5s linear infinite}
@keyframes sweep{from{transform:translateY(0)}to{transform:translateY(220px)}}
'''
    body = f'''<defs>{SWEEP}</defs>
<rect class="bg" width="{W}" height="{H}" rx="14"/>
<text x="{W / 2}" y="70" class="a" text-anchor="middle">CLOSE THE WORLD, OPEN THE NEXT</text>
<text x="{W / 2}" y="70" class="b" text-anchor="middle">.TXEN EHT NEPO ,DLROW EHT ESOLC</text>
<text x="{W / 2}" y="108" class="s" text-anchor="middle">let's all love lain · <tspan class="red">present day, present time</tspan></text>
{scanlines(W, H)}'''
    write('footer.svg', svg(W, H, body, css, 'close the world, open the next'))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    header(); creation(); neofetch(); wires(); footer()
