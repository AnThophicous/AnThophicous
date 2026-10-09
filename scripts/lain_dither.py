#!/usr/bin/env python3
"""Lain em 1-bit: dithering Atkinson + luz que se move + sombra projetada, sem fundo.

gera:
  assets/lain.png  -> estático, transparente (800x800)
  assets/lain.gif  -> animação de 5s, transparente (400x400)
  assets/lain.mp4  -> animação de 5s, fundo preto (800x800)  [mp4 não tem transparência]

uso:  python3 scripts/lain_dither.py     (precisa de numpy, pillow e ffmpeg)
"""
import math, os, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'assets')
N, FPS, T = 400, 30, 5.0
NF = int(FPS * T)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
rng = np.random.default_rng(7)
random.seed(7)

# pixel: 0 = transparente, 1 = preto, 2 = branco
CLEAR, BLACK, WHITE = 0, 1, 2


def shift(a, dy, dx, fill=0):
    """desloca um array sem 'dar a volta' nas bordas (diferente de np.roll)."""
    o = np.full_like(a, fill)
    H, W = a.shape
    o[max(dy, 0):H + min(dy, 0), max(dx, 0):W + min(dx, 0)] = \
        a[max(-dy, 0):H + min(-dy, 0), max(-dx, 0):W + min(-dx, 0)]
    return o


def blur(a, r):
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))
    return np.asarray(im, dtype=np.float32) / 255


def atkinson(a):
    """dithering de Atkinson (o do Macintosh clássico): espalha só 6/8 do erro => contraste forte."""
    a = a.astype(np.float64).copy()
    H, W = a.shape
    o = np.zeros((H, W), bool)
    for y in range(H):
        row = a[y]
        for x in range(W):
            old = row[x]
            new = old > 0.5
            o[y, x] = new
            e = (old - new) / 8
            if x + 1 < W: row[x + 1] += e
            if x + 2 < W: row[x + 2] += e
            if y + 1 < H:
                if x > 0: a[y + 1, x - 1] += e
                a[y + 1, x] += e
                if x + 1 < W: a[y + 1, x + 1] += e
            if y + 2 < H: a[y + 2, x] += e
    return o


def smooth(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


# ── análise da imagem original ──────────────────────────────────────────
src = Image.open(os.path.join(HERE, 'lain_src.png')).convert('RGBA').resize((N, N), Image.LANCZOS)
alpha = np.asarray(src.split()[3], dtype=np.float32) / 255
gray = np.asarray(src.convert('RGB').convert('L'), dtype=np.float32) / 255

# fundo = tudo que é transparente/branco e encosta na borda (os brancos dos olhos ficam)
mask = Image.fromarray((((alpha < 0.5) | (gray > 0.97)) * 255).astype(np.uint8)).copy()
for p in [(0, 0), (N - 1, 0), (0, N // 2), (N - 1, N // 2)]:
    if mask.getpixel(p) == 255:
        ImageDraw.floodfill(mask, p, 128)
fg = np.asarray(mask) != 128
fg_soft = blur(fg, N * 0.03)
outline = (np.asarray(Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))) > 127) & ~fg
dilated = fg | outline

hair = gray < 0.16
yy, xx = np.mgrid[0:N, 0:N] / N
base = np.clip((gray - 0.07) / 0.42, 0, 1) ** 0.85      # cabelo -> preto, pele -> claro
occlusion = blur(hair, N * 0.02)                          # sombra do cabelo na pele


def light(lx, ly, expo=1.0):
    """(lx, ly) = de onde a luz vem, em -1..1. devolve (brilho da Lain, intensidade da sombra)."""
    key = np.clip(0.92 - 0.55 * (lx * (xx - 0.5) + ly * (yy - 0.5)), 0.45, 1.08)
    v = base * key
    d = int(N * 0.018)
    edge = fg & ~shift(fg, int(round(-ly * d)), int(round(-lx * d)), True)
    v = np.clip(v + 0.9 * blur(edge, N * 0.006) * hair, 0, 1)      # luz de contorno no cabelo
    v = v * (1 - 0.45 * occlusion * (~hair))
    v = np.where(fg, v * expo, 0.5)
    cast = shift(fg_soft, int(-ly * N * 0.06), int(-lx * N * 0.08), 0.0)
    return np.clip(v, 0, 1), np.clip(cast * expo, 0, 1)


def compose(lum, cast, with_outline=True):
    subject = atkinson(lum)
    shadow = ~atkinson(1 - 0.7 * cast)
    c = np.zeros((N, N), np.uint8)
    c[shadow & ~dilated] = BLACK
    c[fg] = np.where(subject[fg], WHITE, BLACK)
    if with_outline:
        c[outline] = WHITE
    return c


# ── HUD ─────────────────────────────────────────────────────────────────
f_big, f_mid, f_sm = (ImageFont.truetype(FONT, s) for s in (22, 13, 10))


def label(d, xy, txt, font, inv=False):
    if not txt:
        return
    bb = d.textbbox(xy, txt, font=font)
    d.rectangle((bb[0] - 3, bb[1] - 2, bb[2] + 3, bb[3] + 2), fill=255 if inv else 0)
    d.text(xy, txt, font=font, fill=0 if inv else 255)


def typed(txt, t, t0, cps=14):
    if t < t0:
        return ''
    n = int((t - t0) * cps)
    return txt[:n] + ('_' if n < len(txt) and int(t * 8) % 2 == 0 else '')


def frame(i):
    t = i / FPS
    lx, ly = -0.9 * math.cos(t / T * 2 * math.pi), 0.75     # luz vai da esquerda pra direita e volta
    expo = 0.15 + 0.85 * smooth(t / 0.9)
    if t > 4.55:
        expo *= 1 + 2 * smooth((t - 4.55) / 0.3)
    lum, cast = light(lx, ly, expo)
    if t < 0.9:                                              # boot: "cabeça de leitura" descendo
        head = int(N * smooth(t / 0.9))
        noise = rng.random((N, N)) < 0.08
        lum = lum.copy()
        lum[head:] = np.where(noise[head:], 1.0, 0.0)
    c = compose(lum, cast, with_outline=t >= 0.9)

    for gt in (2.15, 3.7):                                   # glitches
        if gt <= t < gt + 0.22:
            for _ in range(6):
                y0, h = random.randrange(0, N - 30), random.randrange(3, 26)
                c[y0:y0 + h] = np.roll(c[y0:y0 + h], random.randrange(-60, 60), axis=1)
            y0 = random.randrange(0, N - 40)
            band = c[y0:y0 + random.randrange(4, 30)]
            band[band == BLACK] = 9
            band[band == WHITE] = BLACK
            band[band == 9] = WHITE
            if random.random() < 0.5:
                c = np.roll(c, random.choice([-3, 3]), axis=1)

    hud = Image.new('L', (N, N), 128)
    d = ImageDraw.Draw(hud)
    d.fontmode = '1'
    label(d, (10, 10), 'LAYER:01  WEIRD', f_sm)
    if int(t * 2) % 2 == 0:
        label(d, (N - 78, 10), '● WIRED', f_sm)
    label(d, (10, 32), typed('PRESENT DAY', t, 1.0), f_mid)
    label(d, (10, 52), typed('PRESENT TIME', t, 1.7), f_mid)
    if 2.75 <= t < 3.55:
        label(d, (N - 140 + random.randrange(-3, 4), 250 + random.randrange(-2, 3)),
              'HAHAHAHA', f_big, inv=int(t * 12) % 2 == 0)
    label(d, (10, N - 24), typed("let's all love lain", t, 3.0, 18), f_mid)
    label(d, (N - 128, N - 20), 'serial experiments', f_sm)
    hv = np.asarray(hud)
    c[hv == 0] = BLACK
    c[hv == 255] = WHITE

    if t > 4.7:                                              # desligando o CRT
        k = smooth((t - 4.7) / 0.3)
        h = max(1, int(N * (1 - k)))
        sq = np.asarray(Image.fromarray(c).resize((N, h), Image.NEAREST))
        c = np.zeros((N, N), np.uint8)
        y0 = (N - h) // 2
        c[y0:y0 + h] = sq
        if h < 6:
            w = int(N * (1 - k * 0.9))
            c[N // 2 - 1:N // 2 + 1, (N - w) // 2:(N + w) // 2] = WHITE
    return c


def main():
    os.makedirs(OUT, exist_ok=True)
    rgba = np.array([[0, 0, 0, 0], [0, 0, 0, 255], [255, 255, 255, 255]], np.uint8)

    lum, cast = light(-0.55, 0.75)
    Image.fromarray(rgba[compose(lum, cast)]).resize((800, 800), Image.NEAREST) \
        .save(os.path.join(OUT, 'lain.png'), optimize=True)

    frames = []
    for i in range(NF):
        frames.append(frame(i))
        print(f'\rframe {i + 1}/{NF}', end='', flush=True)
    print()

    gif = []
    for f in frames:
        im = Image.fromarray(f, 'P')
        im.putpalette([0, 0, 0, 0, 0, 0, 255, 255, 255] + [0] * (253 * 3))
        im.info['transparency'] = 0
        gif.append(im)
    gif[0].save(os.path.join(OUT, 'lain.gif'), save_all=True, append_images=gif[1:],
                duration=33, loop=0, transparency=0, disposal=2, optimize=False)

    lut = np.array([0, 0, 255], np.uint8)
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'gray',
                          '-s', f'{N}x{N}', '-r', str(FPS), '-i', '-', '-vf', 'scale=800:800:flags=neighbor',
                          '-c:v', 'libx264', '-crf', '14', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                          '-movflags', '+faststart', os.path.join(OUT, 'lain.mp4')], stdin=subprocess.PIPE)
    for f in frames:
        p.stdin.write(lut[f].tobytes())
    p.stdin.close()
    p.wait()


if __name__ == '__main__':
    main()
