import streamlit as st
import requests
import json
import base64
import os
from PIL import Image
import io
import random
import time
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  LANGUAGE CONFIG
# ─────────────────────────────────────────────
LANGUAGES = {
    "English": {
        "code": "en",
        "title": "🌾 CropSense AI",
        "subtitle": "Multi-Agent Farming Intelligence",
        "name_label": "Your Name",
        "village_label": "Village / Location",
        "crop_label": "Crop Type",
        "chat_placeholder": "Ask about your crops, diseases, weather, market prices…",
        "send_btn": "Send",
        "clear_btn": "Clear",
        "photo_tab": "📷 Camera",
        "upload_tab": "📁 Upload Image",
        "analyze_btn": "🔍 Analyze with Vision Agent",
        "profile_header": "Farmer Profile",
        "chat_header": "AI Farming Assistant",
        "save_btn": "💾 Save Profile",
        "welcome": "Hello {name}! I'm CropSense AI with 4 specialist agents — Vision, Weather, Soil & Market. Ask me anything about your {crop} crop.",
        "crops": ["Rice","Wheat","Cotton","Sugarcane","Maize","Tomato","Potato","Onion","Soybean","Groundnut","Other"],
        "image_prompt": "Upload a crop photo for AI disease analysis",
        "analyzing": "👁️ Vision Agent analyzing your crop...",
    },
    "తెలుగు (Telugu)": {
        "code": "te",
        "title": "🌾 క్రాప్‌సెన్స్ AI",
        "subtitle": "మల్టీ-ఏజెంట్ వ్యవసాయ సహాయకుడు",
        "name_label": "మీ పేరు",
        "village_label": "గ్రామం / స్థానం",
        "crop_label": "పంట రకం",
        "chat_placeholder": "పంటలు, వ్యాధులు, వాతావరణం గురించి అడగండి…",
        "send_btn": "పంపు",
        "clear_btn": "తొలగించు",
        "photo_tab": "📷 కెమెరా",
        "upload_tab": "📁 అప్‌లోడ్",
        "analyze_btn": "🔍 విజన్ ఏజెంట్ విశ్లేషణ",
        "profile_header": "రైతు వివరాలు",
        "chat_header": "AI వ్యవసాయ సహాయకుడు",
        "save_btn": "💾 ప్రొఫైల్ సేవ్ చేయి",
        "welcome": "నమస్కారం {name}! నేను CropSense AI. విజన్, వాతావరణం, నేల, మార్కెట్ ఏజెంట్లు సిద్ధంగా ఉన్నాయి. మీ {crop} పంట గురించి అడగండి.",
        "crops": ["వరి","గోధుమ","పత్తి","చెరకు","మొక్కజొన్న","టమాట","బంగాళాదుంప","ఉల్లిపాయ","సోయాబీన్","వేరుశనగ","ఇతర"],
        "image_prompt": "AI వ్యాధి విశ్లేషణ కోసం పంట ఫోటో అప్‌లోడ్ చేయండి",
        "analyzing": "👁️ విజన్ ఏజెంట్ విశ్లేషిస్తోంది...",
    },
    "हिंदी (Hindi)": {
        "code": "hi",
        "title": "🌾 CropSense AI",
        "subtitle": "मल्टी-एजेंट कृषि सहायक",
        "name_label": "आपका नाम",
        "village_label": "गाँव / स्थान",
        "crop_label": "फसल प्रकार",
        "chat_placeholder": "फसलों, बीमारियों, मौसम के बारे में पूछें…",
        "send_btn": "भेजें",
        "clear_btn": "साफ़ करें",
        "photo_tab": "📷 कैमरा",
        "upload_tab": "📁 अपलोड",
        "analyze_btn": "🔍 विज़न एजेंट विश्लेषण",
        "profile_header": "किसान प्रोफ़ाइल",
        "chat_header": "AI कृषि सहायक",
        "save_btn": "💾 प्रोफ़ाइल सहेजें",
        "welcome": "नमस्ते {name}! मैं CropSense AI हूँ। विज़न, मौसम, मिट्टी और बाज़ार एजेंट तैयार हैं। अपनी {crop} फसल के बारे में पूछें।",
        "crops": ["चावल","गेहूँ","कपास","गन्ना","मक्का","टमाटर","आलू","प्याज़","सोयाबीन","मूंगफली","अन्य"],
        "image_prompt": "AI रोग विश्लेषण के लिए फसल की फोटो अपलोड करें",
        "analyzing": "👁️ विज़न एजेंट विश्लेषण कर रहा है...",
    },
    "한국어 (Korean)": {
        "code": "ko",
        "title": "🌾 CropSense AI",
        "subtitle": "멀티 에이전트 농업 지원",
        "name_label": "이름",
        "village_label": "마을 / 위치",
        "crop_label": "작물 종류",
        "chat_placeholder": "작물, 질병, 날씨에 대해 물어보세요…",
        "send_btn": "전송",
        "clear_btn": "초기화",
        "photo_tab": "📷 카메라",
        "upload_tab": "📁 업로드",
        "analyze_btn": "🔍 비전 에이전트 분석",
        "profile_header": "농부 프로필",
        "chat_header": "AI 농업 도우미",
        "save_btn": "💾 프로필 저장",
        "welcome": "안녕하세요 {name}! CropSense AI입니다. {crop} 작물에 대해 질문하세요.",
        "crops": ["쌀","밀","면화","사탕수수","옥수수","토마토","감자","양파","대두","땅콩","기타"],
        "image_prompt": "AI 질병 분석을 위해 작물 사진을 업로드하세요",
        "analyzing": "👁️ 비전 에이전트 분석 중...",
    },
    "中文 (Chinese)": {
        "code": "zh",
        "title": "🌾 CropSense AI",
        "subtitle": "多智能体农业助手",
        "name_label": "您的姓名",
        "village_label": "村庄 / 位置",
        "crop_label": "作物类型",
        "chat_placeholder": "询问作物、病害、天气、市场…",
        "send_btn": "发送",
        "clear_btn": "清除",
        "photo_tab": "📷 拍照",
        "upload_tab": "📁 上传",
        "analyze_btn": "🔍 视觉智能体分析",
        "profile_header": "农民信息",
        "chat_header": "AI 农业助手",
        "save_btn": "💾 保存资料",
        "welcome": "您好 {name}！我是 CropSense AI。请询问关于 {crop} 作物的问题。",
        "crops": ["水稻","小麦","棉花","甘蔗","玉米","番茄","土豆","洋葱","大豆","花生","其他"],
        "image_prompt": "上传作物照片进行AI病害分析",
        "analyzing": "👁️ 视觉智能体正在分析...",
    },
}

# ─────────────────────────────────────────────
#  GROQ API  (free — ultra fast llama3)
# ─────────────────────────────────────────────
GROQ_URL          = "https://api.groq.com/openai/v1/chat/completions"
GROQ_CHAT_MODEL   = "llama-3.3-70b-versatile"
GROQ_VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

def get_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return os.environ.get("GROQ_API_KEY", "")

def call_groq(messages, system_prompt="", image_bytes=None):
    api_key = get_api_key()
    if not api_key:
        return "⚠️ No API key. Add GROQ_API_KEY to Streamlit secrets."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    api_messages = []
    if system_prompt:
        api_messages.append({"role": "system", "content": system_prompt})

    if image_bytes is not None:
        # Vision call with image
        img_b64 = base64.b64encode(image_bytes).decode("utf-8")
        api_messages.append({
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
                {"type": "text", "text": system_prompt}
            ]
        })
        model = GROQ_VISION_MODEL
    else:
        for m in messages:
            api_messages.append({"role": m["role"], "content": m["content"]})
        model = GROQ_CHAT_MODEL

    payload = {
        "model": model,
        "messages": api_messages,
        "max_tokens": 1024,
        "temperature": 0.2,
    }

    for attempt in range(3):
        try:
            r = requests.post(GROQ_URL, headers=headers, json=payload, timeout=60)
            if r.status_code == 401:
                return "⚠️ Invalid API key. Check GROQ_API_KEY in Streamlit secrets."
            if r.status_code == 429:
                time.sleep(5 + attempt * 5)
                continue
            if r.status_code == 400:
                err = r.json().get("error", {}).get("message", r.text[:200])
                return f"⚠️ Bad request: {err}"
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"⚠️ API error: {e}"
    return "⚠️ Rate limit hit. Please wait 30 seconds and try again."

# ─────────────────────────────────────────────
#  MOCK AGENTS
# ─────────────────────────────────────────────
def weather_agent(crop, village):
    temps  = [random.randint(28, 38) for _ in range(7)]
    rain   = [random.choice([0,0,0,2,5,10,15,20]) for _ in range(7)]
    days   = [(datetime.now() + timedelta(days=i)).strftime("%a") for i in range(7)]
    rain_days = [days[i] for i, r in enumerate(rain) if r > 0]
    avg_temp  = sum(temps) // 7
    advice = []
    if any(r > 10 for r in rain):
        advice.append("Heavy rain expected — delay fertilizer to avoid washout.")
    if avg_temp > 34:
        advice.append("Heat stress alert — irrigate in early morning or evening.")
    if not rain_days:
        advice.append("No rain forecast — irrigate every 2 days.")
    else:
        advice.append(f"Rain on: {', '.join(rain_days)} — reduce irrigation those days.")
    forecast_str = " | ".join([f"{days[i]}: {temps[i]}°C {'🌧' if rain[i]>0 else '☀'}" for i in range(7)])
    return {"forecast": forecast_str, "advice": advice, "rain_days": rain_days, "avg_temp": avg_temp}

def soil_agent(crop):
    n, p, k = random.randint(30,90), random.randint(20,70), random.randint(40,100)
    moisture, ph = random.randint(25,75), round(random.uniform(5.5, 7.5), 1)
    advice = []
    advice.append(f"{'Low Nitrogen — Apply Urea 50kg/acre' if n<50 else 'Nitrogen OK, no top-dress needed'}.")
    if p < 40: advice.append(f"Low Phosphorus ({p} kg/ha) — Apply DAP 25 kg/acre.")
    if moisture < 40: advice.append(f"Soil dry ({moisture}%) — Irrigate 3-4 cm water immediately.")
    elif moisture > 65: advice.append(f"Waterlogged ({moisture}%) — Stop irrigation, improve drainage.")
    if ph < 6.0: advice.append(f"Acidic soil (pH {ph}) — Apply lime 100 kg/acre.")
    elif ph > 7.2: advice.append(f"Alkaline soil (pH {ph}) — Apply gypsum or sulphur.")
    return {"n": n, "p": p, "k": k, "moisture": moisture, "ph": ph, "advice": advice}

def market_agent(crop):
    prices = {
        "Rice":(1800,2200),"Wheat":(2000,2400),"Cotton":(5500,6500),
        "Sugarcane":(280,350),"Maize":(1500,1900),"Tomato":(800,2500),
        "Potato":(900,1400),"Onion":(1200,3000),"Soybean":(3800,4500),
        "Groundnut":(4500,5500),
    }
    lo, hi = prices.get(crop, (1500,2500))
    current = random.randint(lo, hi)
    msp     = lo + (hi-lo)//3
    trend   = random.choice(["rising","stable","falling"])
    advice  = []
    if trend == "rising":
        advice.append(f"Prices rising — hold 7-10 more days for better returns.")
        advice.append(f"Expected next week: ₹{current+random.randint(50,150)}/quintal")
    elif trend == "falling":
        advice.append(f"Prices falling — sell within 2-3 days to avoid losses.")
        advice.append(f"Current ₹{current}/q is above MSP ₹{msp}/q — safe to sell.")
    else:
        advice.append(f"Prices stable — sell at ₹{current}/quintal.")
        advice.append(f"Best nearby mandi: {random.choice(['Nalgonda','Warangal','Guntur','Karimnagar'])} APMC.")
    return {"price": current, "msp": msp, "trend": trend, "advice": advice}

# ─────────────────────────────────────────────
#  AI AGENTS using Claude
# ─────────────────────────────────────────────
def vision_agent_ai(image_bytes, farmer_name, village, crop, lang_code):
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img.thumbnail((800, 800), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=82)
        resized = buf.getvalue()
    except Exception:
        resized = image_bytes

    prompt = f"""You are the CropSense Vision Agent — expert crop disease diagnostician.
Farmer: {farmer_name}, Village: {village}, Crop: {crop}. Respond in language: {lang_code}.

Analyze this crop image and write a complete structured report:

**1. CROP IDENTIFICATION** — Crop name and growth stage.
**2. DISEASE / PEST / DEFICIENCY** — Name the exact disease (e.g. Rice Blast, Brown Spot, Bacterial Blight, Early Blight, Leaf Rust). If healthy, say so.
**3. SEVERITY** — Mild / Moderate / Severe. Estimated % affected.
**4. ROOT CAUSE** — Fungus / Bacteria / Virus / Pest / Nutrient deficiency. Conditions that caused it.
**5. IMMEDIATE TREATMENT** — Specific chemical/organic treatment with dosage and steps.
**6. PREVENTION** — 3 practical tips for next season.

Be specific. Use simple language a farmer can understand."""

    return call_groq([], system_prompt=prompt, image_bytes=resized)

def orchestrator_ai(vision, weather, soil, market, name, crop, lang_code):
    prompt = f"""You are the CropSense Orchestrator — the Master Brain combining reports from 4 specialist agents.
Respond in language code: {lang_code}. Be practical and use simple farmer-friendly language.

VISION AGENT: {vision or 'No image analyzed yet.'}
WEATHER AGENT: Forecast: {weather['forecast']} | Advice: {'; '.join(weather['advice'])}
SOIL AGENT: N={soil['n']} P={soil['p']} K={soil['k']} Moisture={soil['moisture']}% pH={soil['ph']} | {'; '.join(soil['advice'])}
MARKET AGENT: Price ₹{market['price']}/q | MSP ₹{market['msp']}/q | Trend: {market['trend']} | {'; '.join(market['advice'])}

Write a COMBINED FARM ADVISORY for farmer {name} growing {crop}:

🧠 **ORCHESTRATOR SUMMARY — {name}**

🔴 **URGENT ACTIONS (do today):**
[list the most urgent items across all agents]

📋 **THIS WEEK'S PLAN:**
[day-by-day combined plan from all agents]

💰 **MARKET ADVICE:**
[when to sell, expected price, nearest mandi]

✅ **OVERALL FARM HEALTH:** [Good / Moderate / Needs Attention] — one sentence reason."""

    return call_groq([{"role":"user","content":prompt}])

def chat_agent_ai(messages, name, village, crop, lang_code, weather, soil, market):
    system = f"""You are CropSense AI, a multi-agent farming assistant for {name} from {village}, growing {crop}.
You have live sensor data:
- Weather: avg {weather['avg_temp']}°C, rain expected on: {weather['rain_days'] or 'none this week'}
- Soil: N={soil['n']} P={soil['p']} K={soil['k']} Moisture={soil['moisture']}% pH={soil['ph']}
- Market: {crop} price ₹{market['price']}/quintal, trend={market['trend']}
Respond in language: {lang_code}. Be concise, practical. End with 1-2 actionable tips."""
    return call_groq(messages, system_prompt=system)

# ─────────────────────────────────────────────
#  PAGE CONFIG & CSS
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CropSense AI — Multi-Agent Demo",
    page_icon="🌾", layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f0f4f0; }
[data-testid="stSidebar"] { background: #1a3a1e !important; }

/* All sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] li { color: #d4edda !important; }

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #7dce82 !important; font-weight: 700 !important; }

[data-testid="stSidebar"] label {
    color: #b8e6b8 !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

/* Input fields — white bg, black bold text */
[data-testid="stSidebar"] input {
    background-color: #ffffff !important;
    color: #111111 !important;
    border: 2px solid #4caf50 !important;
    border-radius: 8px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    padding: 8px 12px !important;
    caret-color: #000 !important;
}
[data-testid="stSidebar"] input::placeholder {
    color: #999999 !important;
    font-weight: 400 !important;
}
[data-testid="stSidebar"] input:focus {
    border-color: #81c784 !important;
    box-shadow: 0 0 0 3px rgba(76,175,80,0.25) !important;
    outline: none !important;
}

/* Selectbox */
[data-testid="stSidebar"] .stSelectbox > div > div {
    background-color: #ffffff !important;
    border: 2px solid #4caf50 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div * {
    color: #111111 !important;
    font-weight: 600 !important;
}

/* Save button */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #2e7d32, #43a047) !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 3px 8px rgba(46,125,50,0.4) !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #1b5e20, #2e7d32) !important;
    transform: translateY(-1px);
}

/* App header */
.app-header {
    background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 55%, #388e3c 100%);
    color: white; padding: 22px 28px; border-radius: 16px;
    margin-bottom: 24px;
    box-shadow: 0 6px 24px rgba(46,125,50,0.35);
}
.app-header h1 { margin: 0; font-size: 28px; font-weight: 800; }
.app-header .sub { margin: 4px 0 14px 0; font-size: 13px; opacity: 0.85; letter-spacing: 0.5px; }
.agents-row { display: flex; flex-wrap: wrap; gap: 8px; }
.badge {
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.35);
    border-radius: 20px; padding: 5px 14px;
    font-size: 12px; font-weight: 600;
}

/* Agent cards */
.agent-card {
    background: white; border-radius: 12px; padding: 14px 16px;
    border-left: 4px solid #4caf50;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    font-size: 13px; line-height: 1.65; color: #1a3a1e;
}
.agent-card.weather { border-left-color: #1976d2; }
.agent-card.soil    { border-left-color: #795548; }
.agent-card.market  { border-left-color: #f57c00; }
.agent-card.vision  { border-left-color: #7b1fa2; }
.agent-card.brain   { border-left-color: #c62828; background: #fff8f8; }
.agent-title { font-weight: 800; font-size: 14px; margin-bottom: 8px; }

/* Chat */
.chat-user {
    background: #2e7d32; color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 10px 16px; margin: 6px 0 6px 80px;
    font-size: 14px; line-height: 1.5;
}
.chat-bot {
    background: white; color: #1a3a1e;
    border-radius: 18px 18px 18px 4px;
    padding: 12px 16px; margin: 6px 80px 6px 0;
    font-size: 14px; line-height: 1.7;
    border: 1px solid #dce8dc;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.clabel { font-size: 11px; color: #888; margin-bottom: 2px; }
.clabel.r { text-align: right; margin-right: 4px; }
.clabel.l { text-align: left;  margin-left:  4px; }

.section-title {
    font-size: 17px; font-weight: 700; color: #2e7d32;
    margin: 20px 0 12px 0;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
defaults = {
    "messages":[], "farmer_name":"", "village":"", "crop":"Rice",
    "language":"English", "profile_saved":False,
    "last_vision":None, "weather":None, "soil":None, "market":None,
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌾 CropSense AI")
    st.markdown("*Multi-Agent Farming Intelligence*")
    st.markdown("---")

    lang_key = st.selectbox(
        "🌐 Language",
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(st.session_state.language),
    )
    st.session_state.language = lang_key
    L = LANGUAGES[lang_key]

    st.markdown(f"### 👤 {L['profile_header']}")

    name    = st.text_input(L["name_label"],    value=st.session_state.farmer_name, placeholder="e.g. Ramu")
    village = st.text_input(L["village_label"], value=st.session_state.village,     placeholder="e.g. Nalgonda")
    crop    = st.selectbox(L["crop_label"], L["crops"],
                           index=L["crops"].index(st.session_state.crop)
                           if st.session_state.crop in L["crops"] else 0)

    if st.button(L["save_btn"], use_container_width=True):
        st.session_state.farmer_name   = name
        st.session_state.village       = village
        st.session_state.crop          = crop
        st.session_state.profile_saved = True
        st.session_state.weather = weather_agent(crop, village)
        st.session_state.soil    = soil_agent(crop)
        st.session_state.market  = market_agent(crop)
        welcome = L["welcome"].format(name=name or "Farmer", crop=crop)
        st.session_state.messages = [{"role":"assistant","content":welcome}]
        st.rerun()

    if st.session_state.profile_saved:
        st.success(f"✅ {st.session_state.farmer_name} · {st.session_state.village}")

    st.markdown("---")
    st.markdown("**Active Agents:**")
    st.markdown("👁️ Vision Agent — Disease Detection")
    st.markdown("🌤️ Weather Agent — 7-day Forecast")
    st.markdown("🌱 Soil Agent — Nutrient Analysis")
    st.markdown("📈 Market Agent — Price Intelligence")
    st.markdown("🧠 Orchestrator — Master Brain")

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
L              = LANGUAGES[st.session_state.language]
farmer_name    = st.session_state.farmer_name or "Farmer"
farmer_village = st.session_state.village     or "Your Village"
farmer_crop    = st.session_state.crop

# Init agent data
if st.session_state.weather is None: st.session_state.weather = weather_agent(farmer_crop, farmer_village)
if st.session_state.soil    is None: st.session_state.soil    = soil_agent(farmer_crop)
if st.session_state.market  is None: st.session_state.market  = market_agent(farmer_crop)

W = st.session_state.weather
S = st.session_state.soil
M = st.session_state.market

# Header
st.markdown(f"""
<div class="app-header">
  <h1>{L['title']}</h1>
  <div class="sub">{L['subtitle']} &nbsp;·&nbsp; {farmer_name} &nbsp;·&nbsp; {farmer_village}</div>
  <div class="agents-row">
    <span class="badge">👁️ Vision Agent</span>
    <span class="badge">🌤️ Weather Agent</span>
    <span class="badge">🌱 Soil Agent</span>
    <span class="badge">📈 Market Agent</span>
    <span class="badge">🧠 Orchestrator</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Agent Dashboard ──
st.markdown('<div class="section-title">📊 Live Agent Dashboard</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""<div class="agent-card weather">
      <div class="agent-title">🌤️ Weather Agent</div>
      <b>Forecast:</b> {W['forecast'][:90]}…<br><br>
      {'<br>'.join('• ' + a for a in W['advice'])}
    </div>""", unsafe_allow_html=True)

with c2:
    trend_icon = "📈" if M['trend']=="rising" else ("📉" if M['trend']=="falling" else "➡️")
    st.markdown(f"""<div class="agent-card market">
      <div class="agent-title">📈 Market Agent — {farmer_crop}</div>
      <b>Price:</b> ₹{M['price']}/quintal &nbsp; {trend_icon} {M['trend'].title()}<br>
      <b>MSP:</b> ₹{M['msp']}/quintal<br><br>
      {'<br>'.join('• ' + a for a in M['advice'])}
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""<div class="agent-card soil">
      <div class="agent-title">🌱 Soil Agent</div>
      <b>N:</b> {S['n']} &nbsp;<b>P:</b> {S['p']} &nbsp;<b>K:</b> {S['k']} kg/ha<br>
      <b>Moisture:</b> {S['moisture']}% &nbsp; <b>pH:</b> {S['ph']}<br><br>
      {'<br>'.join('• ' + a for a in S['advice'][:2])}
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── Vision Agent ──
st.markdown('<div class="section-title">👁️ Vision Agent — Crop Disease Detection</div>', unsafe_allow_html=True)

tab_upload, tab_photo = st.tabs([L["upload_tab"], L["photo_tab"]])

def run_vision_and_orchestrator(img_bytes, source_label):
    with st.spinner(L["analyzing"]):
        ctx    = f"{farmer_name}, {farmer_village}, {farmer_crop}"
        result = vision_agent_ai(img_bytes, farmer_name, farmer_village, farmer_crop, L["code"])
        st.session_state.last_vision = result

    st.markdown(f'<div class="agent-card vision"><div class="agent-title">👁️ Vision Agent Report</div>{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role":"user",      "content": source_label})
    st.session_state.messages.append({"role":"assistant", "content": f"👁️ **Vision Agent:**\n\n{result}"})

    st.markdown('<div class="section-title">🧠 Orchestrator — Combined Farm Advisory</div>', unsafe_allow_html=True)
    with st.spinner("🧠 Orchestrator combining all agent reports..."):
        summary = orchestrator_ai(result, W, S, M, farmer_name, farmer_crop, L["code"])
    st.markdown(f'<div class="agent-card brain"><div class="agent-title">🧠 Master Brain Advisory</div>{summary.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role":"assistant", "content": f"🧠 **Orchestrator:**\n\n{summary}"})

with tab_upload:
    st.caption(L["image_prompt"])
    uploaded = st.file_uploader("Choose image", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
    if uploaded:
        img_bytes = uploaded.getvalue()
        st.image(img_bytes, caption=uploaded.name, width=380)
        if st.button(L["analyze_btn"], key="btn_upload", use_container_width=True):
            run_vision_and_orchestrator(img_bytes, f"📁 [Uploaded: {uploaded.name}]")

with tab_photo:
    st.caption(L["image_prompt"])
    img_file = st.camera_input("📸", label_visibility="collapsed")
    if img_file:
        if st.button(L["analyze_btn"], key="btn_cam", use_container_width=True):
            run_vision_and_orchestrator(img_file.getvalue(), "📷 [Photo captured]")

# ── Full Advisory button ──
if st.button("🧠 Get Full Farm Advisory (All Agents)", use_container_width=True, type="primary"):
    with st.spinner("🧠 Orchestrator working..."):
        summary = orchestrator_ai(st.session_state.last_vision, W, S, M, farmer_name, farmer_crop, L["code"])
    st.markdown(f'<div class="agent-card brain"><div class="agent-title">🧠 Master Brain Advisory</div>{summary.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role":"assistant","content":f"🧠 **Orchestrator:**\n\n{summary}"})

st.markdown("---")

# ── Chat ──
st.markdown(f'<div class="section-title">💬 {L["chat_header"]}</div>', unsafe_allow_html=True)

chat_box = st.container(height=380)
with chat_box:
    if not st.session_state.messages:
        welcome = L["welcome"].format(name=farmer_name, crop=farmer_crop)
        st.markdown(f'<div class="clabel l">🌾 CropSense AI</div><div class="chat-bot">{welcome}</div>', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="clabel r">👤 {farmer_name}</div><div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            content = msg["content"].replace("\n","<br>")
            st.markdown(f'<div class="clabel l">🌾 CropSense AI</div><div class="chat-bot">{content}</div>', unsafe_allow_html=True)

ci, cs, cc = st.columns([7,1,1])
with ci:
    user_input = st.text_input("msg", placeholder=L["chat_placeholder"], label_visibility="collapsed")
with cs:
    send = st.button(L["send_btn"], use_container_width=True, type="primary")
with cc:
    if st.button("🗑️", use_container_width=True, help=L["clear_btn"]):
        st.session_state.messages = []
        st.rerun()

if send and user_input.strip():
    st.session_state.messages.append({"role":"user","content":user_input.strip()})
    with st.spinner("🌱 Thinking..."):
        reply = chat_agent_ai(st.session_state.messages, farmer_name, farmer_village, farmer_crop, L["code"], W, S, M)
    st.session_state.messages.append({"role":"assistant","content":reply})
    st.rerun()
