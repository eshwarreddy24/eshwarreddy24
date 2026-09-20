#!/usr/bin/env python3
"""Generate an animated terminal-style GitHub profile card from the account avatar."""

from __future__ import annotations

import io
import math
import urllib.request
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

USERNAME = "eshwarreddy24"
AVATAR_URL = f"https://github.com/{USERNAME}.png?size=512"
OUT = Path("profile-assets/terminal-profile.svg")
META = Path("profile-assets/portrait-source-meta.txt")

COLS = 76
CELL = 4.35
PORTRAIT_X = 88
PORTRAIT_Y = 185
PORTRAIT_W = COLS * CELL


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def get_avatar() -> Image.Image:
    req = urllib.request.Request(
        AVATAR_URL,
        headers={"User-Agent": "eshwarreddy24-profile-generator/1.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        data = response.read()
    return Image.open(io.BytesIO(data)).convert("RGB")


def prepare_grid(img: Image.Image):
    img = ImageOps.exif_transpose(img)
    w, h = img.size
    side = min(w, h)

    # GitHub avatars are normally square. This also handles non-square source images.
    left = max(0, (w - side) // 2)
    top = max(0, (h - side) // 2)
    img = img.crop((left, top, left + side, top + side))

    gray = img.convert("L")
    gray = ImageOps.autocontrast(gray, cutoff=1)
    gray = ImageEnhance.Contrast(gray).enhance(1.28)
    gray = gray.filter(ImageFilter.UnsharpMask(radius=2.2, percent=145, threshold=2))

    edges = gray.filter(ImageFilter.FIND_EDGES)
    edges = ImageEnhance.Contrast(edges).enhance(1.45)

    rows = COLS
    g = gray.resize((COLS, rows), Image.Resampling.LANCZOS)
    e = edges.resize((COLS, rows), Image.Resampling.LANCZOS)

    # Infer whether the avatar background is generally light or dark from the border.
    px = g.load()
    border = []
    for x in range(COLS):
        border.extend((px[x, 0], px[x, rows - 1]))
    for y in range(rows):
        border.extend((px[0, y], px[COLS - 1, y]))
    border_mean = sum(border) / max(1, len(border)) / 255.0
    light_background = border_mean > 0.58

    return g, e, rows, light_background, border_mean


def dot_group(gray: Image.Image, edges: Image.Image, rows: int, light_background: bool) -> str:
    gp = gray.load()
    ep = edges.load()
    dots = []

    # Strong center bias keeps the portrait readable even if the avatar has a busy background.
    for y in range(rows):
        row_delay = y * 0.006
        for x in range(COLS):
            lum = gp[x, y] / 255.0
            edge = ep[x, y] / 255.0

            # On a light background use ink-like darkness; on a dark background use luminance.
            base = (1.0 - lum) if light_background else lum

            # Keep facial edges/detail even when local luminance is flat.
            v = min(1.0, base * 0.78 + edge * 0.72)

            nx = (x + 0.5) / COLS * 2.0 - 1.0
            ny = (y + 0.5) / rows * 2.0 - 1.0

            # Elliptical portrait vignette, slightly wider around shoulders.
            d = math.sqrt((nx / 0.98) ** 2 + ((ny + 0.04) / 1.08) ** 2)
            if d > 1.08:
                continue
            if d > 0.84:
                v *= max(0.0, (1.08 - d) / 0.24)

            # Preserve more density around the central face area.
            center_boost = max(0.0, 1.0 - math.sqrt((nx / 0.72) ** 2 + ((ny + 0.18) / 0.76) ** 2))
            v = min(1.0, v + 0.12 * center_boost)

            if v < 0.13:
                continue

            radius = 0.28 + (CELL * 0.44) * (v ** 1.08)
            cx = PORTRAIT_X + x * CELL + CELL / 2
            cy = PORTRAIT_Y + y * CELL + CELL / 2

            # Two-tone violet/steel terminal portrait, inspired by dot-matrix displays.
            fill = "#a9a3ff" if v > 0.55 else "#6670a7"
            opacity = 0.30 + 0.70 * v
            lane = x % 12
            dots.append(
                f'<circle class="dot lane{lane}" cx="{cx:.2f}" cy="{cy:.2f}" '
                f'r="{radius:.2f}" fill="{fill}" opacity="{opacity:.2f}" '
                f'style="animation-delay:{row_delay + lane * 0.035:.3f}s"/>'
            )
    return "".join(dots)


def build_svg(img: Image.Image) -> tuple[str, float]:
    gray, edges, rows, light_bg, border_mean = prepare_grid(img)
    dots = dot_group(gray, edges, rows, light_bg)

    svg = f'''<svg width="1200" height="650" viewBox="0 0 1200 650"
 xmlns="http://www.w3.org/2000/svg" role="img"
 aria-label="Eshwar Reddy animated terminal profile">
<defs>
  <linearGradient id="outerBg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#03070d"/>
    <stop offset="100%" stop-color="#09111d"/>
  </linearGradient>
  <linearGradient id="panelBg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#101b2d"/>
    <stop offset="100%" stop-color="#0d1726"/>
  </linearGradient>
  <linearGradient id="pill" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#0c3a4d"/>
    <stop offset="100%" stop-color="#125a73"/>
  </linearGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#22d3ee" stop-opacity="0"/>
    <stop offset="50%" stop-color="#22d3ee" stop-opacity=".36"/>
    <stop offset="100%" stop-color="#22d3ee" stop-opacity="0"/>
  </linearGradient>
  <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="4" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="portraitClip"><rect x="72" y="158" width="384" height="398" rx="4"/></clipPath>
  <style>
    .mono {{ font-family:"JetBrains Mono","SFMono-Regular",Consolas,"Liberation Mono",monospace; }}
    .label {{ fill:#7d9bc7; font-size:14px; }}
    .value {{ fill:#f3f7ff; font-size:15px; font-weight:600; }}
    .cyan {{ fill:#22d3ee; }}
    .muted {{ fill:#6f86a8; }}
    .line {{ stroke:#243652; stroke-width:1; }}
    .dotted {{ stroke:#26415e; stroke-width:1; stroke-dasharray:2 4; }}
    @keyframes pulse {{ 0%,100%{{opacity:.42}} 50%{{opacity:1}} }}
    @keyframes drift {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-2px)}} }}
    @keyframes scanner {{ 0%{{transform:translateY(-36px);opacity:0}} 12%{{opacity:.9}} 88%{{opacity:.9}} 100%{{transform:translateY(405px);opacity:0}} }}
    @keyframes blink {{ 0%,48%,100%{{opacity:1}} 49%,70%{{opacity:.2}} }}
    .dot {{ animation:pulse 4.8s ease-in-out infinite; }}
    .lane0{{animation-delay:0s}} .lane1{{animation-delay:.15s}} .lane2{{animation-delay:.30s}}
    .lane3{{animation-delay:.45s}} .lane4{{animation-delay:.60s}} .lane5{{animation-delay:.75s}}
    .lane6{{animation-delay:.90s}} .lane7{{animation-delay:1.05s}} .lane8{{animation-delay:1.20s}}
    .lane9{{animation-delay:1.35s}} .lane10{{animation-delay:1.50s}} .lane11{{animation-delay:1.65s}}
    .portrait {{ animation:drift 7s ease-in-out infinite; transform-origin:263px 350px; }}
    .scanline {{ animation:scanner 5.6s linear infinite; }}
    .live {{ animation:blink 2.3s steps(1,end) infinite; }}
  </style>
</defs>

<rect width="1200" height="650" fill="url(#outerBg)"/>
<rect x="22" y="18" width="1156" height="614" rx="18" fill="#0a1422" stroke="#1a2b44" stroke-width="2"/>
<rect x="34" y="30" width="1132" height="590" rx="14" fill="#0d1726" stroke="#263b59" stroke-width="1.5"/>

<!-- Terminal title bar -->
<circle cx="58" cy="55" r="6" fill="#ff5f57"/>
<circle cx="80" cy="55" r="6" fill="#febc2e"/>
<circle cx="102" cy="55" r="6" fill="#28c840"/>
<text x="600" y="60" text-anchor="middle" class="mono label" font-size="15">profile.sh --live</text>
<line x1="34" y1="78" x2="1166" y2="78" class="line"/>

<!-- Portrait panel -->
<rect x="56" y="105" width="414" height="480" rx="8" fill="url(#panelBg)" stroke="#29415f"/>
<text x="72" y="130" class="mono cyan" font-size="14" font-weight="700">VISUAL.MAP</text>
<text x="448" y="130" text-anchor="end" class="mono label" font-size="12">DOT MATRIX / LIVE</text>
<line x1="70" y1="142" x2="456" y2="142" class="line"/>
<path d="M70 170 v-12 h12" fill="none" stroke="#22d3ee" stroke-width="1.3"/>
<path d="M456 170 v-12 h-12" fill="none" stroke="#22d3ee" stroke-width="1.3"/>
<path d="M70 548 v12 h12" fill="none" stroke="#22d3ee" stroke-width="1.3"/>
<path d="M456 548 v12 h-12" fill="none" stroke="#22d3ee" stroke-width="1.3"/>

<g clip-path="url(#portraitClip)">
  <g class="portrait">{dots}</g>
  <rect class="scanline" x="72" y="158" width="384" height="34" fill="url(#scan)" opacity=".75"/>
</g>
<text x="78" y="570" class="mono muted" font-size="10">PTS {len(dots.split("<circle")) - 1} • /FS/ESHWR • AVATAR SYNC</text>

<!-- System panel -->
<rect x="490" y="105" width="654" height="480" rx="8" fill="url(#panelBg)" stroke="#29415f"/>
<text x="506" y="130" class="mono cyan" font-size="14" font-weight="700">SYSTEM.INFO</text>
<circle cx="908" cy="126" r="4" fill="#ff5470" filter="url(#glow)" class="live"/>
<text x="923" y="130" class="mono" fill="#ff5470" font-size="12" font-weight="700">LIVE</text>
<rect x="977" y="114" width="150" height="25" rx="13" fill="url(#pill)"/>
<text x="1052" y="131" text-anchor="middle" class="mono cyan" font-size="13" font-weight="700">@eshwarreddy24</text>
<line x1="490" y1="142" x2="1144" y2="142" class="line"/>

<g class="mono">
  <text x="506" y="171" class="label">Subject</text><line x1="565" y1="166" x2="825" y2="166" class="dotted"/><text x="1122" y="171" text-anchor="end" class="value">Eshwar Reddy Gali</text>
  <text x="506" y="194" class="label">Role</text><line x1="548" y1="189" x2="790" y2="189" class="dotted"/><text x="1122" y="194" text-anchor="end" class="value">P2P Analyst · SAP Ariba · AI / LLM Builder</text>
  <text x="506" y="217" class="label">Base</text><line x1="548" y1="212" x2="880" y2="212" class="dotted"/><text x="1122" y="217" text-anchor="end" class="value">Bengaluru · India</text>
  <text x="506" y="240" class="label">Focus</text><line x1="556" y1="235" x2="785" y2="235" class="dotted"/><text x="1122" y="240" text-anchor="end" class="value">Procurement · Contract Compliance · Automation</text>
  <text x="506" y="263" class="label">Status</text><line x1="565" y1="258" x2="815" y2="258" class="dotted"/><text x="1122" y="263" text-anchor="end" class="value">Building + Learning + Shipping</text>
  <text x="506" y="286" class="label">ToolChain</text><line x1="583" y1="281" x2="788" y2="281" class="dotted"/><text x="1122" y="286" text-anchor="end" class="value">SAP Ariba · Excel · Power BI · GitHub</text>
  <text x="506" y="309" class="label">Core.SAP</text><line x1="575" y1="304" x2="798" y2="304" class="dotted"/><text x="1122" y="309" text-anchor="end" class="value">Contract Compliance · Buying &amp; Invoicing · MM/FI</text>
  <text x="506" y="332" class="label">Core.P2P</text><line x1="576" y1="327" x2="820" y2="327" class="dotted"/><text x="1122" y="332" text-anchor="end" class="value">Contracts · Requisitions · PO · Receiving · Invoice</text>
  <text x="506" y="355" class="label">Core.Data</text><line x1="584" y1="350" x2="835" y2="350" class="dotted"/><text x="1122" y="355" text-anchor="end" class="value">Advanced Excel · Power BI · Reconciliation</text>
  <text x="506" y="378" class="label">Core.AI</text><line x1="570" y1="373" x2="835" y2="373" class="dotted"/><text x="1122" y="378" text-anchor="end" class="value">Prompt Engineering · RAG · Agents · Evaluation</text>
  <text x="506" y="401" class="label">AI.Assist</text><line x1="585" y1="396" x2="850" y2="396" class="dotted"/><text x="1122" y="401" text-anchor="end" class="value">ChatGPT · Microsoft Copilot · Human Review</text>
  <text x="506" y="424" class="label">Grid.Mail</text><line x1="577" y1="419" x2="835" y2="419" class="dotted"/><text x="1122" y="424" text-anchor="end" class="value">eshwarreddy.gali@outlook.com</text>
  <text x="506" y="447" class="label">Grid.LinkedIn</text><line x1="607" y1="442" x2="833" y2="442" class="dotted"/><text x="1122" y="447" text-anchor="end" class="value">/in/eshwar-reddy-gali-</text>
  <text x="506" y="470" class="label">Grid.GitHub</text><line x1="596" y1="465" x2="885" y2="465" class="dotted"/><text x="1122" y="470" text-anchor="end" class="value">@eshwarreddy24</text>
  <text x="506" y="493" class="label">Grid.Instagram</text><line x1="620" y1="488" x2="890" y2="488" class="dotted"/><text x="1122" y="493" text-anchor="end" class="value">@eshwarrxddy</text>
  <text x="506" y="516" class="label">Mission</text><line x1="564" y1="511" x2="800" y2="511" class="dotted"/><text x="1122" y="516" text-anchor="end" class="value">Smarter enterprise procurement with controlled AI</text>
</g>

<line x1="506" y1="548" x2="1128" y2="548" class="line"/>
<circle cx="510" cy="565" r="3" fill="#22c55e"/>
<text x="520" y="569" class="mono" fill="#22c55e" font-size="11">ALL SYSTEMS NOMINAL</text>
<text x="1128" y="569" text-anchor="end" class="mono label" font-size="11">UTC+5:30 • BLR MODE</text>
</svg>'''
    return svg, border_mean


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = get_avatar()
    svg, border_mean = build_svg(img)
    OUT.write_text(svg, encoding="utf-8")
    META.write_text(
        "Generated from the public GitHub avatar for @eshwarreddy24\n"
        f"source={AVATAR_URL}\n"
        f"source_size={img.size[0]}x{img.size[1]}\n"
        f"grid={COLS}x{COLS}\n"
        f"border_luminance={border_mean:.3f}\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
