import streamlit as st
import requests
import json
import base64
import tempfile
import os
from PIL import Image
import io
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
import random
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
        "upload_tab": "📁 Upload",
        "voice_tab": "🎙️ Voice",
        "analyze_btn": "🔍 Analyze with Vision Agent",
        "profile_header": "Farmer Profile",
        "chat_header": "AI Farming Assistant",
        "save_btn": "💾 Save Profile",
        "welcome": "Hello {name}! I'm your CropSense AI assistant. I have 4 specialist agents ready — Vision, Weather, Soil, and Market. Ask me anything about your {crop} crop.",
        "crops": ["Rice","Wheat","Cotton","Sugarcane","Maize","Tomato","Potato","Onion","Soybean","Groundnut","Other"],
        "voice_prompt": "Click the mic and speak your question",
        "voice_result": "Recognized: ",
        "image_prompt": "Upload or capture a crop photo for AI disease analysis",
        "analyzing": "Vision Agent analyzing your crop...",
    },
    "తెలుగు (Telugu)": {
        "code": "te",
        "title": "🌾 క్రాప్‌సెన్స్ AI",
        "subtitle": "మల్టీ-ఏజెంట్ వ్యవసాయ సహాయకుడు",
        "name_label": "మీ పేరు",
        "village_label": "గ్రామం / స్థానం",
        "crop_label": "పంట రకం",
        "chat_placeholder": "పంటలు, వ్యాధులు, వాతావరణం, ధరల గురించి అడగండి…",
        "send_btn": "పంపు",
        "clear_btn": "తొలగించు",
        "photo_tab": "📷 కెమెరా",
        "upload_tab": "📁 అప్‌లోడ్",
        "voice_tab": "🎙️ వాయిస్",
        "analyze_btn": "🔍 విజన్ ఏజెంట్‌తో విశ్లేషించండి",
        "profile_header": "రైతు వివరాలు",
        "chat_header": "AI వ్యవసాయ సహాయకుడు",
        "save_btn": "💾 ప్రొఫైల్ సేవ్ చేయి",
        "welcome": "నమస్కారం {name}! నేను మీ CropSense AI సహాయకుడిని. విజన్, వాతావరణం, నేల, మార్కెట్ ఏజెంట్లు సిద్ధంగా ఉన్నాయి. మీ {crop} పంట గురించి అడగండి.",
        "crops": ["వరి","గోధుమ","పత్తి","చెరకు","మొక్కజొన్న","టమాట","బంగాళాదుంప","ఉల్లిపాయ","సోయాబీన్","వేరుశనగ","ఇతర"],
        "voice_prompt": "మైక్ బటన్ నొక్కి మీ ప్రశ్న చెప్పండి",
        "voice_result": "గుర్తించబడింది: ",
        "image_prompt": "AI వ్యాధి విశ్లేషణ కోసం పంట ఫోటో తీయండి",
        "analyzing": "విజన్ ఏజెంట్ పంటను విశ్లేషిస్తోంది...",
    },
    "हिंदी (Hindi)": {
        "code": "hi",
        "title": "🌾 CropSense AI",
        "subtitle": "मल्टी-एजेंट कृषि सहायक",
        "name_label": "आपका नाम",
        "village_label": "गाँव / स्थान",
        "crop_label": "फसल प्रकार",
        "chat_placeholder": "फसलों, बीमारियों, मौसम, बाज़ार के बारे में पूछें…",
        "send_btn": "भेजें",
        "clear_btn": "साफ़ करें",
        "photo_tab": "📷 कैमरा",
        "upload_tab": "📁 अपलोड",
        "voice_tab": "🎙️ आवाज़",
        "analyze_btn": "🔍 विज़न एजेंट से विश्लेषण",
        "profile_header": "किसान प्रोफ़ाइल",
        "chat_header": "AI कृषि सहायक",
        "save_btn": "💾 प्रोफ़ाइल सहेजें",
        "welcome": "नमस्ते {name}! मैं आपका CropSense AI हूँ। विज़न, मौसम, मिट्टी और बाज़ार एजेंट तैयार हैं। अपनी {crop} फसल के बारे में पूछें।",
        "crops": ["चावल","गेहूँ","कपास","गन्ना","मक्का","टमाटर","आलू","प्याज़","सोयाबीन","मूंगफली","अन्य"],
        "voice_prompt": "माइक दबाएं और बोलें",
        "voice_result": "पहचाना गया: ",
        "image_prompt": "AI रोग विश्लेषण के लिए फसल की फोटो लें",
        "analyzing": "विज़न एजेंट विश्लेषण कर रहा है...",
    },
    "한국어 (Korean)": {
        "code": "ko",
        "title": "🌾 CropSense AI",
        "subtitle": "멀티 에이전트 농업 지원",
        "name_label": "이름",
        "village_label": "마을 / 위치",
        "crop_label": "작물 종류",
        "chat_placeholder": "작물, 질병, 날씨, 시장 가격에 대해 물어보세요…",
        "send_btn": "전송",
        "clear_btn": "초기화",
        "photo_tab": "📷 카메라",
        "upload_tab": "📁 업로드",
        "voice_tab": "🎙️ 음성",
        "analyze_btn": "🔍 비전 에이전트로 분석",
        "profile_header": "농부 프로필",
        "chat_header": "AI 농업 도우미",
        "save_btn": "💾 프로필 저장",
        "welcome": "안녕하세요 {name}! CropSense AI입니다. 비전, 날씨, 토양, 시장 에이전트가 준비됐습니다. {crop} 작물에 대해 질문하세요.",
        "crops": ["쌀","밀","면화","사탕수수","옥수수","토마토","감자","양파","대두","땅콩","기타"],
        "voice_prompt": "마이크 버튼을 누르고 말하세요",
        "voice_result": "인식됨: ",
        "image_prompt": "AI 질병 분석을 위해 작물 사진을 찍으세요",
        "analyzing": "비전 에이전트 분석 중...",
    },
    "中文 (Chinese)": {
        "code": "zh",
        "title": "🌾 CropSense AI",
        "subtitle": "多智能体农业助手",
        "name_label": "您的姓名",
        "village_label": "村庄 / 位置",
        "crop_label": "作物类型",
        "chat_placeholder": "询问作物、病害、天气、市场价格…",
        "send_btn": "发送",
        "clear_btn": "清除",
        "photo_tab": "📷 拍照",
        "upload_tab": "📁 上传",
        "voice_tab": "🎙️ 语音",
        "analyze_btn": "🔍 视觉智能体分析",
        "profile_header": "农民信息",
        "chat_header": "AI 农业助手",
        "save_btn": "💾 保存资料",
        "welcome": "您好 {name}！我是 CropSense AI。视觉、天气、土壤和市场智能体已就绪。请询问关于 {crop} 作物的问题。",
        "crops": ["水稻","小麦","棉花","甘蔗","玉米","番茄","土豆","洋葱","大豆","花生","其他"],
        "voice_prompt": "点击麦克风并说出问题",
        "voice_result": "已识别：",
        "image_prompt": "拍摄或上传作物照片进行AI病害分析",
        "analyzing": "视觉智能体正在分析...",
    },
}

# ─────────────────────────────────────────────
#  OLLAMA
# ─────────────────────────────────────────────
OLLAMA_URL      = "http://localhost:11434/api/generate"
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
DEFAULT_CHAT    = "llama3.2"
DEFAULT_VISION  = "llava:7b"

def get_installed_models():
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        if r.status_code == 200:
            return [m["name"] for m in r.json().get("models", [])], True
    except Exception:
        pass
    return [], False

def best_chat_model(models):
    return next((m for m in models if any(x in m for x in ["llama3","mistral","gemma","phi"])), DEFAULT_CHAT)

def best_vision_model(models):
    return next((m for m in models if any(x in m for x in ["llava","moondream","bakllava"])), DEFAULT_VISION)

# ─────────────────────────────────────────────
#  MOCK AGENTS (Weather / Soil / Market)
# ─────────────────────────────────────────────
def weather_agent(crop, village):
    temps  = [random.randint(28,38) for _ in range(7)]
    rain   = [random.choice([0,0,0,2,5,10,15,20]) for _ in range(7)]
    days   = [(datetime.now()+timedelta(days=i)).strftime("%a") for i in range(7)]
    rain_days = [days[i] for i,r in enumerate(rain) if r > 0]
    avg_temp  = sum(temps)//7
    advice = []
    if any(r > 10 for r in rain):
        advice.append("Heavy rain expected — delay fertilizer application to avoid washout.")
    if avg_temp > 34:
        advice.append("High heat stress alert — irrigate in early morning or evening.")
    if not rain_days:
        advice.append("No rain in forecast — irrigate every 2 days.")
    else:
        advice.append(f"Rain expected on: {', '.join(rain_days)} — reduce irrigation on those days.")
    forecast_str = " | ".join([f"{days[i]}: {temps[i]}°C {'🌧️' if rain[i]>0 else '☀️'}" for i in range(7)])
    return {
        "agent": "🌤️ Weather Agent",
        "forecast": forecast_str,
        "advice": advice,
        "rain_days": rain_days,
        "avg_temp": avg_temp,
    }

def soil_agent(crop):
    nitrogen   = random.randint(30, 90)
    phosphorus = random.randint(20, 70)
    potassium  = random.randint(40, 100)
    moisture   = random.randint(25, 75)
    ph         = round(random.uniform(5.5, 7.5), 1)
    advice = []
    if nitrogen < 50:
        advice.append(f"Low Nitrogen ({nitrogen} kg/ha) — Apply Urea 50 kg/acre within 3 days.")
    else:
        advice.append(f"Nitrogen OK ({nitrogen} kg/ha) — No top-dress needed this week.")
    if phosphorus < 40:
        advice.append(f"Low Phosphorus ({phosphorus} kg/ha) — Apply DAP 25 kg/acre.")
    if moisture < 40:
        advice.append(f"Soil moisture low ({moisture}%) — Irrigate immediately, 3-4 cm water.")
    elif moisture > 65:
        advice.append(f"Soil waterlogged ({moisture}%) — Stop irrigation, ensure drainage.")
    if ph < 6.0:
        advice.append(f"Soil too acidic (pH {ph}) — Apply lime 100 kg/acre.")
    elif ph > 7.2:
        advice.append(f"Soil alkaline (pH {ph}) — Apply gypsum or sulphur.")
    return {
        "agent": "🌱 Soil Agent",
        "nitrogen": nitrogen, "phosphorus": phosphorus,
        "potassium": potassium, "moisture": moisture, "ph": ph,
        "advice": advice,
    }

def market_agent(crop):
    prices = {
        "Rice": (1800, 2200), "Wheat": (2000, 2400), "Cotton": (5500, 6500),
        "Sugarcane": (280, 350), "Maize": (1500, 1900), "Tomato": (800, 2500),
        "Potato": (900, 1400), "Onion": (1200, 3000), "Soybean": (3800, 4500),
        "Groundnut": (4500, 5500),
    }
    lo, hi = prices.get(crop, (1500, 2500))
    current = random.randint(lo, hi)
    msp     = lo + (hi - lo) // 3
    trend   = random.choice(["rising","stable","falling"])
    advice  = []
    if trend == "rising":
        advice.append(f"Prices rising — hold stock for 7-10 more days for better returns.")
        advice.append(f"Predicted price next week: ₹{current + random.randint(50,150)}/quintal")
    elif trend == "falling":
        advice.append(f"Prices falling — sell within 2-3 days to avoid losses.")
        advice.append(f"Current price ₹{current}/q is above MSP ₹{msp}/q — safe to sell now.")
    else:
        advice.append(f"Prices stable — sell at current rate ₹{current}/quintal.")
        advice.append(f"Best nearby mandis: {random.choice(['Nalgonda','Warangal','Guntur','Karimnagar'])} APMC.")
    return {
        "agent": "📈 Market Agent",
        "current_price": current,
        "msp": msp,
        "trend": trend,
        "advice": advice,
        "crop": crop,
    }

# ─────────────────────────────────────────────
#  ORCHESTRATOR — combines all 4 agents
# ─────────────────────────────────────────────
def orchestrator_summary(vision_result, weather, soil, market, name, crop, lang_code, chat_model):
    prompt = f"""You are the CropSense AI Orchestrator. You received reports from 4 specialist agents for farmer {name} growing {crop}.

=== VISION AGENT REPORT ===
{vision_result if vision_result else "No image analyzed yet."}

=== WEATHER AGENT REPORT ===
7-day forecast: {weather['forecast']}
Advice: {'; '.join(weather['advice'])}

=== SOIL AGENT REPORT ===
N:{soil['nitrogen']} kg/ha | P:{soil['phosphorus']} kg/ha | K:{soil['potassium']} kg/ha
Moisture:{soil['moisture']}% | pH:{soil['ph']}
Advice: {'; '.join(soil['advice'])}

=== MARKET AGENT REPORT ===
Current price: ₹{market['current_price']}/quintal | MSP: ₹{market['msp']}/quintal | Trend: {market['trend']}
Advice: {'; '.join(market['advice'])}

Now write a COMBINED FARM ADVISORY in language code: {lang_code}.
Format as:
🧠 **ORCHESTRATOR SUMMARY for {name}**

🔴 URGENT ACTIONS (do today):
- [list urgent items from all agents]

📋 THIS WEEK'S PLAN:
- [combined day-by-day plan]

💰 MARKET ADVICE:
- [when to sell, expected price]

✅ OVERALL FARM HEALTH: [Good/Moderate/Needs Attention] — [one sentence reason]

Keep it simple, practical, and easy for a farmer to understand."""

    payload = {
        "model": chat_model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }
    try:
        response = requests.post(OLLAMA_CHAT_URL, json=payload, stream=True, timeout=90)
        response.raise_for_status()
        full = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if "message" in data:
                    full += data["message"].get("content", "")
                if data.get("done"):
                    break
        return full or "Orchestrator could not generate summary."
    except Exception as e:
        return f"⚠️ Orchestrator error: {e}"

# ─────────────────────────────────────────────
#  CHAT AGENT
# ─────────────────────────────────────────────
def get_system_prompt(name, village, crop, lang_code, weather, soil, market):
    return f"""You are CropSense AI, a multi-agent farming assistant for {name} from {village}, growing {crop}.
You have live data from 4 agents:
- Weather: avg {weather['avg_temp']}°C, rain on {weather['rain_days'] or 'no days this week'}
- Soil: N={soil['nitrogen']}, P={soil['phosphorus']}, K={soil['potassium']}, moisture={soil['moisture']}%, pH={soil['ph']}
- Market: {crop} price ₹{market['current_price']}/q, trend={market['trend']}

Always respond in language code: {lang_code}.
Be concise and practical. End with 1-2 actionable tips."""

def chat_with_ollama(messages, system_prompt, model):
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
        "stream": True,
    }
    try:
        r = requests.post(OLLAMA_CHAT_URL, json=payload, stream=True, timeout=60)
        r.raise_for_status()
        full = ""
        for line in r.iter_lines():
            if line:
                data = json.loads(line)
                if "message" in data:
                    full += data["message"].get("content", "")
                if data.get("done"):
                    break
        return full
    except requests.exceptions.ConnectionError:
        return "⚠️ Ollama not running. Run: `ollama serve`"
    except Exception as e:
        return f"⚠️ Error: {e}"

# ─────────────────────────────────────────────
#  VISION AGENT
# ─────────────────────────────────────────────
def resize_image(image_bytes, max_size=640):
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img.thumbnail((max_size, max_size), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=80)
        return buf.getvalue()
    except Exception:
        return image_bytes

def vision_agent(image_bytes, farmer_context, model):
    resized = resize_image(image_bytes)
    img_b64 = base64.b64encode(resized).decode("utf-8")
    prompt = """You are the CropSense Vision Agent — an expert crop disease diagnostician.
Examine this crop image carefully and produce a structured report.

**1. CROP IDENTIFICATION**
Name the crop and growth stage.

**2. DISEASE / PEST / DEFICIENCY DETECTED**
Look for: yellow spots, brown lesions, black spots, white powder, wilting, holes, rot, discoloration.
Name the EXACT disease (e.g. Rice Blast, Brown Spot, Bacterial Leaf Blight, Sheath Blight, Leaf Rust, Early Blight).
If healthy, write "No disease detected" and confirm what looks normal.

**3. SEVERITY**
Rate: Mild / Moderate / Severe. Estimate % of plant affected.

**4. ROOT CAUSE**
Fungus / Bacteria / Virus / Pest / Nutrient deficiency? Explain conditions that caused it.

**5. IMMEDIATE TREATMENT**
Specific chemical or organic treatment with dosage and application steps.

**6. PREVENTION NEXT SEASON**
3 actionable prevention tips.

Farmer context: """ + farmer_context + "\n\nBEGIN VISION REPORT:"

    payload = {
        "model": model,
        "prompt": prompt,
        "images": [img_b64],
        "stream": False,
        "options": {"num_predict": 900, "temperature": 0.1, "num_ctx": 4096},
    }
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=180)
        if r.status_code == 500:
            try: err = r.json().get("error", r.text[:300])
            except: err = r.text[:300]
            return f"⚠️ Vision model error:\n```\n{err}\n```\nTry pulling: `ollama pull llava:7b`"
        if r.status_code == 404:
            return f"⚠️ Model `{model}` not found. Run: `ollama pull {model}`"
        r.raise_for_status()
        result = r.json().get("response", "").strip()
        if len(result) < 50:
            return "⚠️ Vision model returned empty response. Try switching to `llava:latest` or `moondream`."
        return result
    except requests.exceptions.Timeout:
        return f"⚠️ Timeout. Model `{model}` taking too long. Try `moondream` for faster results."
    except Exception as e:
        return f"⚠️ Vision error: {e}"

# ─────────────────────────────────────────────
#  VOICE
# ─────────────────────────────────────────────
LANG_SR = {"en":"en-IN","te":"te-IN","hi":"hi-IN","ko":"ko-KR","zh":"zh-CN"}

def transcribe_audio(audio_bytes, lang_code):
    rec = sr.Recognizer()
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_bytes); fname = f.name
        with sr.AudioFile(fname) as src:
            audio = rec.record(src)
        os.unlink(fname)
        return rec.recognize_google(audio, language=LANG_SR.get(lang_code, "en-IN"))
    except Exception:
        return ""

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
/* ── Global ── */
[data-testid="stAppViewContainer"] { background: #f0f4f0; }
[data-testid="stSidebar"] { background: #1a3a1e !important; }

/* ── Sidebar ALL text ── */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] small { color: #d4edda !important; }

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 { color: #7dce82 !important; font-weight: 700 !important; }

[data-testid="stSidebar"] label {
    color: #a8d5a2 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

/* ── Sidebar text inputs — WHITE bg, BLACK text, clearly visible ── */
[data-testid="stSidebar"] input {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 2px solid #4caf50 !important;
    border-radius: 8px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    padding: 6px 10px !important;
    caret-color: #000000 !important;
}
[data-testid="stSidebar"] input::placeholder {
    color: #777777 !important;
    font-weight: 400 !important;
}
[data-testid="stSidebar"] input:focus {
    border-color: #81c784 !important;
    box-shadow: 0 0 0 2px rgba(76,175,80,0.3) !important;
}

/* ── Sidebar selectbox ── */
[data-testid="stSidebar"] .stSelectbox > div > div {
    background-color: #ffffff !important;
    border: 2px solid #4caf50 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div * {
    color: #000000 !important;
    font-weight: 600 !important;
}

/* ── Save Profile button ── */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #2e7d32, #43a047) !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px !important;
    letter-spacing: 0.3px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #1b5e20, #2e7d32) !important;
    transform: translateY(-1px);
}

/* ── App header ── */
.app-header {
    background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #388e3c 100%);
    color: white; padding: 20px 28px; border-radius: 16px;
    margin-bottom: 22px;
    box-shadow: 0 6px 20px rgba(46,125,50,0.35);
}
.app-header h1 { margin: 0; font-size: 26px; font-weight: 800; }
.app-header .subtitle { margin: 4px 0 10px 0; font-size: 13px; opacity: 0.85; letter-spacing: 0.5px; }
.app-header .agents-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; }
.badge {
    background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.35);
    border-radius: 20px; padding: 4px 12px; font-size: 12px; font-weight: 600;
}

/* ── Agent cards ── */
.agent-card {
    background: white; border-radius: 12px; padding: 14px 16px;
    border-left: 4px solid #4caf50;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07); margin-bottom: 12px;
    font-size: 13px; line-height: 1.6; color: #1a3a1e;
}
.agent-card.weather { border-left-color: #1976d2; }
.agent-card.soil    { border-left-color: #795548; }
.agent-card.market  { border-left-color: #f57c00; }
.agent-card.vision  { border-left-color: #7b1fa2; }
.agent-card.brain   { border-left-color: #c62828; background: #fff8f8; }
.agent-title { font-weight: 800; font-size: 14px; margin-bottom: 6px; }

/* ── Chat bubbles ── */
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
.chat-label { font-size: 11px; color: #888; margin-bottom: 2px; }
.chat-label.right { text-align: right; margin-right: 4px; }
.chat-label.left  { text-align: left;  margin-left: 4px; }

/* ── Divider ── */
.section-title {
    font-size: 16px; font-weight: 700; color: #2e7d32;
    margin: 18px 0 10px 0; display: flex; align-items: center; gap: 8px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
defaults = {
    "messages": [], "farmer_name": "", "village": "", "crop": "Rice",
    "language": "English", "voice_text": "", "profile_saved": False,
    "last_vision": None, "weather_data": None, "soil_data": None, "market_data": None,
}
for k, v in defaults.items():
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
                           index=L["crops"].index(st.session_state.crop) if st.session_state.crop in L["crops"] else 0)

    if st.button(L["save_btn"], use_container_width=True):
        st.session_state.farmer_name   = name
        st.session_state.village       = village
        st.session_state.crop          = crop
        st.session_state.profile_saved = True
        # Regenerate agent data on save
        st.session_state.weather_data  = weather_agent(crop, village)
        st.session_state.soil_data     = soil_agent(crop)
        st.session_state.market_data   = market_agent(crop)
        welcome = L["welcome"].format(name=name or "Farmer", crop=crop)
        st.session_state.messages = [{"role":"assistant","content":welcome}]
        st.rerun()

    if st.session_state.profile_saved:
        st.success(f"✅ {st.session_state.farmer_name} · {st.session_state.village} · {st.session_state.crop}")

    st.markdown("---")

    # Ollama status (no settings exposed)
    installed_models, ollama_online = get_installed_models()
    chat_model   = best_chat_model(installed_models)
    vision_model = best_vision_model(installed_models)

    if ollama_online:
        st.markdown(f"🟢 **AI Engine Online**")
        st.caption(f"{len(installed_models)} model(s) loaded")
    else:
        st.error("🔴 AI Engine Offline")
        st.caption("Run: `ollama serve`")

    st.markdown("---")
    st.markdown("**Agents Active:**")
    st.markdown("🔵 Vision Agent — Disease Detection")
    st.markdown("🟡 Weather Agent — 7-day Forecast")
    st.markdown("🟤 Soil Agent — Nutrient Analysis")
    st.markdown("🟠 Market Agent — Price Intelligence")
    st.markdown("🔴 Orchestrator — Master Brain")

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
L              = LANGUAGES[st.session_state.language]
farmer_name    = st.session_state.farmer_name or "Farmer"
farmer_village = st.session_state.village     or "Your Village"
farmer_crop    = st.session_state.crop

# Ensure agent data exists
if st.session_state.weather_data is None:
    st.session_state.weather_data = weather_agent(farmer_crop, farmer_village)
if st.session_state.soil_data is None:
    st.session_state.soil_data = soil_agent(farmer_crop)
if st.session_state.market_data is None:
    st.session_state.market_data = market_agent(farmer_crop)

W = st.session_state.weather_data
S = st.session_state.soil_data
M = st.session_state.market_data

# ── Header ──
st.markdown(f"""
<div class="app-header">
  <h1>{L['title']}</h1>
  <div class="subtitle">{L['subtitle']} &nbsp;·&nbsp; {farmer_name} &nbsp;·&nbsp; {farmer_village}</div>
  <div class="agents-row">
    <span class="badge">👁️ Vision Agent</span>
    <span class="badge">🌤️ Weather Agent</span>
    <span class="badge">🌱 Soil Agent</span>
    <span class="badge">📈 Market Agent</span>
    <span class="badge">🧠 Orchestrator</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── AGENT DASHBOARD ──
st.markdown('<div class="section-title">📊 Live Agent Dashboard</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="agent-card weather">
      <div class="agent-title">🌤️ Weather Agent</div>
      <b>7-Day:</b> {W['forecast'][:80]}…<br>
      {'<br>'.join(['• ' + a for a in W['advice']])}
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="agent-card soil">
      <div class="agent-title">🌱 Soil Agent</div>
      <b>N:</b>{S['nitrogen']} &nbsp;<b>P:</b>{S['phosphorus']} &nbsp;<b>K:</b>{S['potassium']} kg/ha<br>
      <b>Moisture:</b> {S['moisture']}% &nbsp; <b>pH:</b> {S['ph']}<br>
      {'<br>'.join(['• ' + a for a in S['advice'][:2]])}
    </div>""", unsafe_allow_html=True)

with col3:
    trend_icon = "📈" if M['trend']=="rising" else ("📉" if M['trend']=="falling" else "➡️")
    st.markdown(f"""
    <div class="agent-card market">
      <div class="agent-title">📈 Market Agent — {farmer_crop}</div>
      <b>Price:</b> ₹{M['current_price']}/quintal &nbsp; {trend_icon} {M['trend'].title()}<br>
      <b>MSP:</b> ₹{M['msp']}/quintal<br>
      {'<br>'.join(['• ' + a for a in M['advice']])}
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── VISION AGENT + ORCHESTRATOR ──
st.markdown('<div class="section-title">👁️ Vision Agent — Crop Disease Detection</div>', unsafe_allow_html=True)

tab_upload, tab_photo, tab_voice = st.tabs([L["upload_tab"], L["photo_tab"], L["voice_tab"]])

with tab_upload:
    st.caption(L["image_prompt"])
    uploaded = st.file_uploader("Choose image", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
    if uploaded:
        img_bytes = uploaded.getvalue()
        st.image(img_bytes, caption=uploaded.name, width=380)
        if st.button(L["analyze_btn"], key="analyze_upload", use_container_width=True):
            with st.spinner(L["analyzing"]):
                ctx    = f"Name:{farmer_name}, Village:{farmer_village}, Crop:{farmer_crop}"
                result = vision_agent(img_bytes, ctx, model=vision_model)
                st.session_state.last_vision = result
            st.markdown(f'<div class="agent-card vision"><div class="agent-title">👁️ Vision Agent Report</div>{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role":"user","content":f"📁 [Uploaded: {uploaded.name}]"})
            st.session_state.messages.append({"role":"assistant","content":f"👁️ **Vision Agent Report:**\n\n{result}"})

            # Auto-trigger orchestrator
            st.markdown('<div class="section-title">🧠 Orchestrator — Combined Farm Advisory</div>', unsafe_allow_html=True)
            with st.spinner("🧠 Orchestrator combining all agent reports..."):
                summary = orchestrator_summary(result, W, S, M, farmer_name, farmer_crop, L["code"], chat_model)
            st.markdown(f'<div class="agent-card brain"><div class="agent-title">🧠 Master Brain Advisory</div>{summary.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role":"assistant","content":f"🧠 **Orchestrator Advisory:**\n\n{summary}"})

with tab_photo:
    st.caption(L["image_prompt"])
    img_file = st.camera_input("📸", label_visibility="collapsed")
    if img_file:
        img_bytes = img_file.getvalue()
        if st.button(L["analyze_btn"], key="analyze_cam", use_container_width=True):
            with st.spinner(L["analyzing"]):
                ctx    = f"Name:{farmer_name}, Village:{farmer_village}, Crop:{farmer_crop}"
                result = vision_agent(img_bytes, ctx, model=vision_model)
                st.session_state.last_vision = result
            st.markdown(f'<div class="agent-card vision"><div class="agent-title">👁️ Vision Agent Report</div>{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role":"user","content":"📷 [Photo captured]"})
            st.session_state.messages.append({"role":"assistant","content":f"👁️ **Vision Agent:**\n\n{result}"})

with tab_voice:
    st.caption(L["voice_prompt"])
    audio_bytes = audio_recorder(
        text="", recording_color="#e74c3c", neutral_color="#2e7d32",
        icon_name="microphone", icon_size="2x", pause_threshold=2.0,
    )
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        with st.spinner("Transcribing..."):
            text = transcribe_audio(audio_bytes, L["code"])
        if text:
            st.success(f"{L['voice_result']} **{text}**")
            st.session_state.voice_text = text
        else:
            st.warning("Could not transcribe. Please try again.")

# ── GET FULL ORCHESTRATOR SUMMARY without image ──
if st.button("🧠 Get Full Farm Advisory (All Agents)", use_container_width=True, type="primary"):
    with st.spinner("🧠 Orchestrator working..."):
        summary = orchestrator_summary(
            st.session_state.last_vision, W, S, M,
            farmer_name, farmer_crop, L["code"], chat_model
        )
    st.markdown(f'<div class="agent-card brain"><div class="agent-title">🧠 Master Brain Advisory</div>{summary.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role":"assistant","content":f"🧠 **Orchestrator Advisory:**\n\n{summary}"})

st.markdown("---")

# ── CHAT ──
st.markdown(f'<div class="section-title">💬 {L["chat_header"]}</div>', unsafe_allow_html=True)

chat_container = st.container(height=380)
with chat_container:
    if not st.session_state.messages:
        welcome = L["welcome"].format(name=farmer_name, crop=farmer_crop)
        st.markdown(f'<div class="chat-label left">🌾 CropSense AI</div><div class="chat-bot">{welcome}</div>', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-label right">👤 {farmer_name}</div><div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            content = msg["content"].replace("\n","<br>")
            st.markdown(f'<div class="chat-label left">🌾 CropSense AI</div><div class="chat-bot">{content}</div>', unsafe_allow_html=True)

default_text = st.session_state.voice_text
st.session_state.voice_text = ""

col_in, col_send, col_clear = st.columns([7, 1, 1])
with col_in:
    user_input = st.text_input("msg", value=default_text, placeholder=L["chat_placeholder"], label_visibility="collapsed")
with col_send:
    send = st.button(L["send_btn"], use_container_width=True, type="primary")
with col_clear:
    if st.button("🗑️", use_container_width=True, help=L["clear_btn"]):
        st.session_state.messages = []
        st.rerun()

if send and user_input.strip():
    st.session_state.messages.append({"role":"user","content":user_input.strip()})
    sys_p  = get_system_prompt(farmer_name, farmer_village, farmer_crop, L["code"], W, S, M)
    with st.spinner("🌱 Thinking..."):
        reply = chat_with_ollama(st.session_state.messages, sys_p, model=chat_model)
    st.session_state.messages.append({"role":"assistant","content":reply})
    st.rerun()