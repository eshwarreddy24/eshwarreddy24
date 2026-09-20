#!/usr/bin/env python3
"""Build the animated GitHub profile header from the supplied smiling portrait."""

from __future__ import annotations

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "profile-source"
ASSET_DIR = ROOT / "profile-assets"
OUT_SVG = ASSET_DIR / "terminal-profile.svg"
OUT_JPG = ASSET_DIR / "portrait-smile.jpg"
META = ASSET_DIR / "portrait-source-meta.txt"

def load_portrait() -> bytes:
    parts = sorted(SOURCE_DIR.glob("portrait-smile.b64.*"))
    if not parts:
        raise SystemExit("No portrait source chunks found.")
    encoded = "".join(p.read_text(encoding="utf-8").strip() for p in parts)
    return base64.b64decode(encoded)

def svg_for(portrait_b64: str) -> str:
    return f'''<svg width="1200" height="650" viewBox="0 0 1200 650"
xmlns="http://www.w3.org/2000/svg" role="img"
aria-label="Eshwar Reddy animated procurement SAP AI profile">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#020711"/>
    <stop offset="100%" stop-color="#071426"/>
  </linearGradient>
  <linearGradient id="panel" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#0b1728"/>
    <stop offset="100%" stop-color="#08121f"/>
  </linearGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#22d3ee" stop-opacity="0"/>
    <stop offset="50%" stop-color="#22d3ee" stop-opacity=".44"/>
    <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="vfx" cx="50%" cy="48%" r="58%">
    <stop offset="0%" stop-color="#22d3ee" stop-opacity=".13"/>
    <stop offset="70%" stop-color="#2563eb" stop-opacity=".04"/>
    <stop offset="100%" stop-color="#000000" stop-opacity=".44"/>
  </radialGradient>
  <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="portraitGlow" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="-3" dy="0" stdDeviation="6" flood-color="#8b5cf6" flood-opacity=".62"/>
    <feDropShadow dx="3" dy="0" stdDeviation="7" flood-color="#22d3ee" flood-opacity=".70"/>
  </filter>
  <clipPath id="portraitClip"><rect x="50" y="120" width="425" height="455" rx="10"/></clipPath>
  <style>
    .mono{{font-family:"JetBrains Mono","SFMono-Regular",Consolas,"Liberation Mono",monospace}}
    .label{{fill:#78a7d8;font-size:14px}}
    .value{{fill:#eef6ff;font-size:15px;font-weight:600}}
    .cyan{{fill:#22d3ee}}
    .line{{stroke:#203956;stroke-width:1}}
    .dots{{stroke:#214565;stroke-width:1;stroke-dasharray:2 4}}
    @keyframes float3d{{0%,100%{{transform:translateY(0) scale(1.018) rotate(-.25deg)}}50%{{transform:translateY(-9px) scale(1.042) rotate(.3deg)}}}}
    @keyframes scanMove{{0%{{transform:translateY(-65px);opacity:0}}10%{{opacity:.88}}90%{{opacity:.88}}100%{{transform:translateY(500px);opacity:0}}}}
    @keyframes pulse{{0%,100%{{opacity:.38}}50%{{opacity:1}}}}
    @keyframes frameGlow{{0%,100%{{filter:drop-shadow(0 0 4px #22d3ee)}}50%{{filter:drop-shadow(0 0 14px #8b5cf6)}}}}
    @keyframes orbit{{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}
    @keyframes cursor{{0%,45%{{opacity:1}}46%,100%{{opacity:.15}}}}
    .face{{animation:float3d 7s ease-in-out infinite;transform-origin:260px 350px}}
    .scan{{animation:scanMove 5.6s linear infinite}}
    .live{{animation:pulse 2.2s ease-in-out infinite}}
    .frame{{animation:frameGlow 5s ease-in-out infinite}}
    .orbit{{animation:orbit 18s linear infinite;transform-origin:263px 345px}}
    .cursor{{animation:cursor 1.2s steps(1,end) infinite}}
  </style>
</defs>

<rect width="1200" height="650" fill="url(#bg)"/>
<rect x="22" y="20" width="1156" height="610" rx="20" fill="#07111f" stroke="#173a62" stroke-width="2"/>
<circle cx="54" cy="52" r="6" fill="#ff5f57"/>
<circle cx="76" cy="52" r="6" fill="#febc2e"/>
<circle cx="98" cy="52" r="6" fill="#28c840"/>
<text x="145" y="57" class="mono cyan" font-size="15">eshwar@github:~$</text>
<text x="303" y="57" class="mono" fill="#eef6ff" font-size="15">whoami</text>
<text x="1138" y="57" text-anchor="end" class="mono label">BUILD / LEARN / IMPROVE / REPEAT ∞</text>
<line x1="22" y1="76" x2="1178" y2="76" class="line"/>

<rect class="frame" x="42" y="104" width="445" height="492" rx="12" fill="url(#panel)" stroke="#22d3ee"/>
<text x="58" y="131" class="mono cyan" font-size="14" font-weight="700">PROFILE.VISUAL</text>
<text x="468" y="131" text-anchor="end" class="mono label" font-size="12">PHOTO / VFX / MOTION</text>

<g clip-path="url(#portraitClip)">
  <image class="face" x="50" y="120" width="425" height="483" preserveAspectRatio="xMidYMid slice"
         href="data:image/jpeg;base64,{portrait_b64}" filter="url(#portraitGlow)"/>
  <rect x="50" y="120" width="425" height="455" fill="url(#vfx)"/>
  <rect class="scan" x="50" y="120" width="425" height="45" fill="url(#scan)"/>
  <g class="orbit" opacity=".45">
    <ellipse cx="263" cy="345" rx="188" ry="213" fill="none" stroke="#22d3ee" stroke-width="1.1" stroke-dasharray="4 9"/>
    <circle cx="451" cy="345" r="3" fill="#a78bfa" filter="url(#glow)"/>
  </g>
</g>
<path d="M58 151 v-15 h15 M470 151 v-15 h-15 M58 560 v15 h15 M470 560 v15 h-15" fill="none" stroke="#22d3ee" stroke-width="2"/>
<text x="62" y="586" class="mono" fill="#6f8aac" font-size="10">PROCUREMENT • SAP • DATA • AI / LLM</text>

<rect x="505" y="104" width="653" height="492" rx="12" fill="url(#panel)" stroke="#24476a"/>
<text x="524" y="131" class="mono cyan" font-size="14" font-weight="700">SYSTEM.INFO</text>
<circle class="live" cx="908" cy="126" r="4" fill="#22c55e" filter="url(#glow)"/>
<text x="922" y="131" class="mono" fill="#22c55e" font-size="12" font-weight="700">LIVE</text>
<text x="1136" y="131" text-anchor="end" class="mono cyan" font-size="13" font-weight="700">@eshwarreddy24</text>
<line x1="505" y1="143" x2="1158" y2="143" class="line"/>

<g class="mono">
  <text x="524" y="178" class="label">Subject</text><line x1="586" y1="173" x2="825" y2="173" class="dots"/><text x="1138" y="178" text-anchor="end" class="value">Eshwar Reddy Gali</text>
  <text x="524" y="211" class="label">Role</text><line x1="566" y1="206" x2="790" y2="206" class="dots"/><text x="1138" y="211" text-anchor="end" class="value">Procurement &amp; P2P · SAP · Data · AI</text>
  <text x="524" y="244" class="label">Base</text><line x1="566" y1="239" x2="875" y2="239" class="dots"/><text x="1138" y="244" text-anchor="end" class="value">Bengaluru, India</text>
  <text x="524" y="277" class="label">Status</text><line x1="575" y1="272" x2="820" y2="272" class="dots"/><text x="1138" y="277" text-anchor="end" class="value">Building · Learning · Improving</text>
  <text x="524" y="310" class="label">Core.SAP</text><line x1="590" y1="305" x2="800" y2="305" class="dots"/><text x="1138" y="310" text-anchor="end" class="value">SAP Ariba · SAP MM/FI · Contract Compliance</text>
  <text x="524" y="343" class="label">Core.Data</text><line x1="600" y1="338" x2="820" y2="338" class="dots"/><text x="1138" y="343" text-anchor="end" class="value">SQL · Power BI · Tableau · Advanced Excel</text>
  <text x="524" y="376" class="label">Core.AI</text><line x1="585" y1="371" x2="820" y2="371" class="dots"/><text x="1138" y="376" text-anchor="end" class="value">OpenAI API · LLMs · Prompt Engineering · RAG</text>
  <text x="524" y="409" class="label">Focus</text><line x1="575" y1="404" x2="810" y2="404" class="dots"/><text x="1138" y="409" text-anchor="end" class="value">Smarter enterprise procurement workflows</text>
  <text x="524" y="442" class="label">LinkedIn</text><line x1="590" y1="437" x2="860" y2="437" class="dots"/><text x="1138" y="442" text-anchor="end" class="value">/in/eshwar-reddy-gali-</text>
  <text x="524" y="475" class="label">Instagram</text><line x1="600" y1="470" x2="875" y2="470" class="dots"/><text x="1138" y="475" text-anchor="end" class="value">@eshwarrxddy</text>
</g>

<line x1="524" y1="533" x2="1138" y2="533" class="line"/>
<circle cx="527" cy="558" r="3" fill="#22c55e"/>
<text x="537" y="562" class="mono" fill="#22c55e" font-size="10">ALL SYSTEMS NOMINAL</text>
<text x="1138" y="562" text-anchor="end" class="mono label" font-size="10">PROCUREMENT • SAP • DATA • AI</text>
</svg>'''

def main():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    raw = load_portrait()
    OUT_JPG.write_bytes(raw)
    b64 = base64.b64encode(raw).decode("ascii")
    OUT_SVG.write_text(svg_for(b64), encoding="utf-8")
    META.write_text(
        "Source: user-provided portrait transformed into a smiling cyber/VFX profile visual.\n"
        "Purpose: GitHub profile README header.\n"
        "Motion: SVG float, scan-line, orbital light, status pulse.\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT_SVG} and {OUT_JPG}")

if __name__ == "__main__":
    main()
