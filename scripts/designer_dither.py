#!/usr/bin/env python3
"""Banner 'Mid-Level · Fullstack / Website Designer' — seda vermelha animada, dithering estilo PC-98
e referências a anime retrô (Evangelion, Cowboy Bebop, VHS dos anos 90).

gera:  assets/designer.gif
uso:   python3 scripts/designer_dither.py      (precisa de numpy + pillow)
"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'assets', 'designer.gif')
W, H = 900, 420
NF, MS = 48, 83                      # 48 quadros × 83 ms ≈ 4 s em loop perfeito
SANS = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
SERIF = '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
JP = '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'
random.seed(26)

# paleta limitada, tipo PC-98: só vermelhos (escuro -> branco)
PAL = ['#0e0006', '#2e000c', '#5c0617', '#9a0c26', '#d0143a', '#ff3b5c', '#ff9aab', '#ffe3e8', '#ffffff']
NP = len(PAL)
PAL_RGB = [int(c[i:i + 2], 16) for c in PAL for i in (1, 3, 5)]


def bayer(n=4):
    m = np.array([[0, 2], [3, 1]])
    while m.shape[0] < n:
        m = np.block([[4 * m, 4 * m + 2], [4 * m + 3, 4 * m + 1]])
    return (m + 0.5) / m.size


def dither(level, h, w, n=4):
    """level em 0..NP-1 (float) -> índice da paleta com dithering ordenado (Bayer)."""
    b = np.tile(bayer(n), (h // n + 1, w // n + 1))[:h, :w]
    return np.clip(np.floor(level + b), 0, NP - 1).astype(np.uint8)


# ── seda: campo de dobras com distorção de domínio (curvas, nada de reta) ─────
BW, BH = W // 2, H // 2
uu, vv = np.meshgrid(np.linspace(0, 1, BW), np.linspace(0, BH / BW, BH))


def silk(p):
    wx = 0.16 * np.sin(2 * np.pi * (0.9 * uu + 0.5 * vv) + p) + 0.07 * np.sin(2 * np.pi * (2.1 * vv - 0.4 * uu) - 2 * p)
    wy = 0.12 * np.sin(2 * np.pi * (0.6 * uu - 1.1 * vv) - p) + 0.05 * np.sin(2 * np.pi * (1.7 * uu) + 3 * p)
    x, y = uu + wx, vv + wy
    h1 = np.sin(2 * np.pi * (1.15 * x - 1.9 * y) + 1.3 * np.sin(2 * np.pi * (0.45 * x + 0.8 * y) + p))
    h2 = np.sin(2 * np.pi * (2.3 * x - 1.2 * y) - p + 0.8 * np.sin(2 * np.pi * 1.3 * y + p))
    h = 0.72 * h1 + 0.28 * h2
    light = np.clip(uu - 0.8 * vv, 0, 1)                     # luz vindo de cima à direita
    b = 0.04 + 0.26 * (0.5 + 0.5 * h) + 0.30 * light
    b += 0.50 * np.exp(-((h - 0.86) / 0.06) ** 2)              # brilho fino no topo das dobras
    b += 0.22 * np.exp(-((h1 + 0.2) / 0.045) ** 2) * (uu > 0.25)  # segunda linha de brilho
    vig = 1 - 0.55 * ((uu - 0.5) ** 2 * 1.6 + (vv - 0.23) ** 2 * 6)
    return np.clip(b * vig, 0, 1), h


# ── camadas de texto (máscaras em resolução cheia) ─────────────────────────────
def mask_text(txt, font, xy, anchor='mm', size=(W, H), stroke=0):
    m = Image.new('L', size, 0)
    ImageDraw.Draw(m).text(xy, txt, font=font, fill=255, anchor=anchor, stroke_width=stroke, stroke_fill=255)
    return np.asarray(m, dtype=np.float32) / 255


def fit_font(path, txt, width, start):
    s = start
    while ImageFont.truetype(path, s).getlength(txt) > width:
        s -= 1
    return ImageFont.truetype(path, s)


f_big = fit_font(SANS, 'Website Designer', 780, 110)
f_small = ImageFont.truetype(SANS, 25)
big = mask_text('Website Designer', f_big, (W / 2, 238))
big_out = mask_text('Website Designer', f_big, (W / 2, 238), stroke=3)
shadow = np.asarray(Image.fromarray((big_out * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9)), dtype=np.float32) / 255
shadow = np.roll(shadow, 9, axis=0)
small_txt = 'M I D - L E V E L   ·   F U L L S T A C K'
small = mask_text(small_txt, f_small, (W / 2, 138))
small_out = mask_text(small_txt, f_small, (W / 2, 138), stroke=3)
yy, xx = np.mgrid[0:H, 0:W]
ys = np.where(big.any(axis=1))[0]
glass_lvl = np.clip(8.4 - 2.6 * (yy - ys.min()) / (ys.max() - ys.min()), 5.2, 8.4)   # branco em cima -> rosa embaixo

# anime: brilhos de 4 pontas (o "✦" de anime dos anos 90) espalhados pela seda
SPARKS = [(random.randrange(40, W - 40), random.randrange(40, H - 40), random.randrange(NF), random.choice([6, 8, 11]))
          for _ in range(40)]
SPARKS = [s for s in SPARKS if not (60 < s[0] < 840 and 100 < s[1] < 290)]


def sparkle(d, x, y, r):
    d.polygon([(x, y - r), (x + r * .18, y - r * .18), (x + r, y), (x + r * .18, y + r * .18),
               (x, y + r), (x - r * .18, y + r * .18), (x - r, y), (x - r * .18, y - r * .18)], fill=8)


def frame(i):
    p = 2 * np.pi * i / NF
    b, _ = silk(p)
    bg = dither(b * (NP - 1.4), BH, BW, 4)
    img = np.kron(bg, np.ones((2, 2), np.uint8))          # pixels gordos 2×2 (cara de PC-98)

    th = np.tile(bayer(4), (H // 4 + 1, W // 4 + 1))[:H, :W]
    img[(shadow * 0.85 > th) & (big_out < 0.5)] = 0       # sombra projetada, pontilhada
    img[(small_out > 0.5) & (small < 0.5)] = 1
    img[small > 0.5] = 7
    img[(big_out > 0.5) & (big < 0.5)] = 2                # contorno escuro do vidro
    glass = dither(glass_lvl, H, W, 4)
    # reflexo que atravessa o texto (vidro)
    sx = -300 + (W + 600) * ((i / NF) * 1.6 % 1.6)
    band = np.abs((xx - sx) + (yy - 238) * 0.5) < 34
    glass[band] = 8
    img[big > 0.5] = glass[big > 0.5]

    im = Image.fromarray(img, 'P')
    d = ImageDraw.Draw(im)
    # brilhos piscando
    for (x, y, ph, r) in SPARKS:
        k = math.sin(2 * math.pi * ((i + ph) % NF) / NF)
        if k > 0.35:
            sparkle(d, x, y, r * (k - 0.2))
    # Evangelion: cartão de episódio
    d.text((26, 22), 'EPISODE:16', font=ImageFont.truetype(SERIF, 22), fill=8)
    d.text((28, 50), '第十六話', font=ImageFont.truetype(JP, 14), fill=6)
    # VHS
    if (i // 6) % 2 == 0:
        d.text((W - 26, 22), '▶ PLAY', font=ImageFont.truetype(MONO, 18), fill=8, anchor='ra')
    d.text((W - 26, 46), 'SP', font=ImageFont.truetype(MONO, 14), fill=6, anchor='ra')
    d.text((26, H - 26), 'PM 7:50', font=ImageFont.truetype(MONO, 18), fill=8, anchor='ls')
    # katakana vertical: ウェブデザイナー (web designer)
    fj = ImageFont.truetype(JP, 15)
    for k, ch in enumerate('ウェブデザイナー'):
        d.text((W - 30, 100 + k * 19), ch, font=fj, fill=6, anchor='mm')
    # Cowboy Bebop: digitado no fim do loop
    msg = 'SEE YOU SPACE COWBOY...'
    n = max(0, min(len(msg), int((i - 14) * 1.2)))
    if n:
        d.text((W - 26, H - 26), msg[:n] + ('█' if n < len(msg) and i % 2 else ''),
               font=ImageFont.truetype(MONO, 15), fill=7, anchor='rs')

    a = np.array(im)
    # scanlines
    a[::3] = np.maximum(a[::3].astype(int) - 1, 0).astype(np.uint8)
    # tracking de VHS: algumas faixas escorregam por 3 quadros
    if 30 <= i < 33:
        rnd = random.Random(i)
        for _ in range(5):
            y0, hh = rnd.randrange(0, H - 20), rnd.randrange(3, 18)
            a[y0:y0 + hh] = np.roll(a[y0:y0 + hh], rnd.randrange(-40, 40), axis=1)
        y0 = rnd.randrange(0, H - 4)
        a[y0:y0 + 2] = 8
    out = Image.fromarray(a, 'P')
    out.putpalette(PAL_RGB + [0] * (768 - len(PAL_RGB)))
    return out


def main():
    frames = [frame(i) for i in range(NF)]
    frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=MS, loop=0, optimize=False, disposal=1)
    print('ok', OUT, os.path.getsize(OUT) // 1024, 'KB')


if __name__ == '__main__':
    main()
