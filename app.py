import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 29: O 'Orip", page_icon="🛍️", layout="centered")

# --- CSS 美化 (多元生活色彩) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #E0F7FA 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #00ACC1;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #00838F; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #E0F7FA;
        border-left: 5px solid #4DD0E1;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #B2EBF2; color: #006064; border: 2px solid #00ACC1; padding: 12px;
    }
    .stButton>button:hover { background-color: #80DEEA; border-color: #00838F; }
    .stProgress > div > div > div > div { background-color: #00ACC1; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 29: 14個單字 - User Fix) ---
vocab_data = [
    {"amis": "Mica'edong", "chi": "穿 (衣物)", "icon": "👕", "source": "Row 321"},
    {"amis": "Riko'", "chi": "衣服", "icon": "👗", "source": "Row 321"},
    {"amis": "Mimali", "chi": "打球", "icon": "🏀", "source": "Row 502"},
    {"amis": "Mapolong", "chi": "一起 / 全部", "icon": "👨‍👩‍👧‍👦", "source": "Row 502"},
    {"amis": "Caliw", "chi": "借 (詞根)", "icon": "🤲", "source": "User Fix"}, # 修正
    {"amis": "Misanga'", "chi": "做 / 製造", "icon": "🔨", "source": "Row 787"},
    {"amis": "Hako", "chi": "箱子", "icon": "📦", "source": "Row 787"},
    {"amis": "Malalok", "chi": "勤勞 / 努力", "icon": "🐜", "source": "Row 408"},
    {"amis": "Fafoy", "chi": "豬", "icon": "🐖", "source": "Row 11"},
    {"amis": "Lafang", "chi": "客人", "icon": "🍵", "source": "Row 992"},
    {"amis": "Patiyamay", "chi": "商店 / 市場", "icon": "🏪", "source": "Row 2889"},
    {"amis": "Mihakelong", "chi": "跟隨 / 一起去", "icon": "👣", "source": "Row 2889"},
    {"amis": "'Adingo", "chi": "影子 / 靈魂", "icon": "👻", "source": "Row 4965"},
    {"amis": "Siri", "chi": "山羊", "icon": "🐐", "source": "Row 1290"},
]

# --- 句子庫 (7句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "Mica'edongay kako to riko'.", "chi": "我正在穿衣服。", "icon": "👕", "source": "Row 321 (Adapted)"},
    {"amis": "Mimali kita a mapolong.", "chi": "我們一起打球。", "icon": "🏀", "source": "Row 502"},
    {"amis": "Caliwhan ni Kacaw ko riko' no mako.", "chi": "我的衣服被Kacaw借走。", "icon": "🤲", "source": "Row 959"},
    {"amis": "Misanga' to hako.", "chi": "製作箱子。", "icon": "📦", "source": "Row 787 (Adapted)"},
    {"amis": "Malalok ci ina to romi'ami'ad.", "chi": "媽媽每天都很勤勞。", "icon": "💪", "source": "Row 408"},
    {"amis": "Mihakelong kako ciinaan a talapatiyamay.", "chi": "我跟隨媽媽去商店。", "icon": "🏪", "source": "Row 2889"},
    {"amis": "Ma'araw ako ko 'adingo iso.", "chi": "我看見你的影子。", "icon": "👀", "source": "Row 121"},
]

# --- 3. 隨機題庫 (Synced) ---
raw_quiz_pool = [
    {
        "q": "Mihakelong kako ciinaan a talapatiyamay.",
        "audio": "Mihakelong kako ciinaan a talapatiyamay",
        "options": ["我跟媽媽去商店", "我跟媽媽去學校", "我跟媽媽去山上"],
        "ans": "我跟媽媽去商店",
        "hint": "Patiyamay (商店) (Row 2889)"
    },
    {
        "q": "Mimali kita a mapolong.",
        "audio": "Mimali kita a mapolong",
        "options": ["我們一起打球", "我們一起吃飯", "我們一起唱歌"],
        "ans": "我們一起打球",
        "hint": "Mimali (打球) (Row 502)"
    },
    {
        "q": "單字測驗：Caliw",
        "audio": "Caliw",
        "options": ["借 (詞根)", "買 (詞根)", "賣 (詞根)"],
        "ans": "借 (詞根)",
        "hint": "Row 959: Caliwhan... (被借走)"
    },
    {
        "q": "單字測驗：Misanga'",
        "audio": "Misanga'",
        "options": ["做/製造", "修理", "破壞"],
        "ans": "做/製造",
        "hint": "Row 787: Misanga' to hako (做箱子)"
    },
    {
        "q": "Ma'araw ako ko 'adingo iso.",
        "audio": "Ma'araw ako ko 'adingo iso",
        "options": ["我看見你的影子", "我看見你的靈魂", "我看見你的臉"],
        "ans": "我看見你的影子",
        "hint": "'Adingo (影子) (Row 121)"
    },
    {
        "q": "單字測驗：Malalok",
        "audio": "Malalok",
        "options": ["勤勞", "懶惰", "生氣"],
        "ans": "勤勞",
        "hint": "Row 408: 媽媽每天都很 Malalok"
    },
    {
        "q": "單字測驗：Riko'",
        "audio": "Riko'",
        "options": ["衣服", "褲子", "鞋子"],
        "ans": "衣服",
        "hint": "穿在身上的 Riko'"
    },
    {
        "q": "單字測驗：Fafoy",
        "audio": "Fafoy",
        "options": ["豬", "牛", "羊"],
        "ans": "豬",
        "hint": "Row 11: O fafoy kora"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌
    selected_questions = random.sample(raw_quiz_pool, 3)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #00838F;'>Unit 29: O 'Orip</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>生活點滴 (User Corrected)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (從句子提取)")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Data-Driven)")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #00838F;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 3)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 3**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #B2EBF2; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #00838F;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會生活詞彙了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 3)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()
