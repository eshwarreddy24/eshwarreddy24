#!/usr/bin/env python3
"""Build a monochrome terminal-style animated GitHub profile header."""

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
aria-label="Eshwar Reddy animated terminal profile">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#05080d"/>
    <stop offset="100%" stop-color="#0a1018"/>
  </linearGradient>
  <linearGradient id="panel" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#101826"/>
    <stop offset="100%" stop-color="#0d1420"/>
  </linearGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#d7dde6" stop-opacity="0"/>
    <stop offset="50%" stop-color="#d7dde6" stop-opacity=".20"/>
    <stop offset="100%" stop-color="#d7dde6" stop-opacity="0"/>
  </linearGradient>
  <filter id="mono" x="-10%" y="-10%" width="120%" height="120%">
    <feColorMatrix type="matrix"
      values="0.33 0.33 0.33 0 0
              0.33 0.33 0.33 0 0
              0.33 0.33 0.33 0 0
              0    0    0    1 0"/>
    <feComponentTransfer>
      <feFuncR type="gamma" amplitude="1.0" exponent="1.15" offset="0"/>
      <feFuncG type="gamma" amplitude="1.0" exponent="1.15" offset="0"/>
      <feFuncB type="gamma" amplitude="1.0" exponent="1.15" offset="0"/>
    </feComponentTransfer>
  </filter>
  <pattern id="dotPattern" width="5" height="5" patternUnits="userSpaceOnUse">
    <circle cx="2.5" cy="2.5" r="0.8" fill="#b8bec8" opacity=".72"/>
  </pattern>
  <mask id="portraitDots">
    <rect x="0" y="0" width="100%" height="100%" fill="black"/>
    <image x="76" y="178" width="340" height="365" preserveAspectRatio="xMidYMid slice"
      href="data:image/jpeg;base64,{portrait_b64}" filter="url(#mono)"/>
  </mask>
  <clipPath id="portraitClip"><rect x="62" y="154" width="392" height="405" rx="3"/></clipPath>
  <style>
    .mono{{font-family:"JetBrains Mono","SFMono-Regular",Consolas,"Liberation Mono",monospace}}
    .label{{fill:#8492a8;font-size:14px}}
    .value{{fill:#f3f5f7;font-size:15px;font-weight:600}}
    .accent{{fill:#c7d0dc}}
    .muted{{fill:#68778c}}
    .line{{stroke:#2a394d;stroke-width:1}}
    .dotted{{stroke:#26364a;stroke-width:1;stroke-dasharray:2 4}}

    /* 10 second loop. Each cross-fade is exactly 6% = 0.60 seconds. */
    @keyframes phaseOne{{
      0%,44%{{opacity:1}}
      50%,94%{{opacity:0}}
      100%{{opacity:1}}
    }}
    @keyframes phaseTwo{{
      0%,44%{{opacity:0}}
      50%,94%{{opacity:1}}
      100%{{opacity:0}}
    }}
    @keyframes scanMove{{
      0%{{transform:translateY(-46px);opacity:0}}
      10%{{opacity:.50}}
      90%{{opacity:.50}}
      100%{{transform:translateY(430px);opacity:0}}
    }}
    @keyframes pulse{{0%,100%{{opacity:.42}}50%{{opacity:1}}}}
    @keyframes welcomeIn{{0%,100%{{letter-spacing:4px;opacity:.88}}50%{{letter-spacing:7px;opacity:1}}}}

    .phase-one{{animation:phaseOne 10s linear infinite}}
    .phase-two{{animation:phaseTwo 10s linear infinite;opacity:0}}
    .scan{{animation:scanMove 5.8s linear infinite}}
    .live{{animation:pulse 2.4s ease-in-out infinite}}
    .welcome{{animation:welcomeIn 4s ease-in-out infinite}}
  </style>
</defs>

<rect width="1200" height="650" fill="url(#bg)"/>
<rect x="20" y="18" width="1160" height="614" rx="18" fill="#0a111c" stroke="#1c2a3d" stroke-width="2"/>
<rect x="32" y="30" width="1136" height="590" rx="14" fill="#0d1522" stroke="#2b3a50" stroke-width="1.5"/>

<!-- terminal bar -->
<circle cx="56" cy="54" r="6" fill="#d6d6d6"/>
<circle cx="78" cy="54" r="6" fill="#9fa5ad"/>
<circle cx="100" cy="54" r="6" fill="#737b85"/>
<text x="600" y="59" text-anchor="middle" class="mono label" font-size="15">profile.sh --live</text>
<line x1="32" y1="78" x2="1168" y2="78" class="line"/>

<!-- PHASE 1: reference-style profile card -->
<g class="phase-one">
  <rect x="42" y="104" width="430" height="482" rx="8" fill="url(#panel)" stroke="#29394f"/>
  <text x="56" y="131" class="mono accent" font-size="14" font-weight="700">VISUAL.MAP</text>
  <text x="454" y="131" text-anchor="end" class="mono label" font-size="11">320x340 / 1-BIT</text>
  <line x1="56" y1="143" x2="458" y2="143" class="line"/>

  <path d="M56 174 v-13 h13 M458 174 v-13 h-13 M56 544 v13 h13 M458 544 v13 h-13"
        fill="none" stroke="#78879a" stroke-width="1.2"/>

  <!-- monochrome dot portrait -->
  <g clip-path="url(#portraitClip)">
    <image x="76" y="178" width="340" height="365" preserveAspectRatio="xMidYMid slice"
      href="data:image/jpeg;base64,{portrait_b64}" filter="url(#mono)" opacity=".16"/>
    <rect x="62" y="154" width="392" height="405" fill="url(#dotPattern)" mask="url(#portraitDots)" opacity=".95"/>
    <rect class="scan" x="62" y="154" width="392" height="36" fill="url(#scan)"/>
  </g>
  <text x="66" y="572" class="mono muted" font-size="10">PTS / PROFILE • FS/ESHWR</text>

  <rect x="492" y="104" width="654" height="482" rx="8" fill="url(#panel)" stroke="#29394f"/>
  <text x="508" y="131" class="mono accent" font-size="14" font-weight="700">SYSTEM.INFO</text>
  <circle class="live" cx="904" cy="126" r="4" fill="#d7dde6"/>
  <text x="918" y="131" class="mono accent" font-size="12" font-weight="700">LIVE</text>
  <rect x="984" y="113" width="146" height="26" rx="13" fill="#172233" stroke="#314359"/>
  <text x="1057" y="131" text-anchor="middle" class="mono accent" font-size="13" font-weight="700">@eshwarreddy24</text>
  <line x1="492" y1="143" x2="1146" y2="143" class="line"/>

  <g class="mono">
    <text x="508" y="173" class="label">Subject</text><line x1="570" y1="168" x2="825" y2="168" class="dotted"/><text x="1128" y="173" text-anchor="end" class="value">Eshwar Reddy Gali</text>
    <text x="508" y="198" class="label">Role</text><line x1="550" y1="193" x2="790" y2="193" class="dotted"/><text x="1128" y="198" text-anchor="end" class="value">Procurement &amp; P2P · SAP · Data · AI</text>
    <text x="508" y="223" class="label">Origin</text><line x1="560" y1="218" x2="875" y2="218" class="dotted"/><text x="1128" y="223" text-anchor="end" class="value">Bengaluru · India</text>
    <text x="508" y="248" class="label">Status</text><line x1="560" y1="243" x2="820" y2="243" class="dotted"/><text x="1128" y="248" text-anchor="end" class="value">Building + Learning + Improving</text>
    <text x="508" y="273" class="label">ToolChain</text><line x1="580" y1="268" x2="790" y2="268" class="dotted"/><text x="1128" y="273" text-anchor="end" class="value">SAP Ariba · Excel · Power BI · GitHub</text>
    <text x="508" y="298" class="label">Core.SAP</text><line x1="575" y1="293" x2="798" y2="293" class="dotted"/><text x="1128" y="298" text-anchor="end" class="value">Contract Compliance · SAP MM/FI</text>
    <text x="508" y="323" class="label">Core.P2P</text><line x1="575" y1="318" x2="820" y2="318" class="dotted"/><text x="1128" y="323" text-anchor="end" class="value">Contracts · Requisitions · PO · Receiving</text>
    <text x="508" y="348" class="label">Core.Data</text><line x1="585" y1="343" x2="830" y2="343" class="dotted"/><text x="1128" y="348" text-anchor="end" class="value">SQL · Power BI · Tableau · Advanced Excel</text>
    <text x="508" y="373" class="label">Core.AI</text><line x1="570" y1="368" x2="820" y2="368" class="dotted"/><text x="1128" y="373" text-anchor="end" class="value">OpenAI API · LLMs · Prompt Engineering · RAG</text>
    <text x="508" y="398" class="label">Grid.LinkedIn</text><line x1="610" y1="393" x2="835" y2="393" class="dotted"/><text x="1128" y="398" text-anchor="end" class="value">/in/eshwar-reddy-gali-</text>
    <text x="508" y="423" class="label">Grid.GitHub</text><line x1="595" y1="418" x2="875" y2="418" class="dotted"/><text x="1128" y="423" text-anchor="end" class="value">eshwarreddy24</text>
    <text x="508" y="448" class="label">Grid.Instagram</text><line x1="620" y1="443" x2="880" y2="443" class="dotted"/><text x="1128" y="448" text-anchor="end" class="value">@eshwarrxddy</text>
  </g>

  <line x1="508" y1="534" x2="1128" y2="534" class="line"/>
  <circle cx="512" cy="558" r="3" fill="#c5ccd5"/>
  <text x="522" y="562" class="mono accent" font-size="10">ALL SYSTEMS NOMINAL</text>
  <text x="1128" y="562" text-anchor="end" class="mono label" font-size="10">UTC+5:30 • BLR MODE</text>
</g>

<!-- PHASE 2: clean monochrome welcome scene -->
<g class="phase-two">
  <rect x="42" y="104" width="1104" height="482" rx="8" fill="url(#panel)" stroke="#29394f"/>
  <text x="58" y="131" class="mono accent" font-size="14" font-weight="700">WELCOME.SYS</text>
  <text x="1128" y="131" text-anchor="end" class="mono label" font-size="11">SESSION / ACTIVE</text>
  <line x1="56" y1="143" x2="1132" y2="143" class="line"/>

  <path d="M74 185 h34 M74 185 v34 M1128 185 h-34 M1128 185 v34 M74 520 h34 M74 520 v-34 M1128 520 h-34 M1128 520 v-34"
        fill="none" stroke="#566578" stroke-width="1.2"/>

  <text x="600" y="265" text-anchor="middle" class="mono label" font-size="15" letter-spacing="6">PROCUREMENT  •  SAP  •  DATA  •  AI</text>
  <text x="600" y="350" text-anchor="middle" class="mono value welcome" font-size="62" font-weight="800">Welcome to my world</text>
  <line x1="365" y1="382" x2="835" y2="382" stroke="#5b6979" stroke-width="1"/>
  <text x="600" y="425" text-anchor="middle" class="mono label" font-size="14" letter-spacing="3">BUILD USEFUL THINGS · KEEP LEARNING · IMPROVE SYSTEMS</text>

  <g class="mono">
    <text x="600" y="492" text-anchor="middle" class="muted" font-size="12">CONTRACT COMPLIANCE · P2P ANALYTICS · ENTERPRISE AUTOMATION · LLM WORKFLOWS</text>
  </g>
  <circle cx="512" cy="558" r="3" fill="#c5ccd5"/>
  <text x="522" y="562" class="mono accent" font-size="10">WELCOME SEQUENCE COMPLETE</text>
  <text x="1128" y="562" text-anchor="end" class="mono label" font-size="10">LOOP / 10.00s • FADE / 0.60s</text>
</g>
</svg>'''

def main():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    raw = load_portrait()
    OUT_JPG.write_bytes(raw)
    b64 = base64.b64encode(raw).decode("ascii")
    OUT_SVG.write_text(svg_for(b64), encoding="utf-8")
    META.write_text(
        "Source: user-provided portrait.\n"
        "Style: monochrome terminal profile with reference-inspired layout.\n"
        "Animation: profile view cross-fades to 'Welcome to my world'.\n"
        "Transition duration: 0.60 seconds in a 10-second loop.\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT_SVG} and {OUT_JPG}")

if __name__ == "__main__":
    main()
