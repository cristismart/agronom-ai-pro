# 🌱 Agronom AI Pro — Ghid Deployment

## ⚡ Pornire rapidă (local, pe calculator)

```bash
# 1. Instalează Python 3.10+ de la python.org

# 2. Instalează dependențele
pip install -r requirements.txt

# 3. Pornește aplicația
streamlit run app.py

# Aplicația se deschide la: http://localhost:8501
# Parola implicită: ferma2025
```

---

## 🌐 Deployment online — Railway.app (RECOMANDAT, ~$5/lună)

### Pas 1: Pregătire
1. Creează cont pe [github.com](https://github.com) (gratuit)
2. Creează un repository nou numit `agronom-ai-pro`
3. Urcă fișierele: `app.py`, `requirements.txt`

### Pas 2: Fișier Procfile (crează-l în GitHub)
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### Pas 3: Deploy pe Railway
1. Mergi la [railway.app](https://railway.app) → Sign in with GitHub
2. **New Project** → **Deploy from GitHub repo**
3. Selectează `agronom-ai-pro`
4. Mergi la **Variables** și adaugă:
   - `ANTHROPIC_API_KEY` = cheia ta API
5. **Deploy** → în 2-3 minute ești live!
6. Mergi la **Settings → Domains** → generezi un link public

### Rezultat
Aplicația ta va fi disponibilă la: `https://agronom-ai-pro.railway.app`
Accesibil de pe orice device, 24/7.

---

## 🔑 Schimbarea parolei

În fișierul `app.py`, linia 29:
```python
APP_PASSWORD = "ferma2025"  # ← Schimbă cu parola ta
```

---

## 💰 Costuri lunare estimate

| Serviciu | Cost |
|---|---|
| Railway.app (hosting) | ~$5/lună |
| API Anthropic Claude | ~$5-20/lună |
| **Total** | **~$10-25/lună** |

> Estimare API: ~$8 pentru 500 de conversații/lună cu imagini

---

## ✅ Ce include versiunea PRO

| Funcționalitate | Status |
|---|---|
| Chat cu Agronom AI (română) | ✅ |
| Diagnostic din imagini (poze din câmp) | ✅ |
| Autentificare cu parolă | ✅ |
| Calculator doze dronă T50 | ✅ |
| Istoric consultații salvat | ✅ |
| Export raport PDF | ✅ |
| 8 scurtături rapide predefinite | ✅ |
| Design profesional verde | ✅ |
| Acces de pe orice device | ✅ |
