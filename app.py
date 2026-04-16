"""
🌱 ACP Engineer — Agent Agronom AI PRO
Powered by Claude (Anthropic)
"""

import streamlit as st
import anthropic
import base64
import sqlite3
import json
from datetime import datetime, date
from fpdf import FPDF

# ═══════════════════════════════════════════════════════════════════
# CONFIGURARE
# ═══════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="ACP Engineer — Agronom AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

APP_PASSWORD = "ACPengineer"
CLAUDE_MODEL  = "claude-opus-4-6"

# ═══════════════════════════════════════════════════════════════════
# SVG ILUSTRAȚII CULTURI
# ═══════════════════════════════════════════════════════════════════

SVG_GRAU = """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="140" rx="10" fill="#fef9e7"/>
  <!-- Sol -->
  <ellipse cx="60" cy="130" rx="45" ry="8" fill="#8B6914" opacity="0.3"/>
  <!-- Tulpina stanga -->
  <path d="M35 125 Q33 90 38 60 Q42 30 40 10" stroke="#5d8a3c" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <!-- Tulpina centrala -->
  <path d="M60 128 Q58 90 62 55 Q65 25 63 5" stroke="#5d8a3c" stroke-width="3" fill="none" stroke-linecap="round"/>
  <!-- Tulpina dreapta -->
  <path d="M85 125 Q87 90 82 60 Q78 30 80 10" stroke="#5d8a3c" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <!-- Spic stanga -->
  <ellipse cx="38" cy="12" rx="5" ry="16" fill="#f4d03f" transform="rotate(-8,38,12)"/>
  <ellipse cx="34" cy="16" rx="4" ry="10" fill="#e8c21a" transform="rotate(-20,34,16)"/>
  <ellipse cx="42" cy="16" rx="4" ry="10" fill="#e8c21a" transform="rotate(12,42,16)"/>
  <!-- Spic central -->
  <ellipse cx="63" cy="7" rx="6" ry="20" fill="#f4d03f" transform="rotate(-3,63,7)"/>
  <ellipse cx="57" cy="12" rx="5" ry="12" fill="#e8c21a" transform="rotate(-18,57,12)"/>
  <ellipse cx="69" cy="12" rx="5" ry="12" fill="#e8c21a" transform="rotate(15,69,12)"/>
  <!-- Spic dreapta -->
  <ellipse cx="80" cy="12" rx="5" ry="16" fill="#f4d03f" transform="rotate(8,80,12)"/>
  <ellipse cx="76" cy="16" rx="4" ry="10" fill="#e8c21a" transform="rotate(-12,76,16)"/>
  <ellipse cx="84" cy="16" rx="4" ry="10" fill="#e8c21a" transform="rotate(20,84,16)"/>
  <!-- Frunze -->
  <path d="M60 70 Q45 60 30 65" stroke="#74c69d" stroke-width="2" fill="none"/>
  <path d="M60 80 Q75 68 88 72" stroke="#74c69d" stroke-width="2" fill="none"/>
  <!-- Mustati spic -->
  <line x1="63" y1="2" x2="63" y2="-8" stroke="#8B6914" stroke-width="1" opacity="0.6"/>
  <line x1="59" y1="4" x2="56" y2="-5" stroke="#8B6914" stroke-width="1" opacity="0.6"/>
  <line x1="67" y1="4" x2="70" y2="-5" stroke="#8B6914" stroke-width="1" opacity="0.6"/>
</svg>"""

SVG_ORZ = """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="140" rx="10" fill="#f0f9e8"/>
  <ellipse cx="60" cy="130" rx="45" ry="8" fill="#8B6914" opacity="0.3"/>
  <!-- Tulpini -->
  <path d="M40 126 Q38 85 42 50 Q45 20 43 5" stroke="#4a7c2f" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M60 128 Q60 88 63 52 Q65 22 64 4" stroke="#4a7c2f" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M80 126 Q82 85 78 50 Q75 20 77 5" stroke="#4a7c2f" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <!-- Spice orz cu mustati lungi -->
  <ellipse cx="43" cy="10" rx="4" ry="14" fill="#a8d5a2"/>
  <line x1="43" y1="-2" x2="35" y2="-18" stroke="#5d8a3c" stroke-width="1.2"/>
  <line x1="43" y1="2" x2="35" y2="-10" stroke="#5d8a3c" stroke-width="1.2"/>
  <line x1="43" y1="6" x2="35" y2="-2" stroke="#5d8a3c" stroke-width="1.2"/>
  <line x1="43" y1="10" x2="35" y2="6" stroke="#5d8a3c" stroke-width="1.2"/>
  <line x1="43" y1="-2" x2="51" y2="-18" stroke="#5d8a3c" stroke-width="1.2"/>
  <line x1="43" y1="2" x2="51" y2="-10" stroke="#5d8a3c" stroke-width="1.2"/>
  <line x1="43" y1="6" x2="51" y2="-2" stroke="#5d8a3c" stroke-width="1.2"/>
  <!-- Spic central -->
  <ellipse cx="64" cy="8" rx="5" ry="17" fill="#a8d5a2"/>
  <line x1="64" y1="-6" x2="55" y2="-22" stroke="#5d8a3c" stroke-width="1.2"/>
  <line x1="64" y1="-2" x2="55" y2="-14" stroke="#5d8a3c" stroke-width="1.2"/>
  <line x1="64" y1="3" x2="55" y2="-5" stroke="#5d8a3c" stroke-width="1.2"/>
  <line x1="64" y1="-6" x2="73" y2="-22" stroke="#5d8a3c" stroke-width="1.2"/>
  <line x1="64" y1="-2" x2="73" y2="-14" stroke="#5d8a3c" stroke-width="1.2"/>
  <line x1="64" y1="3" x2="73" y2="-5" stroke="#5d8a3c" stroke-width="1.2"/>
  <!-- Spic dreapta -->
  <ellipse cx="77" cy="10" rx="4" ry="14" fill="#a8d5a2"/>
  <line x1="77" y1="-2" x2="69" y2="-18" stroke="#5d8a3c" stroke-width="1.2"/>
  <line x1="77" y1="2" x2="69" y2="-10" stroke="#5d8a3c" stroke-width="1.2"/>
  <line x1="77" y1="-2" x2="85" y2="-18" stroke="#5d8a3c" stroke-width="1.2"/>
  <line x1="77" y1="2" x2="85" y2="-10" stroke="#5d8a3c" stroke-width="1.2"/>
  <!-- Frunze -->
  <path d="M60 75 Q42 62 28 68" stroke="#74c69d" stroke-width="2" fill="none"/>
  <path d="M60 85 Q78 70 92 75" stroke="#74c69d" stroke-width="2" fill="none"/>
</svg>"""

SVG_RAPITA = """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="140" rx="10" fill="#fffde7"/>
  <ellipse cx="60" cy="130" rx="45" ry="8" fill="#5d4037" opacity="0.3"/>
  <!-- Tulpina principala -->
  <path d="M60 128 Q58 95 60 65 Q61 40 60 10" stroke="#2e7d32" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <!-- Ramuri -->
  <path d="M60 75 Q45 68 35 55" stroke="#2e7d32" stroke-width="2" fill="none"/>
  <path d="M60 60 Q75 52 85 40" stroke="#2e7d32" stroke-width="2" fill="none"/>
  <path d="M60 90 Q42 85 30 78" stroke="#2e7d32" stroke-width="2" fill="none"/>
  <path d="M60 85 Q78 78 90 70" stroke="#2e7d32" stroke-width="2" fill="none"/>
  <!-- Flori galbene pe varf -->
  <circle cx="60" cy="10" r="6" fill="#f9ca24"/>
  <circle cx="54" cy="14" r="5" fill="#f9ca24"/>
  <circle cx="66" cy="14" r="5" fill="#f9ca24"/>
  <circle cx="58" cy="20" r="4" fill="#f0b429"/>
  <circle cx="62" cy="20" r="4" fill="#f0b429"/>
  <!-- Flori pe ramuri -->
  <circle cx="35" cy="55" r="5" fill="#f9ca24"/>
  <circle cx="30" cy="60" r="4" fill="#f9ca24"/>
  <circle cx="85" cy="40" r="5" fill="#f9ca24"/>
  <circle cx="90" cy="45" r="4" fill="#f9ca24"/>
  <circle cx="30" cy="78" r="4" fill="#f0b429"/>
  <circle cx="90" cy="70" r="4" fill="#f0b429"/>
  <!-- Frunze mari la baza -->
  <ellipse cx="42" cy="105" rx="20" ry="10" fill="#388e3c" transform="rotate(-20,42,105)" opacity="0.8"/>
  <ellipse cx="78" cy="108" rx="18" ry="9" fill="#2e7d32" transform="rotate(15,78,108)" opacity="0.8"/>
  <!-- Siliqve (pastai) -->
  <rect x="34" y="58" width="3" height="14" rx="1.5" fill="#8bc34a" transform="rotate(-30,34,58)"/>
  <rect x="84" y="43" width="3" height="14" rx="1.5" fill="#8bc34a" transform="rotate(25,84,43)"/>
</svg>"""

SVG_LUCERNA = """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="140" rx="10" fill="#f3e5f5"/>
  <ellipse cx="60" cy="132" rx="45" ry="7" fill="#5d4037" opacity="0.3"/>
  <!-- Multiple tulpini -->
  <path d="M45 130 Q43 100 47 70 Q50 45 48 20" stroke="#388e3c" stroke-width="2" fill="none"/>
  <path d="M60 132 Q60 100 62 68 Q64 42 62 15" stroke="#2e7d32" stroke-width="2.5" fill="none"/>
  <path d="M75 130 Q77 100 73 70 Q70 45 72 20" stroke="#388e3c" stroke-width="2" fill="none"/>
  <!-- Flori mov -->
  <ellipse cx="48" cy="22" rx="8" ry="12" fill="#9c27b0" opacity="0.8"/>
  <ellipse cx="48" cy="18" rx="6" ry="8" fill="#ab47bc"/>
  <ellipse cx="62" cy="17" rx="9" ry="13" fill="#7b1fa2" opacity="0.9"/>
  <ellipse cx="62" cy="13" rx="7" ry="9" fill="#9c27b0"/>
  <ellipse cx="72" cy="22" rx="8" ry="12" fill="#8e24aa" opacity="0.8"/>
  <ellipse cx="72" cy="18" rx="6" ry="8" fill="#ab47bc"/>
  <!-- Flori mici detaliu -->
  <circle cx="44" cy="14" r="3" fill="#ce93d8"/>
  <circle cx="52" cy="14" r="3" fill="#ce93d8"/>
  <circle cx="58" cy="10" r="3" fill="#ce93d8"/>
  <circle cx="66" cy="10" r="3" fill="#ce93d8"/>
  <!-- Frunze trifoliate -->
  <ellipse cx="38" cy="75" rx="10" ry="6" fill="#4caf50" transform="rotate(-30,38,75)"/>
  <ellipse cx="44" cy="70" rx="10" ry="6" fill="#66bb6a" transform="rotate(-10,44,70)"/>
  <ellipse cx="50" cy="74" rx="10" ry="6" fill="#4caf50" transform="rotate(20,50,74)"/>
  <ellipse cx="72" cy="78" rx="10" ry="6" fill="#4caf50" transform="rotate(-20,72,78)"/>
  <ellipse cx="78" cy="73" rx="10" ry="6" fill="#66bb6a" transform="rotate(10,78,73)"/>
  <ellipse cx="84" cy="77" rx="10" ry="6" fill="#4caf50" transform="rotate(30,84,77)"/>
  <!-- Sol cu radacini -->
  <path d="M60 132 Q55 138 50 142" stroke="#795548" stroke-width="1.5" fill="none" opacity="0.5"/>
  <path d="M60 132 Q65 138 70 142" stroke="#795548" stroke-width="1.5" fill="none" opacity="0.5"/>
</svg>"""

SVG_FLOAREA_SOARELUI = """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="140" rx="10" fill="#fff8e1"/>
  <ellipse cx="60" cy="132" rx="40" ry="7" fill="#5d4037" opacity="0.35"/>
  <!-- Tulpina groasa -->
  <path d="M60 132 Q57 100 59 70 Q60 45 60 30" stroke="#33691e" stroke-width="5" fill="none" stroke-linecap="round"/>
  <!-- Frunze mari -->
  <ellipse cx="38" cy="95" rx="22" ry="12" fill="#558b2f" transform="rotate(-35,38,95)" opacity="0.9"/>
  <ellipse cx="82" cy="85" rx="22" ry="12" fill="#689f38" transform="rotate(30,82,85)" opacity="0.9"/>
  <ellipse cx="35" cy="70" rx="18" ry="10" fill="#558b2f" transform="rotate(-25,35,70)" opacity="0.8"/>
  <ellipse cx="85" cy="65" rx="18" ry="10" fill="#689f38" transform="rotate(20,85,65)" opacity="0.8"/>
  <!-- Petale galbene -->
  <ellipse cx="60" cy="12" rx="7" ry="16" fill="#fdd835"/>
  <ellipse cx="60" cy="12" rx="7" ry="16" fill="#fdd835" transform="rotate(30,60,30)"/>
  <ellipse cx="60" cy="12" rx="7" ry="16" fill="#f9a825" transform="rotate(60,60,30)"/>
  <ellipse cx="60" cy="12" rx="7" ry="16" fill="#fdd835" transform="rotate(90,60,30)"/>
  <ellipse cx="60" cy="12" rx="7" ry="16" fill="#f9a825" transform="rotate(120,60,30)"/>
  <ellipse cx="60" cy="12" rx="7" ry="16" fill="#fdd835" transform="rotate(150,60,30)"/>
  <ellipse cx="60" cy="12" rx="7" ry="16" fill="#f9a825" transform="rotate(180,60,30)"/>
  <ellipse cx="60" cy="12" rx="7" ry="16" fill="#fdd835" transform="rotate(210,60,30)"/>
  <ellipse cx="60" cy="12" rx="7" ry="16" fill="#f9a825" transform="rotate(240,60,30)"/>
  <ellipse cx="60" cy="12" rx="7" ry="16" fill="#fdd835" transform="rotate(270,60,30)"/>
  <ellipse cx="60" cy="12" rx="7" ry="16" fill="#f9a825" transform="rotate(300,60,30)"/>
  <ellipse cx="60" cy="12" rx="7" ry="16" fill="#fdd835" transform="rotate(330,60,30)"/>
  <!-- Centrul floarea -->
  <circle cx="60" cy="30" r="16" fill="#4e342e"/>
  <circle cx="60" cy="30" r="12" fill="#3e2723"/>
  <!-- Seminte pattern -->
  <circle cx="56" cy="27" r="1.5" fill="#6d4c41"/>
  <circle cx="60" cy="25" r="1.5" fill="#6d4c41"/>
  <circle cx="64" cy="27" r="1.5" fill="#6d4c41"/>
  <circle cx="58" cy="31" r="1.5" fill="#6d4c41"/>
  <circle cx="62" cy="31" r="1.5" fill="#6d4c41"/>
  <circle cx="60" cy="35" r="1.5" fill="#6d4c41"/>
</svg>"""

SVG_PORUMB = """<svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="140" rx="10" fill="#e8f5e9"/>
  <ellipse cx="60" cy="132" rx="40" ry="7" fill="#5d4037" opacity="0.35"/>
  <!-- Tulpina groasa -->
  <rect x="55" y="20" width="10" height="115" rx="5" fill="#388e3c"/>
  <path d="M55 132 Q53 100 55 70 Q56 45 55 20" stroke="#2e7d32" stroke-width="1" fill="none"/>
  <!-- Striuri pe tulpina -->
  <line x1="57" y1="25" x2="57" y2="128" stroke="#1b5e20" stroke-width="0.8" opacity="0.4"/>
  <line x1="63" y1="25" x2="63" y2="128" stroke="#1b5e20" stroke-width="0.8" opacity="0.4"/>
  <!-- Frunze late caracteristice -->
  <path d="M60 50 Q35 42 15 55 Q35 52 60 58" fill="#4caf50" opacity="0.9"/>
  <path d="M60 70 Q85 60 105 72 Q85 68 60 78" fill="#43a047" opacity="0.9"/>
  <path d="M60 90 Q32 80 12 92 Q32 88 60 98" fill="#4caf50" opacity="0.8"/>
  <path d="M60 108 Q88 98 108 108 Q88 106 60 115" fill="#43a047" opacity="0.8"/>
  <!-- Stiulete (stiuletele de porumb) -->
  <rect x="68" y="62" width="18" height="36" rx="9" fill="#f9a825"/>
  <!-- Boabe porumb -->
  <circle cx="72" cy="68" r="2.5" fill="#f57f17"/>
  <circle cx="78" cy="68" r="2.5" fill="#f57f17"/>
  <circle cx="72" cy="74" r="2.5" fill="#fbc02d"/>
  <circle cx="78" cy="74" r="2.5" fill="#fbc02d"/>
  <circle cx="72" cy="80" r="2.5" fill="#f57f17"/>
  <circle cx="78" cy="80" r="2.5" fill="#f57f17"/>
  <circle cx="72" cy="86" r="2.5" fill="#fbc02d"/>
  <circle cx="78" cy="86" r="2.5" fill="#fbc02d"/>
  <!-- Matase porumb -->
  <path d="M77 62 Q80 50 82 42" stroke="#f5deb3" stroke-width="1" fill="none"/>
  <path d="M79 62 Q83 50 86 42" stroke="#f5deb3" stroke-width="1" fill="none"/>
  <path d="M75 62 Q77 50 78 42" stroke="#f5deb3" stroke-width="1" fill="none"/>
  <!-- Panicul (floarea) -->
  <path d="M60 20 Q58 10 57 4" stroke="#795548" stroke-width="2" fill="none"/>
  <path d="M60 20 Q64 10 66 4" stroke="#795548" stroke-width="2" fill="none"/>
  <path d="M60 20 Q60 8 60 2" stroke="#795548" stroke-width="2.5" fill="none"/>
</svg>"""

CULTURI = {
    "🌾 Grâu": {
        "svg": SVG_GRAU, "color_bg": "#fef9e7", "color_border": "#f4d03f",
        "color_text": "#7d6608",
        "boli": ["Făinare", "Septorioză", "Rugina galbenă", "Fuzarioză spic"],
        "daunatori": ["Gândacul ghebos", "Afide", "Trips"],
        "faze": ["Înfrățire", "Alungire", "Burduf", "Spicuire", "Maturare"],
        "intrebari": [
            "Ce fungicide aplic la grâu în faza de burduf? Doze și setări T50.",
            "Am rugina galbenă pe grâu. Tratament urgent cu drona T50.",
            "Când aplic al doilea tratament fungicid la grâu?",
            "Cum recunosc fuzarioza spicului la grâu și ce fac?",
        ]
    },
    "🌿 Orz": {
        "svg": SVG_ORZ, "color_bg": "#f0f9e8", "color_border": "#a8d5a2",
        "color_text": "#1b5e20",
        "boli": ["Rețeaua orzului", "Pătarea helmintosporiană", "Făinare", "Rugina pitică"],
        "daunatori": ["Afide", "Trips", "Gândacul ghebos"],
        "faze": ["Înfrățire", "Alungire", "Burduf", "Spicuire", "Maturare"],
        "intrebari": [
            "Ce tratament fungicid fac la orz primăvara? Cu T50.",
            "Am rețeaua orzului — cât de urgent trebuie să tratez?",
            "Care e PHI-ul pentru fungicidele la orz?",
            "Orz vs grâu — diferențe în schema de tratamente?",
        ]
    },
    "🟡 Rapiță": {
        "svg": SVG_RAPITA, "color_bg": "#fffde7", "color_border": "#f9ca24",
        "color_text": "#7d6608",
        "boli": ["Sclerotinia", "Cilindrosporioză", "Alternarioză", "Mana rapiței"],
        "daunatori": ["Gândacul lucios", "Puricii cruciferelor", "Gărgărița tulpinilor"],
        "faze": ["Rozeta", "Vernalizare", "Alungire", "Butonizare", "Înflorire"],
        "intrebari": [
            "Când tratez rapița împotriva gândacului lucios? Prag economic și T50.",
            "Fungicid la rapiță în faza de butonizare — ce aleg?",
            "Sclerotinia la rapiță — cum o previn și tratez?",
            "Când aplic regulatorul de creștere la rapiță?",
        ]
    },
    "💜 Lucernă": {
        "svg": SVG_LUCERNA, "color_bg": "#f3e5f5", "color_border": "#9c27b0",
        "color_text": "#4a148c",
        "boli": ["Putregaiul coroanei", "Verticilioza", "Pătarea frunzelor"],
        "daunatori": ["Gărgărița lucernei", "Trips", "Păduchele lucernei"],
        "faze": ["Pornire vegetație", "Vegetație activă", "Butonizare", "Înflorire", "Cosit"],
        "intrebari": [
            "Insecticid la lucernă înainte de cosit — ce PHI trebuie respectat?",
            "Cum combat gărgărița lucernei? Doze și poate T50?",
            "La câte zile după cosit pot aplica tratamente la lucernă?",
            "Cum îmbunătățesc producția la lucernă prin fertilizare foliară?",
        ]
    },
    "🌻 Floarea soarelui": {
        "svg": SVG_FLOAREA_SOARELUI, "color_bg": "#fff8e1", "color_border": "#fdd835",
        "color_text": "#7d6608",
        "boli": ["Mana florii soarelui", "Sclerotinia", "Putregaiul cenușiu", "Alternarioza"],
        "daunatori": ["Viermele sârmă", "Omida de câmp", "Afide"],
        "faze": ["Răsărire", "4-6 frunze", "Butonizare", "Înflorire", "Maturare"],
        "intrebari": [
            "Mana la floarea soarelui — tratament preventiv sau curativ?",
            "Ce erbicide aplic la floarea soarelui Clearfield/Express?",
            "Sclerotinia la floarea soarelui — fungicid și doze T50.",
            "Cum recunosc deficitul de bor la floarea soarelui?",
        ]
    },
    "🌽 Porumb": {
        "svg": SVG_PORUMB, "color_bg": "#e8f5e9", "color_border": "#f9a825",
        "color_text": "#e65100",
        "boli": ["Fuzarioza tulpinii", "Helminthosporioza", "Rugina porumbului"],
        "daunatori": ["Sfredelitorul porumbului", "Viermele vestic", "Omida de câmp"],
        "faze": ["Răsărire", "4-6 frunze", "8-10 frunze", "Paniculat", "Maturare"],
        "intrebari": [
            "Insecticid împotriva sfredelitorului porumbului — când și cu T50?",
            "Erbicidat postemergent la porumb — ce produse folosesc?",
            "Cum recunosc atacul viermilor de rădăcini la porumb?",
            "Fertilizare foliară la porumb în faza de 6-8 frunze — ce recomandați?",
        ]
    },
}

# SVG Dronă T50
SVG_DRONA = """<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="120" rx="12" fill="#0d2818" opacity="0.95"/>
  <!-- Stars background -->
  <circle cx="20" cy="15" r="1" fill="white" opacity="0.4"/>
  <circle cx="170" cy="20" r="1" fill="white" opacity="0.4"/>
  <circle cx="140" cy="10" r="1.5" fill="white" opacity="0.3"/>
  <circle cx="50" cy="8" r="1" fill="white" opacity="0.4"/>
  <!-- Orizont câmp -->
  <rect x="0" y="88" width="200" height="32" rx="0" fill="#1b4332" opacity="0.8"/>
  <path d="M0 88 Q50 82 100 88 Q150 94 200 88 L200 120 L0 120 Z" fill="#2d6a4f" opacity="0.6"/>
  <!-- Lanuri stilizate -->
  <rect x="10" y="95" width="3" height="18" rx="1" fill="#52b788" opacity="0.7"/>
  <rect x="18" y="92" width="3" height="21" rx="1" fill="#40916c" opacity="0.7"/>
  <rect x="26" y="96" width="3" height="17" rx="1" fill="#52b788" opacity="0.7"/>
  <rect x="34" y="93" width="3" height="20" rx="1" fill="#40916c" opacity="0.7"/>
  <rect x="155" y="94" width="3" height="19" rx="1" fill="#52b788" opacity="0.7"/>
  <rect x="163" y="91" width="3" height="22" rx="1" fill="#40916c" opacity="0.7"/>
  <rect x="171" y="95" width="3" height="18" rx="1" fill="#52b788" opacity="0.7"/>
  <rect x="179" y="93" width="3" height="20" rx="1" fill="#40916c" opacity="0.7"/>
  <!-- Luna -->
  <circle cx="175" cy="18" r="10" fill="#f4d03f" opacity="0.8"/>
  <circle cx="179" cy="15" r="8" fill="#0d2818"/>
  <!-- Drona corp -->
  <rect x="82" y="48" width="36" height="16" rx="6" fill="#e0e0e0"/>
  <rect x="88" y="52" width="24" height="8" rx="3" fill="#9e9e9e"/>
  <!-- Camera -->
  <circle cx="100" cy="67" r="4" fill="#333"/>
  <circle cx="100" cy="67" r="2.5" fill="#555"/>
  <!-- Brate drona -->
  <line x1="82" y1="52" x2="52" y2="38" stroke="#bdbdbd" stroke-width="3" stroke-linecap="round"/>
  <line x1="118" y1="52" x2="148" y2="38" stroke="#bdbdbd" stroke-width="3" stroke-linecap="round"/>
  <line x1="82" y1="60" x2="52" y2="74" stroke="#bdbdbd" stroke-width="3" stroke-linecap="round"/>
  <line x1="118" y1="60" x2="148" y2="74" stroke="#bdbdbd" stroke-width="3" stroke-linecap="round"/>
  <!-- Elice (rotoare) -->
  <ellipse cx="52" cy="38" rx="20" ry="5" fill="#f4d03f" opacity="0.85"/>
  <circle cx="52" cy="38" r="4" fill="#616161"/>
  <ellipse cx="148" cy="38" rx="20" ry="5" fill="#f4d03f" opacity="0.85"/>
  <circle cx="148" cy="38" r="4" fill="#616161"/>
  <ellipse cx="52" cy="74" rx="20" ry="5" fill="#f4d03f" opacity="0.85"/>
  <circle cx="52" cy="74" r="4" fill="#616161"/>
  <ellipse cx="148" cy="74" rx="20" ry="5" fill="#f4d03f" opacity="0.85"/>
  <circle cx="148" cy="74" r="4" fill="#616161"/>
  <!-- Spray picaturi -->
  <circle cx="94" cy="75" r="2" fill="#74c69d" opacity="0.8"/>
  <circle cx="100" cy="79" r="2" fill="#74c69d" opacity="0.8"/>
  <circle cx="106" cy="75" r="2" fill="#74c69d" opacity="0.8"/>
  <circle cx="91" cy="82" r="1.5" fill="#52b788" opacity="0.6"/>
  <circle cx="100" cy="86" r="1.5" fill="#52b788" opacity="0.6"/>
  <circle cx="109" cy="82" r="1.5" fill="#52b788" opacity="0.6"/>
  <!-- Rezervor T50 -->
  <rect x="88" y="62" width="24" height="10" rx="4" fill="#42a5f5" opacity="0.7"/>
  <!-- LED-uri status -->
  <circle cx="88" cy="54" r="2" fill="#4caf50"/>
  <circle cx="112" cy="54" r="2" fill="#f44336"/>
</svg>"""

# ═══════════════════════════════════════════════════════════════════
# CSS DESIGN AGRONOMIC
# ═══════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* FUNDAL PREMIUM DARK */
    .stApp {
        background: linear-gradient(135deg, #020f07 0%, #0a1f12 30%, #0d2818 60%, #071a0e 100%);
        min-height: 100vh;
    }
    /* Grid futuristic pe fundal */
    [data-testid="stAppViewContainer"] {
        background-image:
            linear-gradient(rgba(116,198,157,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(116,198,157,0.03) 1px, transparent 1px);
        background-size: 50px 50px;
    }
    /* Text general alb pe dark */
    .stApp, .stApp p, .stApp label, .stApp div { color: rgba(255,255,255,0.85); }
    .stMarkdown, .stMarkdown p { color: rgba(255,255,255,0.8) !important; }
    h1, h2, h3 { color: white !important; }

    /* HEADER HERO FUTURISTIC */
    .acp-hero {
        background: linear-gradient(135deg, #0a1f12 0%, #1b4332 50%, #0d2818 100%);
        padding: 1.8rem 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 0 1px rgba(116,198,157,0.15), 0 20px 60px rgba(0,0,0,0.5), 0 0 40px rgba(45,106,79,0.1);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(116,198,157,0.15);
    }
    /* Linie luminoasa sus */
    .acp-hero::before {
        content: '';
        position: absolute; top: 0; left: 10%; right: 10%; height: 2px;
        background: linear-gradient(90deg, transparent, #74c69d, #f4d03f, #74c69d, transparent);
        opacity: 0.6;
    }
    /* Glow coltar dreapta */
    .acp-hero::after {
        content: '';
        position: absolute; top: -50px; right: -50px;
        width: 200px; height: 200px;
        background: radial-gradient(circle, rgba(116,198,157,0.08) 0%, transparent 70%);
    }
    .hero-content { position: relative; z-index: 2; }
    .hero-brand { font-size: 0.65rem; font-weight: 800; letter-spacing: 5px; color: #74c69d; text-transform: uppercase; }
    .hero-title { margin: 0.4rem 0 0.2rem 0; font-size: 1.9rem; font-weight: 800; color: white; }
    .hero-sub { margin: 0; font-size: 0.88rem; color: rgba(255,255,255,0.55); }
    .badge-pro {
        background: linear-gradient(135deg,#f4d03f,#f39c12);
        color:#0d2818; font-size:0.6rem; font-weight:800;
        padding:3px 10px; border-radius:20px; letter-spacing:1.5px;
        vertical-align:middle; margin-left:8px;
        box-shadow: 0 0 12px rgba(244,208,63,0.4);
    }

    /* CARDURI CULTURI GLASSMORPHISM */
    .cultura-card {
        background: rgba(10, 30, 20, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 18px;
        border: 1px solid rgba(116,198,157,0.15);
        box-shadow: 0 4px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.04);
        transition: all 0.3s ease;
        overflow: hidden;
        height: 100%;
    }
    .cultura-card:hover {
        box-shadow: 0 12px 40px rgba(45,106,79,0.3), 0 0 20px rgba(116,198,157,0.1);
        transform: translateY(-5px);
        border-color: rgba(116,198,157,0.4);
    }
    .card-img-area {
        height: 140px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.5rem;
    }
    .card-img-area svg { height: 130px; width: auto; }
    .card-body { padding: 1rem 1.2rem 1.2rem 1.2rem; }
    .card-title { font-weight: 800; font-size: 1.05rem; margin-bottom: 0.4rem; color: white !important; }
    .card-tag {
        display: inline-block;
        font-size: 0.68rem; font-weight: 600;
        padding: 2px 8px; border-radius: 20px;
        margin: 2px 1px;
        background: rgba(116,198,157,0.12) !important;
        color: #74c69d !important;
        border: 1px solid rgba(116,198,157,0.2) !important;
    }
    .card-section { font-size: 0.72rem; font-weight: 700; color: rgba(255,255,255,0.35) !important; text-transform: uppercase; letter-spacing: 1px; margin: 0.5rem 0 0.25rem 0; }

    /* CHAT FUTURISTIC */
    .msg-user {
        background: linear-gradient(135deg, rgba(45,106,79,0.35), rgba(27,67,50,0.4));
        border-radius: 18px 18px 4px 18px;
        padding: 1rem 1.2rem;
        margin: 0.6rem 0 0.6rem 2.5rem;
        border: 1px solid rgba(116,198,157,0.25);
        box-shadow: 0 2px 12px rgba(0,0,0,0.2);
        color: rgba(255,255,255,0.9) !important;
    }
    .msg-agent {
        background: rgba(10, 25, 16, 0.7);
        backdrop-filter: blur(8px);
        border-radius: 18px 18px 18px 4px;
        padding: 1rem 1.2rem;
        margin: 0.6rem 2.5rem 0.6rem 0;
        border: 1px solid rgba(116,198,157,0.12);
        box-shadow: 0 4px 20px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.03);
        line-height: 1.8;
        color: rgba(255,255,255,0.85) !important;
    }
    .msg-label { font-size: 0.65rem; font-weight: 800; opacity: 0.4; margin-bottom: 0.4rem; letter-spacing: 2px; text-transform: uppercase; color: #74c69d !important; }

    /* CALCULATOR FUTURISTIC */
    .calc-result {
        background: rgba(10, 25, 16, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 16px; padding: 1.5rem;
        border: 1px solid rgba(116,198,157,0.2);
        box-shadow: 0 0 30px rgba(45,106,79,0.1);
    }
    .calc-result h3 { color: #74c69d !important; }
    .calc-row { display:flex; justify-content:space-between; padding:0.5rem 0; border-bottom:1px solid rgba(116,198,157,0.1); font-size:0.92rem; color: rgba(255,255,255,0.75); }
    .calc-row:last-child { border-bottom:none; font-weight:700; color: #74c69d; }

    /* INFO BOX sezon */
    .season-box {
        border-radius: 14px;
        padding: 1rem 1.3rem;
        font-size: 0.9rem;
        margin: 1rem 0;
        border-left: 5px solid;
    }

    /* SECTIUNE DRONA */
    .drona-section {
        background: linear-gradient(135deg,#0d2818,#1b4332);
        border-radius: 18px;
        padding: 1.5rem;
        color: white;
        margin: 1rem 0;
    }

    /* HISTORY ITEM */
    .hist-card {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.7rem;
        border-left: 5px solid #52b788;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    /* TABS FUTURISTIC */
    .stTabs [data-baseweb="tab-list"] {
        gap:4px;
        background: rgba(10,25,16,0.6);
        border-radius:14px; padding:5px;
        border:1px solid rgba(116,198,157,0.15);
        backdrop-filter: blur(8px);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius:10px; padding:0.5rem 1.1rem;
        font-weight:600; font-size:0.88rem;
        color: rgba(255,255,255,0.5) !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(45,106,79,0.5) !important;
        color: #74c69d !important;
        border: 1px solid rgba(116,198,157,0.3) !important;
        box-shadow: 0 0 12px rgba(45,106,79,0.3) !important;
    }

    /* SIDEBAR dark futuristic */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020f07 0%, #0a1f12 100%) !important;
        border-right: 1px solid rgba(116,198,157,0.1) !important;
    }
    [data-testid="stSidebar"] * { color: rgba(255,255,255,0.8) !important; }
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(45,106,79,0.3) !important;
        border: 1px solid rgba(116,198,157,0.2) !important;
        color: rgba(255,255,255,0.85) !important;
        border-radius: 10px !important;
        transition: all 0.2s !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(45,106,79,0.6) !important;
        border-color: rgba(116,198,157,0.5) !important;
        box-shadow: 0 0 12px rgba(45,106,79,0.3) !important;
    }
    [data-testid="stSidebar"] input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(116,198,157,0.2) !important;
        color: white !important; border-radius: 8px !important;
    }

    /* INPUTS globale */
    .stTextInput input, .stTextArea textarea, .stSelectbox div {
        background: rgba(10,25,16,0.6) !important;
        border: 1px solid rgba(116,198,157,0.2) !important;
        color: white !important; border-radius: 10px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: rgba(116,198,157,0.5) !important;
        box-shadow: 0 0 12px rgba(45,106,79,0.2) !important;
    }

    /* BUTTONS principale */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.25s !important;
        background: rgba(27,67,50,0.6) !important;
        border: 1px solid rgba(116,198,157,0.2) !important;
        color: rgba(255,255,255,0.85) !important;
    }
    .stButton > button:hover {
        background: rgba(45,106,79,0.7) !important;
        border-color: rgba(116,198,157,0.4) !important;
        box-shadow: 0 0 16px rgba(45,106,79,0.3) !important;
    }
    /* Buton primary */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #1b4332, #2d6a4f) !important;
        border: 1px solid rgba(116,198,157,0.4) !important;
        box-shadow: 0 0 20px rgba(45,106,79,0.3) !important;
        color: white !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #2d6a4f, #40916c) !important;
        box-shadow: 0 0 30px rgba(45,106,79,0.5) !important;
    }

    /* EXPANDER */
    .streamlit-expanderHeader {
        background: rgba(10,25,16,0.6) !important;
        border: 1px solid rgba(116,198,157,0.15) !important;
        border-radius: 10px !important;
        color: rgba(255,255,255,0.8) !important;
    }
    .streamlit-expanderContent {
        background: rgba(5,15,10,0.5) !important;
        border: 1px solid rgba(116,198,157,0.1) !important;
    }

    /* METRIC */
    [data-testid="stMetric"] {
        background: rgba(10,25,16,0.6) !important;
        border: 1px solid rgba(116,198,157,0.12) !important;
        border-radius: 12px !important;
        padding: 0.8rem !important;
    }
    [data-testid="stMetricValue"] { color: #74c69d !important; }
    [data-testid="stMetricLabel"] { color: rgba(255,255,255,0.4) !important; }

    /* INFO/SUCCESS/ERROR */
    .stAlert { background: rgba(10,25,16,0.7) !important; border-radius: 12px !important; }

    /* HR separatoare */
    hr { border-color: rgba(116,198,157,0.1) !important; }

    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# BAZA DE DATE
# ═══════════════════════════════════════════════════════════════════

def init_db():
    conn = sqlite3.connect("agronom_history.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT, cultura TEXT,
        created_at TEXT, messages TEXT)""")
    conn.commit(); conn.close()

def save_session(title, messages, cultura="General"):
    conn = sqlite3.connect("agronom_history.db")
    c = conn.cursor()
    c.execute("INSERT INTO sessions (title,cultura,created_at,messages) VALUES (?,?,?,?)",
              (title, cultura, datetime.now().isoformat(), json.dumps(messages, ensure_ascii=False)))
    conn.commit(); conn.close()

def get_sessions(limit=30):
    conn = sqlite3.connect("agronom_history.db")
    c = conn.cursor()
    c.execute("SELECT id,title,cultura,created_at,messages FROM sessions ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = c.fetchall(); conn.close(); return rows

def delete_session(sid):
    conn = sqlite3.connect("agronom_history.db")
    c = conn.cursor()
    c.execute("DELETE FROM sessions WHERE id=?", (sid,))
    conn.commit(); conn.close()

init_db()

# ═══════════════════════════════════════════════════════════════════
# PROMPT SISTEM
# ═══════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = f"""Ești agronumul personal al fermei ACP Engineer, expert cu 20+ ani experiență.

**FERMA ACP Engineer — Culturile active:**
- 🌾 GRÂU — cultură de toamnă, tratamente fungicide în 2 etape (înfrățire + burduf/spicuire)
- 🌿 ORZ — cultură de toamnă, maturare cu 2-3 săptămâni înaintea grâului
- 🟡 RAPIȚĂ — cultură de toamnă, atenție la gândacul lucios și sclerotinia
- 💜 LUCERNĂ — cultură perenă, restricții PHI stricte pre-cosit
- 🌻 FLOAREA SOARELUI — atenție la mana și sclerotinia, erbicide selective Clearfield/Express
- 🌽 PORUMB — sfredelitorul principalul dăunător, erbicidat postemergent obligatoriu

**Drona DJI Agras T50:**
- Rezervor: 40L lichid / 50kg granule | Debit max: 8 L/min, 8 duze
- Acoperire: 40-60 ha/oră | Lățime: 9m la 3m înălțime
- Doze aeriene: 10-15 L/ha | Viteză: 5-7 m/s | RTK GPS centimetric

**Protocol:**
1. Răspunzi MEREU în română, direct și practic
2. Substanță activă + produse comerciale RO + doze exacte + PHI
3. Specifici compatibilitate cu drona T50 + setări recomandate
4. La imagini: Diagnostic → Cauze → Tratament → Prevenție
5. Data: {date.today().strftime('%d %B %Y')}"""

# ═══════════════════════════════════════════════════════════════════
# AUTENTIFICARE
# ═══════════════════════════════════════════════════════════════════

ACP_LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="180" height="180">
  <defs>
    <linearGradient id="lbg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0d2818"/>
      <stop offset="50%" style="stop-color:#1b4332"/>
      <stop offset="100%" style="stop-color:#0d2818"/>
    </linearGradient>
    <linearGradient id="lgold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f4d03f"/>
      <stop offset="50%" style="stop-color:#f39c12"/>
      <stop offset="100%" style="stop-color:#d4ac0d"/>
    </linearGradient>
    <filter id="lglow">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="lshadow">
      <feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="#000" flood-opacity="0.4"/>
    </filter>
  </defs>
  <circle cx="250" cy="250" r="240" fill="url(#lbg)" filter="url(#lshadow)"/>
  <circle cx="250" cy="250" r="228" fill="none" stroke="url(#lgold)" stroke-width="2.5" opacity="0.7"/>
  <circle cx="250" cy="250" r="210" fill="none" stroke="#74c69d" stroke-width="1" opacity="0.3"/>
  <g stroke="url(#lgold)" stroke-width="2" opacity="0.6">
    <line x1="250" y1="22" x2="250" y2="40"/><line x1="250" y1="460" x2="250" y2="478"/>
    <line x1="22" y1="250" x2="40" y2="250"/><line x1="460" y1="250" x2="478" y2="250"/>
    <line x1="88" y1="88" x2="101" y2="101"/><line x1="399" y1="399" x2="412" y2="412"/>
    <line x1="412" y1="88" x2="399" y2="101"/><line x1="101" y1="399" x2="88" y2="412"/>
  </g>
  <g transform="translate(95,245)" opacity="0.75">
    <ellipse cx="-28" cy="-58" rx="8" ry="20" fill="#74c69d" transform="rotate(-30,-28,-58)"/>
    <ellipse cx="-18" cy="-78" rx="7" ry="18" fill="#52b788" transform="rotate(-15,-18,-78)"/>
    <ellipse cx="-33" cy="-38" rx="7" ry="17" fill="#74c69d" transform="rotate(-45,-33,-38)"/>
    <line x1="-23" y1="-8" x2="-23" y2="-88" stroke="#40916c" stroke-width="2"/>
  </g>
  <g transform="translate(405,245)" opacity="0.75">
    <ellipse cx="28" cy="-58" rx="8" ry="20" fill="#74c69d" transform="rotate(30,28,-58)"/>
    <ellipse cx="18" cy="-78" rx="7" ry="18" fill="#52b788" transform="rotate(15,18,-78)"/>
    <ellipse cx="33" cy="-38" rx="7" ry="17" fill="#74c69d" transform="rotate(45,33,-38)"/>
    <line x1="23" y1="-8" x2="23" y2="-88" stroke="#40916c" stroke-width="2"/>
  </g>
  <g transform="translate(250,148)" filter="url(#lglow)">
    <rect x="-16" y="-9" width="32" height="18" rx="5" fill="url(#lgold)"/>
    <line x1="-16" y1="-4" x2="-48" y2="-20" stroke="#f4d03f" stroke-width="3.5" stroke-linecap="round"/>
    <line x1="16" y1="-4" x2="48" y2="-20" stroke="#f4d03f" stroke-width="3.5" stroke-linecap="round"/>
    <line x1="-16" y1="4" x2="-48" y2="20" stroke="#f4d03f" stroke-width="3.5" stroke-linecap="round"/>
    <line x1="16" y1="4" x2="48" y2="20" stroke="#f4d03f" stroke-width="3.5" stroke-linecap="round"/>
    <ellipse cx="-48" cy="-20" rx="16" ry="4" fill="none" stroke="#f4d03f" stroke-width="2.5" opacity="0.85"/>
    <ellipse cx="48" cy="-20" rx="16" ry="4" fill="none" stroke="#f4d03f" stroke-width="2.5" opacity="0.85"/>
    <ellipse cx="-48" cy="20" rx="16" ry="4" fill="none" stroke="#f4d03f" stroke-width="2.5" opacity="0.85"/>
    <ellipse cx="48" cy="20" rx="16" ry="4" fill="none" stroke="#f4d03f" stroke-width="2.5" opacity="0.85"/>
  </g>
  <line x1="110" y1="193" x2="390" y2="193" stroke="url(#lgold)" stroke-width="1" opacity="0.4"/>
  <text x="250" y="292" font-family="Georgia,serif" font-size="108" font-weight="bold"
        fill="url(#lgold)" text-anchor="middle" letter-spacing="6" filter="url(#lglow)">ACP</text>
  <circle cx="222" cy="312" r="3" fill="url(#lgold)" opacity="0.6"/>
  <circle cx="250" cy="312" r="3" fill="url(#lgold)" opacity="0.6"/>
  <circle cx="278" cy="312" r="3" fill="url(#lgold)" opacity="0.6"/>
  <text x="250" y="360" font-family="Arial,sans-serif" font-size="29" font-weight="700"
        fill="white" text-anchor="middle" letter-spacing="10" opacity="0.95">ENGINEER</text>
  <line x1="125" y1="380" x2="375" y2="380" stroke="url(#lgold)" stroke-width="1" opacity="0.4"/>
  <text x="250" y="410" font-family="Arial,sans-serif" font-size="13" fill="#74c69d"
        text-anchor="middle" letter-spacing="3" opacity="0.85">AGRI-TECH SOLUTIONS</text>
</svg>"""

def login_page():
    # CSS special doar pentru pagina de login
    st.markdown("""
    <style>
    /* Ascunde tot padding-ul Streamlit pe login */
    .stApp { background: #020f07 !important; }
    [data-testid="stAppViewContainer"] { padding: 0 !important; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    section[data-testid="stSidebar"] { display: none !important; }

    /* Particule de fundal animate */
    @keyframes float1 { 0%,100%{transform:translateY(0) translateX(0)} 50%{transform:translateY(-30px) translateX(15px)} }
    @keyframes float2 { 0%,100%{transform:translateY(0) translateX(0)} 50%{transform:translateY(20px) translateX(-20px)} }
    @keyframes float3 { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-20px)} }
    @keyframes pulse-ring { 0%{transform:scale(0.95);opacity:0.8} 50%{transform:scale(1.05);opacity:1} 100%{transform:scale(0.95);opacity:0.8} }
    @keyframes shimmer { 0%{background-position:-200% center} 100%{background-position:200% center} }
    @keyframes scanline { 0%{top:-5%} 100%{top:105%} }

    .login-bg {
        position: fixed; top:0; left:0; width:100vw; height:100vh;
        background: radial-gradient(ellipse at 20% 50%, #0a2e1a 0%, #020f07 40%, #000d05 100%);
        z-index: 0;
        overflow: hidden;
    }
    .login-bg::before {
        content: '';
        position: absolute; top:0; left:0; right:0; bottom:0;
        background-image:
            radial-gradient(1px 1px at 20% 30%, rgba(116,198,157,0.4) 0%, transparent 100%),
            radial-gradient(1px 1px at 80% 15%, rgba(244,208,63,0.3) 0%, transparent 100%),
            radial-gradient(1px 1px at 50% 70%, rgba(116,198,157,0.3) 0%, transparent 100%),
            radial-gradient(1px 1px at 10% 80%, rgba(244,208,63,0.2) 0%, transparent 100%),
            radial-gradient(1px 1px at 90% 60%, rgba(116,198,157,0.35) 0%, transparent 100%),
            radial-gradient(1px 1px at 35% 90%, rgba(244,208,63,0.25) 0%, transparent 100%),
            radial-gradient(1px 1px at 70% 45%, rgba(116,198,157,0.3) 0%, transparent 100%);
        background-size: 200px 200px, 300px 300px, 250px 250px, 180px 180px, 220px 220px, 280px 280px, 260px 260px;
    }
    /* Grid lines futuristice */
    .login-grid {
        position: absolute; top:0; left:0; right:0; bottom:0;
        background-image:
            linear-gradient(rgba(116,198,157,0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(116,198,157,0.04) 1px, transparent 1px);
        background-size: 60px 60px;
    }
    /* Spot light verde */
    .login-glow-left {
        position: absolute; top:20%; left:-10%;
        width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(45,106,79,0.15) 0%, transparent 70%);
        animation: float1 8s ease-in-out infinite;
    }
    .login-glow-right {
        position: absolute; bottom:10%; right:-5%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(244,208,63,0.08) 0%, transparent 70%);
        animation: float2 10s ease-in-out infinite;
    }
    /* Scanline effect */
    .login-scan {
        position: absolute; left:0; right:0; height:2px;
        background: linear-gradient(90deg, transparent, rgba(116,198,157,0.3), transparent);
        animation: scanline 6s linear infinite;
        pointer-events: none;
    }

    /* Card glassmorphism */
    .login-card {
        position: relative; z-index: 10;
        background: rgba(10, 30, 20, 0.75);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(116,198,157,0.25);
        border-radius: 28px;
        padding: 2.5rem 2.5rem 2rem 2.5rem;
        max-width: 440px;
        width: 90%;
        margin: 0 auto;
        box-shadow:
            0 0 0 1px rgba(116,198,157,0.1),
            0 30px 60px rgba(0,0,0,0.5),
            0 0 80px rgba(45,106,79,0.15),
            inset 0 1px 0 rgba(255,255,255,0.05);
        text-align: center;
        animation: float3 6s ease-in-out infinite;
    }
    /* Bordera luminoasa */
    .login-card::before {
        content: '';
        position: absolute; top:-1px; left:20%; right:20%; height:2px;
        background: linear-gradient(90deg, transparent, #74c69d, #f4d03f, #74c69d, transparent);
        border-radius: 2px;
        opacity: 0.7;
    }
    .login-card::after {
        content: '';
        position: absolute; bottom:-1px; left:20%; right:20%; height:1px;
        background: linear-gradient(90deg, transparent, rgba(116,198,157,0.4), transparent);
    }

    /* Logo pulsating */
    .logo-wrap {
        display: inline-block;
        animation: pulse-ring 3s ease-in-out infinite;
        filter: drop-shadow(0 0 20px rgba(116,198,157,0.4)) drop-shadow(0 0 40px rgba(45,106,79,0.2));
        margin-bottom: 1rem;
    }

    /* Titlu shimmer */
    .login-title {
        font-size: 1.6rem; font-weight: 800; margin: 0.2rem 0;
        background: linear-gradient(90deg, #74c69d, #f4d03f, #74c69d, #f4d03f);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 4s linear infinite;
        letter-spacing: 1px;
    }
    .login-sub {
        color: rgba(255,255,255,0.45);
        font-size: 0.82rem;
        margin-bottom: 2rem;
        letter-spacing: 0.5px;
    }

    /* Input stilizat */
    .login-input-wrap {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(116,198,157,0.2);
        border-radius: 14px;
        padding: 1.2rem 1.5rem 1rem 1.5rem;
        margin-bottom: 1rem;
        text-align: left;
    }
    .login-input-label {
        font-size: 0.65rem; font-weight: 800; letter-spacing: 3px;
        color: #74c69d; text-transform: uppercase; margin-bottom: 0.6rem;
    }

    /* Buton futuristic */
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #1b4332, #2d6a4f) !important;
        border: 1px solid rgba(116,198,157,0.4) !important;
        color: white !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        border-radius: 12px !important;
        padding: 0.75rem !important;
        font-size: 0.9rem !important;
        box-shadow: 0 0 20px rgba(45,106,79,0.3), inset 0 1px 0 rgba(255,255,255,0.1) !important;
        transition: all 0.3s !important;
    }
    div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #2d6a4f, #40916c) !important;
        box-shadow: 0 0 30px rgba(45,106,79,0.5), 0 0 60px rgba(116,198,157,0.2) !important;
        transform: translateY(-2px) !important;
    }

    /* Stats row */
    .login-stats {
        display: flex; justify-content: center; gap: 1.5rem;
        margin-top: 1.5rem; padding-top: 1.5rem;
        border-top: 1px solid rgba(116,198,157,0.1);
    }
    .login-stat { text-align: center; }
    .login-stat-n { font-size: 1.1rem; font-weight: 800; color: #f4d03f; }
    .login-stat-l { font-size: 0.65rem; color: rgba(255,255,255,0.3); text-transform: uppercase; letter-spacing: 1px; }

    /* Footer login */
    .login-footer {
        margin-top: 1.5rem; font-size: 0.68rem;
        color: rgba(255,255,255,0.2); letter-spacing: 1px;
    }
    </style>

    <div class="login-bg">
        <div class="login-grid"></div>
        <div class="login-glow-left"></div>
        <div class="login-glow-right"></div>
        <div class="login-scan"></div>
    </div>
    <div style="position:relative;z-index:10;display:flex;align-items:center;justify-content:center;min-height:100vh;padding:2rem;">
        <div class="login-card">
            <div class="logo-wrap">""" + ACP_LOGO_SVG + """</div>
            <div class="login-title">Agronom AI Pro</div>
            <div class="login-sub">Platforma inteligentă de management agricol · ACP Engineer</div>
            <div class="login-input-wrap">
                <div class="login-input-label">🔐 Acces securizat</div>
    """, unsafe_allow_html=True)

    password = st.text_input("", type="password", placeholder="Introdu parola de acces...",
                              label_visibility="collapsed")
    if st.button("INTRĂ ÎN APLICAȚIE  →", use_container_width=True, type="primary"):
        if password == APP_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("⚠️ Parolă incorectă. Încearcă din nou.")

    st.markdown("""
            </div>
            <div class="login-stats">
                <div class="login-stat">
                    <div class="login-stat-n">6</div>
                    <div class="login-stat-l">Culturi</div>
                </div>
                <div class="login-stat">
                    <div class="login-stat-n">T50</div>
                    <div class="login-stat-l">Dronă</div>
                </div>
                <div class="login-stat">
                    <div class="login-stat-n">AI</div>
                    <div class="login-stat-l">Claude</div>
                </div>
                <div class="login-stat">
                    <div class="login-stat-n">24/7</div>
                    <div class="login-stat-l">Online</div>
                </div>
            </div>
            <div class="login-footer">© 2025 ACP ENGINEER · AGRI-TECH SOLUTIONS · POWERED BY CLAUDE AI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if not st.session_state.authenticated:
    login_page(); st.stop()

# ═══════════════════════════════════════════════════════════════════
# INIȚIALIZARE STATE
# ═══════════════════════════════════════════════════════════════════

if "messages" not in st.session_state: st.session_state.messages = []
if "api_key" not in st.session_state: st.session_state.api_key = ""
if "cultura_activa" not in st.session_state: st.session_state.cultura_activa = None
if "switch_to_chat" not in st.session_state: st.session_state.switch_to_chat = False

# ═══════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1.2rem 0 0.5rem 0;">
        <div style="font-size:2.2rem">🌱</div>
        <div style="font-size:0.6rem; font-weight:800; letter-spacing:4px; color:#74c69d; margin-top:0.3rem">ACP ENGINEER</div>
        <div style="font-weight:700; font-size:1rem; margin-top:0.2rem">Agronom AI Pro</div>
        <div style="font-size:0.7rem; opacity:0.5; margin-top:0.2rem">{}</div>
    </div>
    """.format(date.today().strftime('%d %B %Y')), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**🔑 API Key Anthropic**")
    api_key_input = st.text_input("", type="password", value=st.session_state.api_key,
                                   placeholder="sk-ant-...", label_visibility="collapsed")
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.success("✅ Conectat la Claude AI")
    st.markdown("[Obține cheie API →](https://console.anthropic.com)")
    st.markdown("---")

    st.markdown("**🌾 Culturile mele**")
    for cname in CULTURI:
        icon = cname.split()[0]
        label = cname.split(" ", 1)[1]
        if st.button(f"{icon} {label}", use_container_width=True, key=f"sb_{cname}"):
            st.session_state.cultura_activa = cname
            st.session_state.quick_q = f"Ce lucrări și tratamente sunt recomandate acum (luna {date.today().strftime('%B')}) pentru {label}? Include setările dronei T50."
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.78rem; line-height:2; opacity:0.7">
    🚁 <b>DJI Agras T50</b><br>
    📦 40L / 50kg · 8 L/min<br>
    📐 40-60 ha/h · 9m lățime<br>
    🎯 10-15 L/ha doze aeriene
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    sessions_list = get_sessions()
    st.markdown(f"📊 **{len(sessions_list)} consultații salvate**")
    if st.button("🚪 Deconectare", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.messages = []
        st.rerun()

# ═══════════════════════════════════════════════════════════════════
# HEADER HERO
# ═══════════════════════════════════════════════════════════════════

luna = date.today().month
sezon_icon = "🌱" if luna in [3,4,5] else "☀️" if luna in [6,7,8] else "🍂" if luna in [9,10,11] else "❄️"

st.markdown(f"""
<div class="acp-hero">
  <div class="hero-content">
    <div class="hero-brand">⚡ ACP Engineer · Agri-Tech Solutions · România</div>
    <h1 class="hero-title">{sezon_icon} Agent Agronom AI <span class="badge-pro">PRO</span></h1>
    <p class="hero-sub">Expert în grâu · orz · rapiță · lucernă · floarea soarelui · porumb · DJI Agras T50</p>
    <div style="margin-top:1rem; display:flex; gap:1.5rem; flex-wrap:wrap; font-size:0.78rem; opacity:0.8;">
        <span>📅 {date.today().strftime('%d %B %Y')}</span>
        <span>🚁 T50 Ready</span>
        <span>🤖 Powered by Claude AI</span>
        <span>🌾 6 Culturi active</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════

tab_culturi, tab_chat, tab_t50, tab_history = st.tabs([
    "🌾 Culturile Mele",
    "💬 Consultație",
    "🚁 Calculator T50",
    "📂 Istoric",
])

# ───────────────────────────────────────────────────────────────────
# TAB 1: DASHBOARD CULTURI CU ILUSTRATII
# ───────────────────────────────────────────────────────────────────

with tab_culturi:
    st.markdown("### 🌾 Ferma ACP Engineer — Culturile tale active")
    st.markdown("Fiecare card conține ilustrația culturii, bolile principale și acces direct la consultație.")
    st.markdown("")

    cols = st.columns(3)
    for i, (cname, cdata) in enumerate(CULTURI.items()):
        with cols[i % 3]:
            label = cname.split(" ", 1)[1]
            boli_tags = "".join([f'<span class="card-tag" style="background:{cdata["color_bg"]};color:{cdata["color_text"]};border:1px solid {cdata["color_border"]}">{b}</span>' for b in cdata["boli"][:3]])
            st.markdown(f"""
            <div class="cultura-card" style="border-color:{cdata['color_border']}">
                <div class="card-img-area" style="background:{cdata['color_bg']}">
                    {cdata['svg']}
                </div>
                <div class="card-body">
                    <div class="card-title" style="color:{cdata['color_text']}">{cname}</div>
                    <div class="card-section">Boli principale</div>
                    <div>{boli_tags}</div>
                    <div class="card-section" style="margin-top:0.6rem">Faze vegetație</div>
                    <div style="font-size:0.75rem; color:#666">{' → '.join(cdata['faze'][:4])}...</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button(f"💬 Consultă pentru {label}", key=f"open_{cname}", use_container_width=True):
                st.session_state.cultura_activa = cname
                st.session_state.quick_q = f"Ce lucrări și tratamente sunt recomandate acum (luna {date.today().strftime('%B')}) pentru {label}? Include setările dronei T50."
                st.session_state.switch_to_chat = True
                st.rerun()

    # Sectiune drona
    st.markdown("---")
    col_d1, col_d2 = st.columns([1, 2])
    with col_d1:
        st.markdown(SVG_DRONA, unsafe_allow_html=True)
    with col_d2:
        st.markdown("""
        <div class="drona-section">
            <div style="font-size:0.65rem; font-weight:800; letter-spacing:3px; color:#74c69d">DJI AGRAS T50</div>
            <h3 style="margin:0.4rem 0; color:white">Tratamente aeriene de precizie</h3>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.8rem; margin-top:1rem; font-size:0.85rem;">
                <div><span style="color:#74c69d; font-weight:700">40L</span> rezervor lichid</div>
                <div><span style="color:#74c69d; font-weight:700">50kg</span> rezervor granule</div>
                <div><span style="color:#74c69d; font-weight:700">8 L/min</span> debit maxim</div>
                <div><span style="color:#74c69d; font-weight:700">9m</span> lățime lucru</div>
                <div><span style="color:#74c69d; font-weight:700">40-60 ha/h</span> acoperire</div>
                <div><span style="color:#74c69d; font-weight:700">RTK</span> GPS centimetric</div>
                <div><span style="color:#74c69d; font-weight:700">10-15 L/ha</span> doze aeriene</div>
                <div><span style="color:#74c69d; font-weight:700">5-7 m/s</span> viteză optimă</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Alerta sezoniera
    st.markdown("---")
    alerte = {
        (3,4,5): ("#e8f5e9","#2d6a4f","#4caf50","🌱 Primăvară", "Tratamente fungicide preventive la grâu și orz, monitoring gândac lucios la rapiță, erbicidate la porumb și floarea soarelui."),
        (6,7,8): ("#fff8e1","#e65100","#f9a825","☀️ Vară", "Orzul se recoltează primul. Sfredelitorul porumbului în zbor. PHI la lucernă înainte de cosit. Monitorizare mana la fl. soarelui."),
        (9,10,11): ("#fff3e0","#bf360c","#ff7043","🍂 Toamnă", "Semănat grâu și orz. Tratament fungicid la sămânță și în vegetație la rapiță. Pregătire sol pentru sezonul următor."),
        (12,1,2): ("#e3f2fd","#0d47a1","#42a5f5","❄️ Iarnă", "Verifică iernarea rapiței și grâului. Planifică schemele de tratamente. Calibrează drona T50 pentru sezonul următor."),
    }
    for luni, (bg, tc, bc, titlu, text) in alerte.items():
        if luna in luni:
            st.markdown(f"""<div class="season-box" style="background:{bg};color:{tc};border-color:{bc}">
                <b>{titlu} — Atenție:</b> {text}
            </div>""", unsafe_allow_html=True)

    # Intrebari rapide per cultura
    st.markdown("---")
    st.markdown("### ⚡ Întrebări frecvente per cultură")
    cultura_sel = st.selectbox("Alege cultura:", list(CULTURI.keys()), label_visibility="collapsed")
    if cultura_sel:
        c1, c2 = st.columns(2)
        for j, q in enumerate(CULTURI[cultura_sel]["intrebari"]):
            with c1 if j % 2 == 0 else c2:
                if st.button(f"💬 {q[:58]}{'...' if len(q)>58 else ''}", key=f"q_{cultura_sel}_{j}", use_container_width=True):
                    st.session_state.quick_q = q
                    st.session_state.cultura_activa = cultura_sel
                    st.session_state.switch_to_chat = True
                    st.rerun()

# ───────────────────────────────────────────────────────────────────
# TAB 2: CHAT
# ───────────────────────────────────────────────────────────────────

with tab_chat:
    # Switch automat la acest tab când vine din Culturile Mele
    if st.session_state.get("switch_to_chat"):
        st.session_state.switch_to_chat = False
        st.markdown("""
        <script>
            setTimeout(function() {
                const tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
                if (tabs.length >= 2) { tabs[1].click(); }
            }, 100);
        </script>
        """, unsafe_allow_html=True)

    if not st.session_state.api_key:
        st.markdown("""
        <div style="background:rgba(10,25,16,0.7);border:1px solid rgba(244,208,63,0.3);border-radius:16px;
             padding:2rem;text-align:center;max-width:500px;margin:2rem auto;">
            <div style="font-size:2.5rem;margin-bottom:1rem">🔑</div>
            <div style="font-weight:800;font-size:1.1rem;color:#f4d03f;margin-bottom:0.5rem">API Key necesar</div>
            <div style="color:rgba(255,255,255,0.6);font-size:0.88rem;margin-bottom:1.5rem">
                Introdu cheia API Anthropic pentru a activa agentul agronom.<br>
                O găsești în sidebar (stânga) sau o poți introduce mai jos.
            </div>
        </div>
        """, unsafe_allow_html=True)
        col_key1, col_key2, col_key3 = st.columns([1, 2, 1])
        with col_key2:
            inline_key = st.text_input("🔑 Introdu API Key Anthropic:", type="password",
                                        placeholder="sk-ant-api03-...",
                                        help="Obții cheia de la console.anthropic.com")
            if inline_key:
                st.session_state.api_key = inline_key
                st.rerun()
            st.markdown("[Creează cont și obține API Key gratuit →](https://console.anthropic.com)",
                        unsafe_allow_html=False)
    else:
        if st.session_state.cultura_activa:
            cdata = CULTURI[st.session_state.cultura_activa]
            label_cult = st.session_state.cultura_activa.split(" ", 1)[1]
            col_badge, col_reset = st.columns([3,1])
            with col_badge:
                st.markdown(f"""<div style="background:{cdata['color_bg']};border:2px solid {cdata['color_border']};
                    border-radius:10px;padding:0.6rem 1rem;font-weight:700;color:{cdata['color_text']};font-size:0.9rem">
                    {st.session_state.cultura_activa} — Consultație activă ✅</div>""", unsafe_allow_html=True)
            with col_reset:
                if st.button("✕ Resetează", key="rst_cult"):
                    st.session_state.cultura_activa = None
                    st.rerun()

        if not st.session_state.messages:
            st.markdown(f"""
            <div style="text-align:center; padding:3rem 1rem; color:#aaa;">
                <div style="font-size:3.5rem">{sezon_icon}</div>
                <h3 style="color:#2d6a4f; margin:1rem 0 0.5rem 0">Bun venit, Christian!</h3>
                <p style="max-width:400px; margin:0 auto">Selectează o cultură din tab-ul <b>Culturile Mele</b> sau descrie direct problema din câmp. Poți trimite și poze pentru diagnostic instant.</p>
            </div>""", unsafe_allow_html=True)
        else:
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    text = msg["content"] if isinstance(msg["content"], str) else next(
                        (b["text"] for b in msg["content"] if isinstance(b,dict) and b.get("type")=="text"), "")
                    has_img = isinstance(msg["content"], list) and any(
                        isinstance(b,dict) and b.get("type")=="image" for b in msg["content"])
                    st.markdown(f"""<div class="msg-user">
                        <div class="msg-label">👨‍🌾 tu {"· 📷 imagine atașată" if has_img else ""}</div>
                        {text}</div>""", unsafe_allow_html=True)
                else:
                    content = msg["content"] if isinstance(msg["content"], str) else ""
                    content_html = content.replace("\n","<br>")
                    st.markdown(f"""<div class="msg-agent">
                        <div class="msg-label">🌱 agronom ai · acp engineer</div>
                        {content_html}</div>""", unsafe_allow_html=True)

        st.markdown("---")
        col_inp, col_img = st.columns([3, 1])
        with col_inp:
            default_val = ""
            if hasattr(st.session_state, "quick_q"):
                default_val = st.session_state.quick_q
                del st.session_state.quick_q
            user_input = st.text_area("", value=default_val,
                placeholder="Descrie problema, faza culturii, simptomele... sau încarcă o poză din câmp →",
                height=95, label_visibility="collapsed")
        with col_img:
            uploaded_image = st.file_uploader("📷 Poză câmp", type=["jpg","jpeg","png","webp"])
            send_btn = st.button("📤 Trimite", use_container_width=True, type="primary")

        if send_btn and (user_input.strip() or uploaded_image):
            if uploaded_image:
                img_data = base64.standard_b64encode(uploaded_image.read()).decode("utf-8")
                user_content = [
                    {"type":"image","source":{"type":"base64","media_type":uploaded_image.type,"data":img_data}},
                    {"type":"text","text": user_input.strip() or "Analizează imaginea și diagnostichează problema."}
                ]
            else:
                user_content = user_input.strip()
            st.session_state.messages.append({"role":"user","content":user_content})
            with st.spinner("🌱 Agronumul analizează..."):
                try:
                    client = anthropic.Anthropic(api_key=st.session_state.api_key)
                    resp = client.messages.create(model=CLAUDE_MODEL, max_tokens=2048, system=SYSTEM_PROMPT,
                        messages=[{"role":m["role"],"content":m["content"]} for m in st.session_state.messages])
                    st.session_state.messages.append({"role":"assistant","content":resp.content[0].text})
                    st.rerun()
                except anthropic.AuthenticationError:
                    st.error("❌ API Key invalid."); st.session_state.messages.pop()
                except Exception as e:
                    st.error(f"❌ Eroare: {e}"); st.session_state.messages.pop()

        if st.session_state.messages:
            ca, cb, cc = st.columns(3)
            with ca:
                if st.button("💾 Salvează consultația", use_container_width=True):
                    first = st.session_state.messages[0]["content"]
                    title = (first if isinstance(first,str) else next(
                        (b["text"] for b in first if b.get("type")=="text"), "Consultație"))[:60]
                    save_session(title, st.session_state.messages, st.session_state.cultura_activa or "General")
                    st.success("✅ Salvat!")
            with cb:
                if st.button("📄 Export PDF", use_container_width=True):
                    try:
                        pdf = FPDF(); pdf.set_auto_page_break(auto=True, margin=15); pdf.add_page()
                        pdf.set_font("Helvetica","B",18); pdf.set_text_color(27,67,50)
                        pdf.cell(0,12,"ACP ENGINEER - RAPORT AGRONOMIC",ln=True,align="C")
                        pdf.set_font("Helvetica","",10); pdf.set_text_color(100,100,100)
                        pdf.cell(0,7,f"Data: {date.today().strftime('%d.%m.%Y')} | Cultura: {st.session_state.cultura_activa or 'General'}",ln=True,align="C")
                        pdf.ln(4); pdf.set_draw_color(45,106,79); pdf.line(10,pdf.get_y(),200,pdf.get_y()); pdf.ln(4)
                        for i,msg in enumerate(st.session_state.messages):
                            if msg["role"]=="user":
                                text = msg["content"] if isinstance(msg["content"],str) else next(
                                    (b["text"] for b in msg["content"] if b.get("type")=="text"),"[Imagine]")
                                pdf.set_font("Helvetica","B",11); pdf.set_text_color(45,106,79)
                                pdf.cell(0,8,f"INTREBARE {(i//2)+1}:",ln=True)
                                pdf.set_font("Helvetica","",10); pdf.set_text_color(50,50,50)
                                pdf.multi_cell(0,6,text.encode('latin-1','replace').decode('latin-1'))
                            else:
                                pdf.set_font("Helvetica","B",11); pdf.set_text_color(27,67,50)
                                pdf.cell(0,8,"RECOMANDARE AGRONOM AI:",ln=True)
                                pdf.set_font("Helvetica","",10); pdf.set_text_color(50,50,50)
                                content = msg["content"] if isinstance(msg["content"],str) else ""
                                pdf.multi_cell(0,6,content.encode('latin-1','replace').decode('latin-1'))
                                pdf.ln(2); pdf.set_draw_color(200,230,210); pdf.line(10,pdf.get_y(),200,pdf.get_y()); pdf.ln(3)
                        pdf.set_font("Helvetica","I",8); pdf.set_text_color(150,150,150)
                        pdf.cell(0,8,"ACP Engineer · Agronom AI Pro · Recomandarile sunt orientative",ln=True,align="C")
                        st.download_button("⬇️ Descarcă PDF", data=bytes(pdf.output()),
                            file_name=f"raport_agro_{date.today().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf", use_container_width=True)
                    except Exception as e: st.error(f"Eroare PDF: {e}")
            with cc:
                if st.button("🗑️ Conversație nouă", use_container_width=True):
                    st.session_state.messages = []; st.rerun()

# ───────────────────────────────────────────────────────────────────
# TAB 3: CALCULATOR T50
# ───────────────────────────────────────────────────────────────────

with tab_t50:
    col_title, col_img_d = st.columns([2,1])
    with col_title:
        st.markdown("### 🚁 Calculator Tratamente DJI Agras T50")
        st.markdown("Calculează cantitățile exacte de produs și apă pentru orice suprafață.")
    with col_img_d:
        st.markdown(f'<div style="transform:scale(0.7);transform-origin:top right">{SVG_DRONA}</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        cultura_calc = st.selectbox("🌾 Cultura tratată", list(CULTURI.keys()))
        suprafata = st.number_input("📐 Suprafața (ha)", 0.1, 5000.0, 10.0, 0.5)
        tip_produs = st.selectbox("🧪 Tip produs", ["Fungicid","Insecticid","Erbicid","Fertilizant foliar","Regulator creștere"])
        doza_prod = st.number_input("💊 Doza produs (L sau kg/ha)", 0.01, 50.0, 1.5, 0.05)
        volum_apa = st.number_input("💧 Volum soluție/ha (L/ha)", 5.0, 30.0, 12.0, 1.0)
    with c2:
        viteza = st.slider("🚀 Viteză zbor (m/s)", 2, 10, 6)
        inaltime = st.slider("📏 Înălțime zbor (m)", 1, 8, 3)
        overlap = st.slider("🔁 Suprapunere treceri (%)", 0, 30, 10)
        rezervor = st.number_input("🛢️ Capacitate rezervor (L)", 5.0, 40.0, 40.0, 5.0)

    if st.button("⚙️ Calculează doze T50", type="primary", use_container_width=True):
        vol_total = suprafata * volum_apa
        prod_total = suprafata * doza_prod
        apa_total = vol_total - prod_total
        nr_rez = vol_total / rezervor
        nr_umpleri = max(1, round(nr_rez + 0.49))
        prod_rez = prod_total / nr_umpleri
        apa_rez = apa_total / nr_umpleri
        latimi = {1:5.5,2:7.0,3:9.0,4:10.5,5:12.0,6:13.0,7:14.0,8:15.0}
        lat = latimi.get(inaltime, 9.0) * (1 - overlap/100)
        acop = (viteza * lat * 3600) / 10000
        t_zbor = suprafata / acop
        t_total = t_zbor + nr_umpleri * 0.15
        debit = (volum_apa * viteza * lat) / 600
        ok = debit <= 8.0

        cdata = CULTURI[cultura_calc]
        label = cultura_calc.split(" ",1)[1]
        st.markdown(f"""
        <div class="calc-result">
            <h3 style="color:#1b4332;margin:0 0 1rem 0">📊 {suprafata} ha de {label} · {tip_produs}</h3>
            <div class="calc-row"><span>Produs necesar total</span><span><b>{prod_total:.2f} L/kg</b></span></div>
            <div class="calc-row"><span>Apă necesară total</span><span><b>{apa_total:.0f} L</b></span></div>
            <div class="calc-row"><span>Volum total soluție</span><span><b>{vol_total:.0f} L</b></span></div>
            <div class="calc-row"><span>Număr umpleri rezervor ({rezervor:.0f}L)</span><span><b>{nr_umpleri} umpleri</b></span></div>
            <div class="calc-row"><span>Produs per umplere</span><span><b>{prod_rez:.2f} L/kg</b></span></div>
            <div class="calc-row"><span>Apă per umplere</span><span><b>{apa_rez:.0f} L</b></span></div>
        </div>""", unsafe_allow_html=True)

        r1, r2, r3 = st.columns(3)
        with r1:
            st.metric("⏱️ Timp total", f"{t_total:.1f} ore")
            st.metric("🚀 Acoperire", f"{acop:.1f} ha/oră")
        with r2:
            st.metric("📏 Lățime lucru", f"{lat:.1f} m")
            st.metric("🔄 Umpleri", f"{nr_umpleri}")
        with r3:
            st.metric("💧 Debit necesar", f"{debit:.2f} L/min",
                      delta="✅ OK" if ok else "⚠️ Depășit!", delta_color="normal" if ok else "inverse")
            st.metric("✈️ Timp zbor", f"{t_zbor:.1f} ore")

        if not ok:
            st.error(f"⚠️ Debitul calculat ({debit:.1f} L/min) depășește maximul T50 (8 L/min). Reduce viteza sau mărește volumul de apă.")
        else:
            st.success(f"✅ Parametrii optimi pentru DJI Agras T50 — {label}!")
        st.info(f"📋 **Instrucțiuni pilot:** {viteza} m/s · {inaltime}m înălțime · {prod_rez:.2f} L/kg produs + {apa_rez:.0f}L apă per umplere · {nr_umpleri} curse total")

# ───────────────────────────────────────────────────────────────────
# TAB 4: ISTORIC
# ───────────────────────────────────────────────────────────────────

with tab_history:
    st.markdown("### 📂 Istoricul consultațiilor")
    sessions = get_sessions()
    if not sessions:
        st.markdown("<div style='text-align:center;padding:3rem;color:#aaa'><div style='font-size:3rem'>📂</div><p>Nicio consultație salvată încă.</p></div>", unsafe_allow_html=True)
    else:
        culturi_in_istoric = list(set(s[2] for s in sessions))
        filtru = st.selectbox("Filtrează după cultură:", ["Toate"] + culturi_in_istoric)
        sessions_f = sessions if filtru == "Toate" else [s for s in sessions if s[2] == filtru]
        st.markdown(f"**{len(sessions_f)} consultații**")
        for sess in sessions_f:
            sid, title, cultura, created_at, msgs_json = sess
            msgs = json.loads(msgs_json)
            n = len([m for m in msgs if m["role"]=="user"])
            dt = datetime.fromisoformat(created_at).strftime("%d.%m.%Y %H:%M")
            cdata = CULTURI.get(cultura, {})
            border_color = cdata.get("color_border", "#52b788")
            with st.expander(f"{cultura} · {title[:50]} · {dt} ({n} întrebări)"):
                for msg in msgs:
                    if msg["role"]=="user":
                        t = msg["content"] if isinstance(msg["content"],str) else next(
                            (b["text"] for b in msg["content"] if isinstance(b,dict) and b.get("type")=="text"),"[Imagine]")
                        st.markdown(f"**👨‍🌾 Tu:** {t}")
                    else:
                        c = msg["content"] if isinstance(msg["content"],str) else ""
                        st.markdown(f"**🌱 Agronom AI:** {c[:400]}{'...' if len(c)>400 else ''}")
                    st.markdown("---")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("📂 Reîncarcă", key=f"l_{sid}", use_container_width=True):
                        st.session_state.messages = msgs
                        st.success("✅ Reîncărcat! Mergi la Consultație.")
                with c2:
                    if st.button("🗑️ Șterge", key=f"d_{sid}", use_container_width=True):
                        delete_session(sid); st.rerun()

# ═══════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════

st.markdown(f"""
<div style="text-align:center;padding:2rem 0 1rem 0;margin-top:2rem;border-top:2px solid #e8f5e9;">
    <div style="font-size:1.5rem">🌱</div>
    <div style="font-weight:800;color:#1b4332;font-size:1rem;margin:0.3rem 0">ACP Engineer · Agronom AI Pro</div>
    <div style="color:#aaa;font-size:0.78rem">Powered by Claude Opus AI (Anthropic) · {date.today().year} · România</div>
    <div style="color:#ccc;font-size:0.7rem;margin-top:0.3rem">Recomandările sunt orientative — consultați un specialist înainte de orice tratament fitosanitar</div>
</div>
""", unsafe_allow_html=True)
