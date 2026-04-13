"""
🌱 Agent Agronom AI — Versiunea PRO
Powered by Claude (Anthropic)
"""

import streamlit as st
import anthropic
import base64
import sqlite3
import json
import io
from datetime import datetime, date
from fpdf import FPDF

# ═══════════════════════════════════════════════════════════════════
# CONFIGURARE
# ═══════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Agronom AI Pro",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Parolă de acces (schimbă aceasta!)
APP_PASSWORD = "ACPengineer"
CLAUDE_MODEL = "claude-opus-4-6"

# ═══════════════════════════════════════════════════════════════════
# CSS PROFESIONAL
# ═══════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Header */
    .pro-header {
        background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 50%, #40916c 100%);
        padding: 1.8rem 2.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(29, 67, 50, 0.3);
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .pro-header h1 { margin: 0; font-size: 1.8rem; font-weight: 700; }
    .pro-header p { margin: 0.3rem 0 0 0; opacity: 0.85; font-size: 0.95rem; }
    .badge {
        background: #74c69d;
        color: #1b4332;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 20px;
        letter-spacing: 0.5px;
    }

    /* Chat bubbles */
    .msg-user {
        background: linear-gradient(135deg, #d8f3dc, #b7e4c7);
        border-radius: 18px 18px 4px 18px;
        padding: 1rem 1.2rem;
        margin: 0.6rem 0 0.6rem 3rem;
        border: 1px solid #95d5b2;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .msg-agent {
        background: white;
        border-radius: 18px 18px 18px 4px;
        padding: 1rem 1.2rem;
        margin: 0.6rem 3rem 0.6rem 0;
        border: 1px solid #e8f5e9;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }
    .msg-label {
        font-size: 0.75rem;
        font-weight: 600;
        opacity: 0.65;
        margin-bottom: 0.3rem;
    }

    /* Cards */
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid #e8f5e9;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .stat-num { font-size: 2rem; font-weight: 700; color: #2d6a4f; }
    .stat-label { font-size: 0.8rem; color: #888; margin-top: 0.2rem; }

    /* Calculator */
    .calc-result {
        background: linear-gradient(135deg, #d8f3dc, #b7e4c7);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #95d5b2;
        margin-top: 1rem;
    }
    .calc-result h3 { color: #1b4332; margin-top: 0; }
    .calc-row {
        display: flex;
        justify-content: space-between;
        padding: 0.4rem 0;
        border-bottom: 1px solid #95d5b2;
        font-size: 0.95rem;
    }
    .calc-row:last-child { border-bottom: none; font-weight: 700; }

    /* History */
    .hist-item {
        background: white;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #52b788;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        cursor: pointer;
    }
    .hist-item:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .hist-date { font-size: 0.75rem; color: #888; }
    .hist-title { font-weight: 600; color: #1b4332; margin-top: 0.2rem; }
    .hist-preview { font-size: 0.85rem; color: #555; margin-top: 0.3rem; }

    /* Login */
    .login-box {
        max-width: 400px;
        margin: 5rem auto;
        background: white;
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        text-align: center;
    }

    /* Sidebar */
    .sidebar-card {
        background: white;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.8rem;
        border: 1px solid #e8f5e9;
        font-size: 0.88rem;
    }
    .sidebar-card strong { color: #1b4332; }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #f1f8e9;
        border-radius: 10px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.2s;
    }

    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# BAZA DE DATE (SQLite)
# ═══════════════════════════════════════════════════════════════════

def init_db():
    conn = sqlite3.connect("agronom_history.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            created_at TEXT,
            messages TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_session(title, messages):
    conn = sqlite3.connect("agronom_history.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO sessions (title, created_at, messages) VALUES (?, ?, ?)",
        (title, datetime.now().isoformat(), json.dumps(messages, ensure_ascii=False))
    )
    session_id = c.lastrowid
    conn.commit()
    conn.close()
    return session_id

def get_sessions(limit=20):
    conn = sqlite3.connect("agronom_history.db")
    c = conn.cursor()
    c.execute("SELECT id, title, created_at, messages FROM sessions ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_session(session_id):
    conn = sqlite3.connect("agronom_history.db")
    c = conn.cursor()
    c.execute("SELECT id, title, created_at, messages FROM sessions WHERE id=?", (session_id,))
    row = c.fetchone()
    conn.close()
    return row

def delete_session(session_id):
    conn = sqlite3.connect("agronom_history.db")
    c = conn.cursor()
    c.execute("DELETE FROM sessions WHERE id=?", (session_id,))
    conn.commit()
    conn.close()

init_db()

# ═══════════════════════════════════════════════════════════════════
# PROMPT DE SISTEM
# ═══════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = f"""Ești un inginer agronom expert cu peste 20 de ani de experiență în:
- Agricultura din România și Europa de Est
- Culturi de câmp: grâu, porumb, floarea soarelui, rapiță, soia, sfeclă de zahăr, legume
- Viticultură și pomicultură
- Diagnostic boli, dăunători și deficiențe nutriționale
- Recomandări fitosanitare și îngrășăminte (OMFP 1182/2005 și Regulamentele UE)
- Drona agricolă DJI Agras T50 pentru tratamente aeriene

**Specificații DJI Agras T50:**
- Rezervor: 40L lichid / 50kg granule
- Debit maxim: 8 L/min, 8 duze
- Acoperire: 40-60 ha/oră (condiții optime)
- Lățime de lucru: 9 m la 3 m înălțime
- Sistem RTK pentru precizie GPS centimetrică
- Evitare obstacole: radar omnidirectional 360°
- Doze aeriene recomandate: 10-15 L/ha lichid diluat
- Viteză optimă zbor: 5-7 m/s pentru pesticide

**Protocol răspuns:**
1. Răspunzi ÎNTOTDEAUNA în română
2. Dai substanța activă + denumiri comerciale disponibile în RO + doze exacte
3. Menționezi PHI (pauza pre-recoltare) și nr. maxim de tratamente/sezon
4. Specifici dacă tratamentul e omologat pentru aplicare cu drona
5. La imagini: identifici problema, explici cauzele, dai soluția imediată + preventivă
6. Ești concis și practic — agri­cultorul citește în teren, nu la birou
7. Data curentă: {date.today().strftime('%d %B %Y')}

Structurează răspunsul cu: **Diagnostic** → **Tratament** → **Doze** → **Aplicare cu T50** (dacă e relevant) → **Prevenție**."""

# ═══════════════════════════════════════════════════════════════════
# AUTENTIFICARE
# ═══════════════════════════════════════════════════════════════════

def login_page():
    st.markdown("""
    <div class="login-box">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🌱</div>
        <h2 style="color: #1b4332; margin-bottom: 0.3rem;">Agronom AI Pro</h2>
        <p style="color: #666; margin-bottom: 2rem;">Acces securizat</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Autentificare")
        password = st.text_input("Parolă de acces", type="password", placeholder="Introdu parola...")
        if st.button("Intră în aplicație →", use_container_width=True, type="primary"):
            if password == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Parolă incorectă. Încearcă din nou.")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login_page()
    st.stop()

# ═══════════════════════════════════════════════════════════════════
# INIȚIALIZARE SESIUNE
# ═══════════════════════════════════════════════════════════════════

if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "session_saved" not in st.session_state:
    st.session_state.session_saved = False

# ═══════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🌱 Agronom AI Pro")
    st.markdown("---")

    # API Key
    st.markdown("**🔑 API Key Anthropic**")
    api_key_input = st.text_input(
        "API Key",
        type="password",
        value=st.session_state.api_key,
        placeholder="sk-ant-...",
        label_visibility="collapsed"
    )
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.success("✅ Conectat")
    st.markdown("[Obține API Key →](https://console.anthropic.com)")

    st.markdown("---")

    # Statistici rapide
    sessions_list = get_sessions()
    total_msgs = sum(len(json.loads(s[3])) for s in sessions_list) if sessions_list else 0

    st.markdown("**📊 Statistici**")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Consultații", len(sessions_list))
    with col_b:
        st.metric("Mesaje", total_msgs + len(st.session_state.messages))

    st.markdown("---")

    # Întrebări rapide
    st.markdown("**⚡ Scurtături**")
    quick = {
        "🌾 Boli grâu": "Care sunt cele mai comune boli ale grâului în România primăvara și cum le tratez? Incluzând setări T50.",
        "🌽 Dăunători porumb": "Ce dăunători atacă porumbul în România și ce tratamente aplici cu drona T50?",
        "🍇 Mana viță": "Cum combat mana la viță de vie? Doza, produse omologate, PHI.",
        "🚁 Setări T50": "Care sunt setările optime ale dronei DJI Agras T50 pentru fungicide la grâu?",
        "🌿 Deficit azot": "Cum recunosc deficitul de azot? Simptome pe grâu, porumb și rapiță.",
        "📅 Calendar mai": "Ce tratamente și lucrări agricole sunt recomandate în luna mai în România?",
        "🛢️ Mix rezervor T50": "Ce produse pot mixa în același rezervor T50? Compatibilități pesticide.",
        "⚠️ PHI rapiță": "Care e pauza pre-recoltare (PHI) pentru cele mai comune fungicide la rapiță?",
    }
    for label, question in quick.items():
        if st.button(label, use_container_width=True, key=f"q_{label}"):
            st.session_state.quick_q = question

    st.markdown("---")

    # Buton logout
    if st.button("🚪 Deconectare", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.messages = []
        st.rerun()

# ═══════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════

st.markdown("""
<div class="pro-header">
    <div style="font-size: 3rem;">🌱</div>
    <div>
        <h1>Agent Inginer Agronom AI <span class="badge">PRO</span></h1>
        <p>Expert în culturi, boli, tratamente fitosanitare și drona DJI Agras T50 • România</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# TABURI PRINCIPALE
# ═══════════════════════════════════════════════════════════════════

tab_chat, tab_t50, tab_history = st.tabs([
    "💬 Consultație",
    "🚁 Calculator T50",
    "📂 Istoric"
])

# ───────────────────────────────────────────────────────────────────
# TAB 1: CHAT
# ───────────────────────────────────────────────────────────────────

with tab_chat:
    if not st.session_state.api_key:
        st.info("🔑 Introdu API Key-ul Anthropic în sidebar pentru a începe consultația.")
    else:
        # Mesaje
        chat_area = st.container()
        with chat_area:
            if not st.session_state.messages:
                st.markdown("""
                <div style="text-align:center; padding: 3rem; color: #888;">
                    <div style="font-size:3rem">🌱</div>
                    <h3 style="color:#2d6a4f">Bun venit, agronom!</h3>
                    <p>Descrie problema, încarcă o poză din câmp sau alege o scurtătură din sidebar.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        text = msg["content"] if isinstance(msg["content"], str) else next(
                            (b["text"] for b in msg["content"] if isinstance(b, dict) and b.get("type") == "text"), ""
                        )
                        has_image = isinstance(msg["content"], list) and any(
                            isinstance(b, dict) and b.get("type") == "image" for b in msg["content"]
                        )
                        img_badge = " 📷" if has_image else ""
                        st.markdown(f"""
                        <div class="msg-user">
                            <div class="msg-label">👨‍🌾 TU{img_badge}</div>
                            {text}
                        </div>""", unsafe_allow_html=True)
                    else:
                        content = msg["content"] if isinstance(msg["content"], str) else ""
                        # Convertim newlines în HTML
                        content_html = content.replace("\n", "<br>")
                        st.markdown(f"""
                        <div class="msg-agent">
                            <div class="msg-label">🌱 AGRONOM AI</div>
                            {content_html}
                        </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # Input
        col_inp, col_img = st.columns([3, 1])
        with col_inp:
            default_val = ""
            if hasattr(st.session_state, "quick_q"):
                default_val = st.session_state.quick_q
                del st.session_state.quick_q
            user_input = st.text_area(
                "Întrebarea ta:",
                value=default_val,
                placeholder="Ex: Am observat pete brune cu halou galben pe frunzele de grâu. Ce boală este? Pot aplica cu T50?",
                height=90,
                label_visibility="collapsed"
            )
        with col_img:
            uploaded_image = st.file_uploader(
                "📷 Poză din câmp",
                type=["jpg", "jpeg", "png", "webp"],
                help="Adaugă o imagine pentru diagnostic vizual"
            )
            send_btn = st.button("📤 Trimite", use_container_width=True, type="primary")

        # Trimitere mesaj
        if send_btn and (user_input.strip() or uploaded_image):
            if isinstance(msg["content"], list) and any(
                isinstance(b, dict) and b.get("type") == "image" for b in msg["content"]
            ) if st.session_state.messages and st.session_state.messages[-1]["role"] == "user" else False:
                pass

            # Build content
            if uploaded_image:
                img_data = base64.standard_b64encode(uploaded_image.read()).decode("utf-8")
                user_content = [
                    {"type": "image", "source": {"type": "base64", "media_type": uploaded_image.type, "data": img_data}},
                    {"type": "text", "text": user_input.strip() or "Analizează această imagine și diagnostichează problema plantei."}
                ]
            else:
                user_content = user_input.strip()

            st.session_state.messages.append({"role": "user", "content": user_content})
            st.session_state.session_saved = False

            with st.spinner("🌱 Agronumul analizează..."):
                try:
                    client = anthropic.Anthropic(api_key=st.session_state.api_key)
                    response = client.messages.create(
                        model=CLAUDE_MODEL,
                        max_tokens=2048,
                        system=SYSTEM_PROMPT,
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    )
                    answer = response.content[0].text
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.rerun()
                except anthropic.AuthenticationError:
                    st.error("❌ API Key invalid.")
                    st.session_state.messages.pop()
                except Exception as e:
                    st.error(f"❌ Eroare: {str(e)}")
                    st.session_state.messages.pop()

        # Butoane acțiuni sesiune
        if st.session_state.messages:
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)

            with col_s1:
                if st.button("💾 Salvează consultația", use_container_width=True):
                    # Generăm titlu automat din primul mesaj
                    first_msg = st.session_state.messages[0]["content"]
                    if isinstance(first_msg, list):
                        title_text = next((b["text"] for b in first_msg if b.get("type") == "text"), "Consultație cu imagine")
                    else:
                        title_text = first_msg
                    title = title_text[:60] + ("..." if len(title_text) > 60 else "")
                    save_session(title, st.session_state.messages)
                    st.session_state.session_saved = True
                    st.success("✅ Consultație salvată!")

            with col_s2:
                if st.button("📄 Export PDF", use_container_width=True):
                    st.session_state.generate_pdf = True

            with col_s3:
                if st.button("🗑️ Conversație nouă", use_container_width=True):
                    st.session_state.messages = []
                    st.session_state.session_saved = False
                    st.rerun()

            with col_s4:
                msg_count = len([m for m in st.session_state.messages if m["role"] == "user"])
                st.markdown(f"<div style='text-align:center; padding:0.5rem; color:#888; font-size:0.85rem'>{msg_count} întrebări</div>", unsafe_allow_html=True)

        # Generare PDF
        if hasattr(st.session_state, "generate_pdf") and st.session_state.generate_pdf:
            st.session_state.generate_pdf = False
            try:
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()

                # Font pentru română (folosim built-in Helvetica, fără diacritice)
                pdf.set_font("Helvetica", "B", 20)
                pdf.set_text_color(27, 67, 50)
                pdf.cell(0, 12, "RAPORT CONSULTATIE AGRONOMICA", ln=True, align="C")
                pdf.set_font("Helvetica", "", 11)
                pdf.set_text_color(100, 100, 100)
                pdf.cell(0, 8, f"Data: {date.today().strftime('%d.%m.%Y')} | Powered by Claude AI", ln=True, align="C")
                pdf.ln(8)

                # Linie separator
                pdf.set_draw_color(45, 106, 79)
                pdf.set_line_width(0.8)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(6)

                for i, msg in enumerate(st.session_state.messages):
                    if msg["role"] == "user":
                        text = msg["content"] if isinstance(msg["content"], str) else next(
                            (b["text"] for b in msg["content"] if b.get("type") == "text"), "[Imagine atașată]"
                        )
                        pdf.set_font("Helvetica", "B", 11)
                        pdf.set_text_color(45, 106, 79)
                        pdf.cell(0, 8, f"INTREBARE {(i//2)+1}:", ln=True)
                        pdf.set_font("Helvetica", "", 10)
                        pdf.set_text_color(50, 50, 50)
                        # Eliminăm diacritice pentru compatibilitate FPDF built-in
                        safe_text = text.encode('latin-1', 'replace').decode('latin-1')
                        pdf.multi_cell(0, 6, safe_text)
                        pdf.ln(3)
                    else:
                        pdf.set_font("Helvetica", "B", 11)
                        pdf.set_text_color(27, 67, 50)
                        pdf.cell(0, 8, "RECOMANDARE AGRONOM AI:", ln=True)
                        pdf.set_font("Helvetica", "", 10)
                        pdf.set_text_color(50, 50, 50)
                        content = msg["content"] if isinstance(msg["content"], str) else ""
                        safe_content = content.encode('latin-1', 'replace').decode('latin-1')
                        pdf.multi_cell(0, 6, safe_content)
                        pdf.ln(4)
                        pdf.set_draw_color(200, 230, 210)
                        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                        pdf.ln(4)

                # Footer
                pdf.set_font("Helvetica", "I", 8)
                pdf.set_text_color(150, 150, 150)
                pdf.cell(0, 8, "Raport generat de Agronom AI Pro | Recomandarile sunt orientative", ln=True, align="C")

                pdf_bytes = pdf.output()
                st.download_button(
                    label="⬇️ Descarcă Raport PDF",
                    data=bytes(pdf_bytes),
                    file_name=f"consultatie_agro_{date.today().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Eroare generare PDF: {e}")

# ───────────────────────────────────────────────────────────────────
# TAB 2: CALCULATOR DRONĂ T50
# ───────────────────────────────────────────────────────────────────

with tab_t50:
    st.markdown("### 🚁 Calculator Tratamente DJI Agras T50")
    st.markdown("Introdu parametrii tratamentului și obții cantitățile exacte de produs și apă.")

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        suprafata = st.number_input("📐 Suprafața de tratat (ha)", min_value=0.1, max_value=5000.0, value=10.0, step=0.5)
        doza_prod = st.number_input("💊 Doza produs (L/ha sau kg/ha)", min_value=0.0, max_value=50.0, value=1.5, step=0.1)
        volum_apa = st.number_input("💧 Volum total soluție/ha (L/ha)", min_value=5.0, max_value=30.0, value=12.0, step=1.0,
                                     help="Recomandat: 10-15 L/ha pentru aplicații aeriene cu T50")
        tip_produs = st.selectbox("🧪 Tip produs", ["Fungicid", "Insecticid", "Erbicid", "Fertilizant foliar", "Regulator creștere"])

    with col_c2:
        viteza_zbor = st.slider("🚀 Viteza de zbor (m/s)", min_value=2, max_value=10, value=6,
                                  help="Recomandat: 5-7 m/s pentru pesticide")
        inaltime_zbor = st.slider("📏 Înălțimea de zbor (m)", min_value=1, max_value=8, value=3,
                                    help="3m = lățime lucru 9m; 2m = mai precis dar mai lent")
        overlap = st.slider("🔁 Suprapunere treceri (%)", min_value=0, max_value=30, value=10)
        rezervor_cap = st.number_input("🛢️ Capacitate rezervor folosit (L)", min_value=5.0, max_value=40.0, value=40.0, step=5.0)

    st.markdown("---")

    if st.button("⚙️ Calculează", type="primary", use_container_width=True):
        # Calcule
        volum_total = suprafata * volum_apa  # L total soluție
        produs_total = suprafata * doza_prod  # L sau kg produs
        apa_totala = volum_total - produs_total  # L apă pură
        nr_rezervoare = volum_total / rezervor_cap
        produs_per_rezervor = produs_total / nr_rezervoare if nr_rezervoare > 0 else 0
        apa_per_rezervor = apa_totala / nr_rezervoare if nr_rezervoare > 0 else 0

        # Lățime de lucru în funcție de înălțime
        latimi = {1: 5.5, 2: 7.0, 3: 9.0, 4: 10.5, 5: 12.0, 6: 13.0, 7: 14.0, 8: 15.0}
        latime_lucru = latimi.get(inaltime_zbor, 9.0) * (1 - overlap / 100)

        # Timp estimat
        viteza_ms = viteza_zbor
        acoperire_ha_ora = (viteza_ms * latime_lucru * 3600) / 10000
        timp_efectiv_ore = suprafata / acoperire_ha_ora
        nr_umpleri = max(1, round(nr_rezervoare + 0.5))
        timp_umpleri_ore = nr_umpleri * 0.15  # 9 min per umplere estimat
        timp_total_ore = timp_efectiv_ore + timp_umpleri_ore

        # Debit necesar
        debit_lmin = (volum_apa * viteza_zbor * latime_lucru) / 600
        debit_ok = debit_lmin <= 8.0

        # Afișare rezultate
        st.markdown(f"""
        <div class="calc-result">
            <h3>📊 Rezultate calcul — {suprafata} ha de {tip_produs.lower()}</h3>
            <div class="calc-row"><span>Produs necesar total</span><span><b>{produs_total:.2f} L/kg</b></span></div>
            <div class="calc-row"><span>Apă necesară total</span><span><b>{apa_totala:.0f} L</b></span></div>
            <div class="calc-row"><span>Volum total soluție</span><span><b>{volum_total:.0f} L</b></span></div>
            <div class="calc-row"><span>Număr umpleri rezervor ({rezervor_cap}L)</span><span><b>{nr_rezervoare:.1f} ≈ {nr_umpleri} umpleri</b></span></div>
            <div class="calc-row"><span>Produs / umplere rezervor</span><span><b>{produs_per_rezervor:.2f} L/kg</b></span></div>
            <div class="calc-row"><span>Apă / umplere rezervor</span><span><b>{apa_per_rezervor:.0f} L</b></span></div>
        </div>
        """, unsafe_allow_html=True)

        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.metric("⏱️ Timp total estimat", f"{timp_total_ore:.1f} ore")
            st.metric("🚀 Acoperire efectivă", f"{acoperire_ha_ora:.1f} ha/oră")
        with col_r2:
            st.metric("📏 Lățime lucru efectivă", f"{latime_lucru:.1f} m")
            st.metric("🔄 Nr. umpleri", f"{nr_umpleri}")
        with col_r3:
            debit_color = "normal" if debit_ok else "inverse"
            st.metric("💧 Debit necesar", f"{debit_lmin:.2f} L/min",
                      delta="✅ OK" if debit_ok else "⚠️ Prea mare!", delta_color=debit_color)
            st.metric("⏰ Timp zbor pur", f"{timp_efectiv_ore:.1f} ore")

        # Avertismente
        warnings = []
        if not debit_ok:
            warnings.append(f"⚠️ **Debitul calculat ({debit_lmin:.1f} L/min) depășește maximul T50 (8 L/min)**. Reduce viteza sau mărește volumul de apă.")
        if volum_apa < 8:
            warnings.append("⚠️ Volumul de soluție sub 8 L/ha poate fi insuficient pentru acoperire uniformă.")
        if viteza_zbor > 8 and tip_produs in ["Fungicid", "Insecticid"]:
            warnings.append("⚠️ Viteză mare pentru fungicide/insecticide — consideră reducerea la 5-6 m/s.")
        if inaltime_zbor > 4:
            warnings.append("⚠️ Înălțime mare crește riscul de derivă. Recomandat max 3-4m pentru pesticide.")

        if warnings:
            st.markdown("---")
            for w in warnings:
                st.warning(w)
        else:
            st.success("✅ Parametrii sunt optimi pentru drona DJI Agras T50!")

        st.markdown("---")
        st.markdown(f"""
        **📋 Instrucțiuni rapide pentru pilot:**
        Setează drona T50 la **{viteza_zbor} m/s** și **{inaltime_zbor}m înălțime**.
        La fiecare umplere: adaugă **{produs_per_rezervor:.2f} L/kg** de {tip_produs.lower()} și completează cu **{apa_per_rezervor:.0f}L apă**.
        Amestecă bine înainte de zbor. Efectuează **{nr_umpleri} curse de umplere** total.
        """)

# ───────────────────────────────────────────────────────────────────
# TAB 3: ISTORIC
# ───────────────────────────────────────────────────────────────────

with tab_history:
    st.markdown("### 📂 Istoricul consultațiilor")

    sessions = get_sessions()

    if not sessions:
        st.markdown("""
        <div style="text-align:center; padding: 3rem; color:#888;">
            <div style="font-size:3rem">📂</div>
            <p>Nicio consultație salvată încă.</p>
            <p>Mergi la tab-ul Consultație și salvează o conversație.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        col_h1, col_h2 = st.columns([2, 1])
        with col_h1:
            st.markdown(f"**{len(sessions)} consultații salvate**")
        with col_h2:
            if st.button("🔄 Actualizează", use_container_width=True):
                st.rerun()

        for sess in sessions:
            sess_id, title, created_at, messages_json = sess
            try:
                msgs = json.loads(messages_json)
                n_msgs = len([m for m in msgs if m["role"] == "user"])
                dt = datetime.fromisoformat(created_at).strftime("%d.%m.%Y %H:%M")
            except Exception:
                n_msgs = 0
                dt = created_at[:16]

            with st.expander(f"📋 {title[:70]} — {dt} ({n_msgs} întrebări)"):
                # Afișează conversația
                for msg in msgs:
                    if msg["role"] == "user":
                        text = msg["content"] if isinstance(msg["content"], str) else next(
                            (b["text"] for b in msg["content"] if isinstance(b, dict) and b.get("type") == "text"),
                            "[Imagine atașată]"
                        )
                        st.markdown(f"**👨‍🌾 Tu:** {text}")
                    else:
                        content = msg["content"] if isinstance(msg["content"], str) else ""
                        st.markdown(f"**🌱 Agronom AI:** {content[:500]}{'...' if len(content) > 500 else ''}")
                    st.markdown("---")

                col_h_a, col_h_b, col_h_c = st.columns(3)
                with col_h_a:
                    if st.button("📂 Reîncarcă în chat", key=f"load_{sess_id}", use_container_width=True):
                        st.session_state.messages = msgs
                        st.session_state.session_saved = True
                        st.success("✅ Consultație reîncărcată! Mergi la tab-ul Consultație.")
                with col_h_b:
                    if st.button("🗑️ Șterge", key=f"del_{sess_id}", use_container_width=True):
                        delete_session(sess_id)
                        st.rerun()
                with col_h_c:
                    st.markdown(f"<div style='text-align:center;padding:0.5rem;color:#888;font-size:0.8rem'>{n_msgs} întrebări</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#aaa;font-size:0.8rem'>🌱 Agronom AI Pro • Powered by Claude Opus (Anthropic) • "
    f"Versiunea PRO • {date.today().year} • Recomandările sunt orientative — consultați un specialist înainte de tratamente</div>",
    unsafe_allow_html=True
)
