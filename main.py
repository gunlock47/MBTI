import streamlit as st
import random
import time

# =========================
# 페이지 설정
# =========================
st.set_page_config(
    page_title="MBTI 포켓몬 추천기",
    page_icon="💙",
    layout="wide"
)

# =========================
# CSS 스타일 + 애니메이션 효과
# =========================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;700;900&display=swap');

    /* 전체 배경 */
    .stApp {
        background: linear-gradient(-45deg, #d8f3ff, #a8ddff, #71c7ff, #4aa3ff, #b7ecff);
        background-size: 400% 400%;
        animation: gradientMove 12s ease infinite;
        font-family: 'Noto Sans KR', sans-serif;
        overflow-x: hidden;
    }

    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 상단 제목 */
    .main-title {
        font-family: 'Jua', sans-serif;
        text-align: center;
        font-size: 64px;
        color: #075a9c;
        text-shadow: 
            3px 3px 0px #ffffff,
            6px 6px 12px rgba(0, 76, 140, 0.25);
        margin-top: 15px;
        animation: bounceIn 1.2s ease;
    }

    .sub-title {
        text-align: center;
        font-size: 22px;
        font-weight: 700;
        color: #0b4f8a;
        margin-bottom: 20px;
        animation: fadeIn 1.8s ease;
    }

    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.08); opacity: 1; }
        70% { transform: scale(0.95); }
        100% { transform: scale(1); }
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* 귀여운 카드 */
    .cute-card {
        background: rgba(255, 255, 255, 0.87);
        border: 4px solid rgba(255, 255, 255, 0.95);
        border-radius: 32px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 
            0 18px 40px rgba(0, 75, 140, 0.22),
            inset 0 0 25px rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        animation: cardPop 0.8s ease;
    }

    @keyframes cardPop {
        0% { transform: scale(0.88) translateY(30px); opacity: 0; }
        100% { transform: scale(1) translateY(0); opacity: 1; }
    }

    .result-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.94), rgba(232,248,255,0.94));
        border: 5px solid white;
        border-radius: 35px;
        padding: 32px;
        box-shadow: 0 20px 45px rgba(0, 70, 140, 0.25);
        animation: resultAppear 0.9s ease;
        position: relative;
        overflow: hidden;
    }

    @keyframes resultAppear {
        0% { opacity: 0; transform: translateY(40px) scale(0.9) rotate(-1deg); }
        100% { opacity: 1; transform: translateY(0) scale(1) rotate(0deg); }
    }

    /* 반짝이 효과 */
    .sparkle {
        position: relative;
    }

    .sparkle::before {
        content: "✨";
        position: absolute;
        top: 12px;
        left: 20px;
        font-size: 28px;
        animation: twinkle 1.5s infinite alternate;
    }

    .sparkle::after {
        content: "💫";
        position: absolute;
        bottom: 18px;
        right: 24px;
        font-size: 32px;
        animation: twinkle 1.2s infinite alternate-reverse;
    }

    @keyframes twinkle {
        0% { opacity: 0.3; transform: scale(0.8) rotate(0deg); }
        100% { opacity: 1; transform: scale(1.2) rotate(18deg); }
    }

    /* 포켓몬 이름 */
    .pokemon-name {
        font-family: 'Jua', sans-serif;
        text-align: center;
        font-size: 48px;
        color: #075a9c;
        text-shadow: 2px 2px 0 #ffffff;
        margin-bottom: 5px;
    }

    .pokemon-type {
        text-align: center;
        font-size: 20px;
        color: #1a6aa8;
        font-weight: 800;
        margin-bottom: 10px;
    }

    /* 태그 */
    .tag-box {
        text-align: center;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .tag {
        display: inline-block;
        background: linear-gradient(135deg, #32a8ff, #0077d9);
        color: white;
        padding: 8px 15px;
        border-radius: 999px;
        margin: 6px;
        font-size: 16px;
        font-weight: 900;
        box-shadow: 0 5px 12px rgba(0, 80, 160, 0.25);
        animation: floatTag 2.2s ease-in-out infinite;
    }

    .tag:nth-child(2) {
        animation-delay: 0.3s;
    }

    .tag:nth-child(3) {
        animation-delay: 0.6s;
    }

    @keyframes floatTag {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }

    /* 설명 박스 */
    .reason-box {
        background: #eaf8ff;
        border-left: 8px solid #249cff;
        padding: 20px;
        border-radius: 20px;
        color: #174b73;
        font-size: 18px;
        line-height: 1.75;
        margin-top: 18px;
        box-shadow: 0 6px 14px rgba(0, 100, 180, 0.12);
    }

    .mini-box {
        background: rgba(255,255,255,0.82);
        border-radius: 22px;
        padding: 18px;
        margin-top: 15px;
        text-align: center;
        color: #075a9c;
        font-size: 18px;
        font-weight: 800;
        box-shadow: 0 8px 18px rgba(0, 75, 140, 0.16);
        border: 2px dashed #76caff;
    }

    /* 버튼 */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #1da1ff, #006bd6);
        color: white;
        border: none;
        border-radius: 24px;
        padding: 16px 22px;
        font-size: 21px;
        font-weight: 900;
        box-shadow: 0 10px 22px rgba(0, 74, 150, 0.32);
        transition: all 0.25s ease;
        animation: pulseButton 1.8s infinite;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #007be8, #004fb8);
        transform: translateY(-3px) scale(1.02);
        color: white;
    }

    @keyframes pulseButton {
        0% { box-shadow: 0 0 0 0 rgba(0, 127, 255, 0.45); }
        70% { box-shadow: 0 0 0 12px rgba(0, 127, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 127, 255, 0); }
    }

    /* 셀렉트박스 라벨 */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextInput"] label {
        color: #075a9c;
        font-size: 19px;
        font-weight: 900;
    }

    /* 이미지 둥둥 효과 */
    .pokemon-img-wrap {
        animation: floatPokemon 2.7s ease-in-out infinite;
        filter: drop-shadow(0 18px 18px rgba(0, 70, 140, 0.22));
    }

    @keyframes floatPokemon {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-14px) rotate(2deg); }
    }

    /* 하단 */
    .footer {
        text-align: center;
        color: #064e89;
        font-size: 14px;
        margin-top: 35px;
        font-weight: 700;
    }

    /* 떠다니는 버블 배경 */
    .bubble {
        position: fixed;
        bottom: -120px;
        width: 40px;
        height: 40px;
        background: rgba(255,255,255,0.35);
        border-radius: 50%;
        animation: rise 12s infinite ease-in;
        z-index: 0;
        pointer-events: none;
    }

    .bubble:nth-child(1) { left: 8%; width: 35px; height: 35px; animation-duration: 10s; }
    .bubble:nth-child(2) { left: 18%; width: 60px; height: 60px; animation-duration: 14s; animation-delay: 2s; }
    .bubble:nth-child(3) { left: 32%; width: 25px; height: 25px; animation-duration: 9s; animation-delay: 1s; }
    .bubble:nth-child(4) { left: 47%; width: 80px; height: 80px; animation-duration: 16s; animation-delay: 3s; }
    .bubble:nth-child(5) { left: 62%; width: 45px; height: 45px; animation-duration: 11s; animation-delay: 2s; }
    .bubble:nth-child(6) { left: 77%; width: 70px; height: 70px; animation-duration: 15s; animation-delay: 4s; }
    .bubble:nth-child(7) { left: 88%; width: 30px; height: 30px; animation-duration: 8s; animation-delay: 1s; }

    @keyframes rise {
        0% { bottom: -120px; transform: translateX(0) scale(1); opacity: 0; }
        20% { opacity: 0.7; }
        50% { transform: translateX(35px) scale(1.1); }
        100% { bottom: 110%; transform: translateX(-25px) scale(0.8); opacity: 0; }
    }

    /* 포켓볼 느낌 장식 */
    .pokeball-line {
        width: 100%;
        height: 8px;
        background: linear-gradient(90deg, #0077d9, #ffffff, #0077d9);
        border-radius: 999px;
        margin: 18px 0;
        animation: lineGlow 2s infinite alternate;
    }

    @keyframes lineGlow {
        from { box-shadow: 0 0 6px rgba(255,255,255,0.4); }
        to { box-shadow: 0 0 18px rgba(255,255,255,0.95); }
    }

    /* Streamlit 기본 메뉴 일부 숨기기 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>

    <div class="bubble"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
    """,
    unsafe_allow_html=True
)

# =========================
# MBTI별 포켓몬 데이터
# =========================
pokemon_data = {
    "INTJ": {
        "name": "뮤츠",
        "emoji": "🧬",
        "id": 150,
        "type": "에스퍼 타입",
        "color": "#9b59b6",
        "tags": ["전략가", "분석력", "독립적"],
        "reason": "INTJ는 깊이 생각하고 계획을 세우는 전략가 타입이에요. 강력한 지능과 독립적인 분위기를 가진 뮤츠와 잘 어울립니다.",
        "study": "큰 목표를 먼저 세우고, 세부 계획을 단계별로 나누면 집중력이 더 좋아져요."
    },
    "INTP": {
        "name": "메타몽",
        "emoji": "🫧",
        "id": 132,
        "type": "노말 타입",
        "color": "#c678dd",
        "tags": ["호기심", "탐구", "창의적"],
        "reason": "INTP는 새로운 아이디어를 탐구하고 다양한 가능성을 실험하는 타입이에요. 무엇이든 변신할 수 있는 메타몽처럼 유연한 사고력이 있어요.",
        "study": "개념을 외우기보다 '왜 그럴까?'를 질문하며 공부하면 오래 기억돼요."
    },
    "ENTJ": {
        "name": "리자몽",
        "emoji": "🔥",
        "id": 6,
        "type": "불꽃 / 비행 타입",
        "color": "#ff7f50",
        "tags": ["리더십", "추진력", "카리스마"],
        "reason": "ENTJ는 목표를 향해 강하게 나아가는 리더형이에요. 뜨거운 에너지와 강한 존재감을 가진 리자몽과 잘 어울립니다.",
        "study": "오늘 끝낼 과제를 정하고 체크리스트로 완료 표시를 해보세요."
    },
    "ENTP": {
        "name": "팬텀",
        "emoji": "👻",
        "id": 94,
        "type": "고스트 / 독 타입",
        "color": "#6c5ce7",
        "tags": ["재치", "장난기", "아이디어"],
        "reason": "ENTP는 말솜씨와 아이디어가 뛰어나고 장난기 있는 타입이에요. 톡톡 튀는 매력의 팬텀과 찰떡궁합입니다.",
        "study": "친구에게 설명하듯 말하면서 공부하면 이해도가 빠르게 올라가요."
    },
    "INFJ": {
        "name": "루기아",
        "emoji": "🌊",
        "id": 249,
        "type": "에스퍼 / 비행 타입",
        "color": "#74b9ff",
        "tags": ["이상주의", "통찰력", "조용한 힘"],
        "reason": "INFJ는 깊은 내면과 따뜻한 이상을 가진 타입이에요. 바다 깊은 곳에서 조용히 힘을 품고 있는 루기아와 잘 어울립니다.",
        "study": "공부한 내용을 나만의 문장으로 정리하면 생각이 훨씬 선명해져요."
    },
    "INFP": {
        "name": "이브이",
        "emoji": "🤎",
        "id": 133,
        "type": "노말 타입",
        "color": "#a0522d",
        "tags": ["감성", "가능성", "순수함"],
        "reason": "INFP는 따뜻한 마음과 무한한 가능성을 가진 타입이에요. 여러 모습으로 진화할 수 있는 이브이처럼 자신만의 길을 찾아갑니다.",
        "study": "좋아하는 색깔 펜이나 예쁜 노트로 정리하면 공부 의욕이 올라갈 수 있어요."
    },
    "ENFJ": {
        "name": "라프라스",
        "emoji": "🎵",
        "id": 131,
        "type": "물 / 얼음 타입",
        "color": "#00a8ff",
        "tags": ["배려", "소통", "따뜻함"],
        "reason": "ENFJ는 사람들을 잘 이끌고 따뜻하게 챙기는 타입이에요. 사람을 태우고 바다를 건너는 다정한 라프라스와 잘 어울려요.",
        "study": "스터디 그룹에서 내용을 설명해보면 실력이 더 단단해져요."
    },
    "ENFP": {
        "name": "피카츄",
        "emoji": "⚡",
        "id": 25,
        "type": "전기 타입",
        "color": "#f1c40f",
        "tags": ["활발함", "긍정", "친화력"],
        "reason": "ENFP는 밝고 에너지가 넘치며 사람들과 금방 친해지는 타입이에요. 귀엽고 활기찬 피카츄와 딱 맞습니다.",
        "study": "짧은 시간 집중하고 보상을 주는 방식이 잘 맞아요. 25분 공부 후 5분 휴식을 추천해요."
    },
    "ISTJ": {
        "name": "거북왕",
        "emoji": "💧",
        "id": 9,
        "type": "물 타입",
        "color": "#0984e3",
        "tags": ["책임감", "성실함", "안정감"],
        "reason": "ISTJ는 책임감이 강하고 꾸준한 타입이에요. 단단한 방어력과 안정적인 힘을 가진 거북왕과 잘 어울립니다.",
        "study": "매일 같은 시간에 공부하는 루틴을 만들면 큰 효과를 볼 수 있어요."
    },
    "ISFJ": {
        "name": "잠만보",
        "emoji": "🍙",
        "id": 143,
        "type": "노말 타입",
        "color": "#2d98da",
        "tags": ["포근함", "배려", "든든함"],
        "reason": "ISFJ는 주변 사람을 조용히 챙기는 따뜻한 타입이에요. 포근하고 든든한 잠만보처럼 편안한 매력이 있습니다.",
        "study": "무리하지 말고 충분한 휴식과 함께 꾸준히 반복하는 공부가 잘 맞아요."
    },
    "ESTJ": {
        "name": "괴력몬",
        "emoji": "💪",
        "id": 68,
        "type": "격투 타입",
        "color": "#45aaf2",
        "tags": ["실행력", "질서", "책임감"],
        "reason": "ESTJ는 현실적이고 실행력이 뛰어난 타입이에요. 강한 힘과 추진력을 가진 괴력몬과 잘 어울립니다.",
        "study": "문제집 페이지 수나 문제 개수처럼 구체적인 목표를 세우면 좋아요."
    },
    "ESFJ": {
        "name": "푸크린",
        "emoji": "🎀",
        "id": 40,
        "type": "노말 / 페어리 타입",
        "color": "#ff79c6",
        "tags": ["사교성", "친절", "분위기 메이커"],
        "reason": "ESFJ는 사람들과 어울리는 것을 좋아하고 분위기를 밝게 만드는 타입이에요. 사랑스러운 푸크린과 잘 맞아요.",
        "study": "친구와 서로 퀴즈를 내며 공부하면 집중력이 올라갈 수 있어요."
    },
    "ISTP": {
        "name": "개굴닌자",
        "emoji": "🥷",
        "id": 658,
        "type": "물 / 악 타입",
        "color": "#0066cc",
        "tags": ["실용적", "침착함", "순발력"],
        "reason": "ISTP는 조용하지만 상황 판단이 빠르고 실전 능력이 뛰어난 타입이에요. 민첩하고 멋진 개굴닌자와 잘 어울립니다.",
        "study": "이론을 본 뒤 바로 문제에 적용해보는 방식이 효과적이에요."
    },
    "ISFP": {
        "name": "님피아",
        "emoji": "🌸",
        "id": 700,
        "type": "페어리 타입",
        "color": "#ff9ff3",
        "tags": ["감성", "예술적", "다정함"],
        "reason": "ISFP는 감각적이고 부드러운 매력을 가진 타입이에요. 사랑스럽고 우아한 님피아와 잘 어울립니다.",
        "study": "필기 색상과 그림, 도식을 활용하면 기억하기 쉬워져요."
    },
    "ESTP": {
        "name": "윈디",
        "emoji": "🐾",
        "id": 59,
        "type": "불꽃 타입",
        "color": "#ff6b35",
        "tags": ["모험심", "활동적", "용감함"],
        "reason": "ESTP는 즉흥적이고 활동적이며 도전을 즐기는 타입이에요. 빠르고 용감한 윈디와 찰떡입니다.",
        "study": "가만히 오래 앉아 있기보다 짧고 강하게 여러 번 공부하는 방식이 잘 맞아요."
    },
    "ESFP": {
        "name": "파치리스",
        "emoji": "✨",
        "id": 417,
        "type": "전기 타입",
        "color": "#5dade2",
        "tags": ["흥", "귀여움", "에너지"],
        "reason": "ESFP는 밝고 즐거운 분위기를 만드는 타입이에요. 통통 튀는 매력의 파치리스와 잘 어울립니다.",
        "study": "공부 목표를 달성할 때마다 작은 보상을 정하면 동기부여가 잘 돼요."
    }
}

lucky_items = [
    "파란색 노트 💙",
    "반짝이는 볼펜 🖊️",
    "귀여운 스티커 ⭐",
    "시원한 물 한 병 🧊",
    "포켓몬볼 키링 🔴",
    "달콤한 간식 🍪",
    "하늘색 후드티 🩵",
    "작은 응원 메모 📝"
]

cheer_messages = [
    "오늘도 너의 모험은 계속된다!",
    "작은 노력도 경험치가 되고 있어!",
    "실패해도 괜찮아. 다시 도전하면 레벨업!",
    "너는 이미 충분히 멋진 트레이너야!",
    "오늘의 집중력이 내일의 진화를 만든다!"
]

# =========================
# 상단 화면
# =========================
st.markdown("<div class='main-title'>💙 MBTI 포켓몬 추천기 💙</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>나의 MBTI를 고르면 찰떡 포켓몬이 등장해요! 🐾✨</div>",
    unsafe_allow_html=True
)
st.markdown("<div class='pokeball-line'></div>", unsafe_allow_html=True)

# =========================
# 입력 영역
# =========================
left, center, right = st.columns([1, 1.4, 1])

with center:
    st.markdown("<div class='cute-card sparkle'>", unsafe_allow_html=True)

    user_name = st.text_input(
        "이름 또는 닉네임을 입력하세요",
        placeholder="예: 피카츄마스터"
    )

    selected_mbti = st.selectbox(
        "나의 MBTI를 선택하세요!",
        list(pokemon_data.keys()),
        index=list(pokemon_data.keys()).index("ENFP")
    )

    st.caption("※ 이 추천은 재미용입니다. 실제 성격을 정확히 판단하는 도구는 아니에요.")

    start = st.button("내 포켓몬 소환하기 💫")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 결과 출력
# =========================
if start:
    data = pokemon_data[selected_mbti]
    display_name = user_name.strip() if user_name.strip() else "당신"

    # 재미있는 로딩 효과
    with st.spinner("포켓몬을 찾는 중... 🔍"):
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.008)
            progress.progress(i + 1)

    st.balloons()

    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{data['id']}.png"

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.8, 1.5, 0.8])

    with col2:
        st.markdown("<div class='result-card sparkle'>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class='pokemon-name'>
                {data['emoji']} {display_name}님의 포켓몬은<br>
                {data['name']}!
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class='pokemon-type'>
                {selected_mbti} · {data['type']}
            </div>
            """,
            unsafe_allow_html=True
        )

        # 이미지에 애니메이션을 주기 위해 HTML img 사용
        st.markdown(
            f"""
            <div class='pokemon-img-wrap' style='text-align:center;'>
                <img src="{image_url}" width="360" style="max-width:90%;">
            </div>
            """,
            unsafe_allow_html=True
        )

        tag_html = "<div class='tag-box'>"
        for tag in data["tags"]:
            tag_html += f"<span class='tag'>#{tag}</span>"
        tag_html += "</div>"
        st.markdown(tag_html, unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class='reason-box'>
                <b>💙 추천 이유</b><br>
                {data['reason']}
            </div>
            """,
            unsafe_allow_html=True
        )

        random.seed(selected_mbti + display_name)
        lucky_item = random.choice(lucky_items)
        cheer = random.choice(cheer_messages)

        st.markdown(
            f"""
            <div class='mini-box'>
                🎁 오늘의 행운 아이템<br>
                <span style="font-size:24px;">{lucky_item}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class='mini-box'>
                📚 포켓몬이 주는 공부 팁<br>
                <span style="font-size:20px;">{data['study']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class='mini-box'>
                🏆 오늘의 응원 메시지<br>
                <span style="font-size:21px;">"{cheer}"</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.4, 1])

    with col2:
        st.markdown(
            """
            <div class='cute-card sparkle'>
                <div style='text-align:center; font-size:28px; color:#075a9c; font-weight:900;'>
                    아직 포켓몬이 숨어 있어요... 🫧
                </div>
                <div style='text-align:center; font-size:19px; color:#17689e; margin-top:10px;'>
                    MBTI를 고르고 버튼을 누르면<br>
                    귀여운 포켓몬이 나타납니다! 🐾✨
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# 전체 추천표
# =========================
st.markdown("<br>", unsafe_allow_html=True)

with st.expander("📘 전체 MBTI별 추천 포켓몬 보기"):
    cols = st.columns(4)
    for idx, (mbti, data) in enumerate(pokemon_data.items()):
        with cols[idx % 4]:
            st.markdown(
                f"""
                <div style="
                    background: rgba(255,255,255,0.78);
                    border-radius: 18px;
                    padding: 14px;
                    margin-bottom: 12px;
                    text-align: center;
                    box-shadow: 0 6px 14px rgba(0,80,150,0.12);
                    border: 2px solid white;
                ">
                    <div style="font-size:26px;">{data['emoji']}</div>
                    <b style="color:#075a9c;">{mbti}</b><br>
                    <span style="color:#17689e;">{data['name']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================
# 하단
# =========================
st.markdown(
    """
    <div class='footer'>
        Made with Streamlit 💙 | Pokemon images from PokeAPI official artwork URLs<br>
        재미용 MBTI 포켓몬 추천 웹앱입니다 🐳✨
    </div>
    """,
    unsafe_allow_html=True
)import streamlit as st
import random
import time

# =========================
# 페이지 설정
# =========================
st.set_page_config(
    page_title="MBTI 포켓몬 추천기",
    page_icon="💙",
    layout="wide"
)

# =========================
# CSS 스타일 + 애니메이션 효과
# =========================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;700;900&display=swap');

    /* 전체 배경 */
    .stApp {
        background: linear-gradient(-45deg, #d8f3ff, #a8ddff, #71c7ff, #4aa3ff, #b7ecff);
        background-size: 400% 400%;
        animation: gradientMove 12s ease infinite;
        font-family: 'Noto Sans KR', sans-serif;
        overflow-x: hidden;
    }

    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 상단 제목 */
    .main-title {
        font-family: 'Jua', sans-serif;
        text-align: center;
        font-size: 64px;
        color: #075a9c;
        text-shadow: 
            3px 3px 0px #ffffff,
            6px 6px 12px rgba(0, 76, 140, 0.25);
        margin-top: 15px;
        animation: bounceIn 1.2s ease;
    }

    .sub-title {
        text-align: center;
        font-size: 22px;
        font-weight: 700;
        color: #0b4f8a;
        margin-bottom: 20px;
        animation: fadeIn 1.8s ease;
    }

    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.08); opacity: 1; }
        70% { transform: scale(0.95); }
        100% { transform: scale(1); }
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* 귀여운 카드 */
    .cute-card {
        background: rgba(255, 255, 255, 0.87);
        border: 4px solid rgba(255, 255, 255, 0.95);
        border-radius: 32px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 
            0 18px 40px rgba(0, 75, 140, 0.22),
            inset 0 0 25px rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        animation: cardPop 0.8s ease;
    }

    @keyframes cardPop {
        0% { transform: scale(0.88) translateY(30px); opacity: 0; }
        100% { transform: scale(1) translateY(0); opacity: 1; }
    }

    .result-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.94), rgba(232,248,255,0.94));
        border: 5px solid white;
        border-radius: 35px;
        padding: 32px;
        box-shadow: 0 20px 45px rgba(0, 70, 140, 0.25);
        animation: resultAppear 0.9s ease;
        position: relative;
        overflow: hidden;
    }

    @keyframes resultAppear {
        0% { opacity: 0; transform: translateY(40px) scale(0.9) rotate(-1deg); }
        100% { opacity: 1; transform: translateY(0) scale(1) rotate(0deg); }
    }

    /* 반짝이 효과 */
    .sparkle {
        position: relative;
    }

    .sparkle::before {
        content: "✨";
        position: absolute;
        top: 12px;
        left: 20px;
        font-size: 28px;
        animation: twinkle 1.5s infinite alternate;
    }

    .sparkle::after {
        content: "💫";
        position: absolute;
        bottom: 18px;
        right: 24px;
        font-size: 32px;
        animation: twinkle 1.2s infinite alternate-reverse;
    }

    @keyframes twinkle {
        0% { opacity: 0.3; transform: scale(0.8) rotate(0deg); }
        100% { opacity: 1; transform: scale(1.2) rotate(18deg); }
    }

    /* 포켓몬 이름 */
    .pokemon-name {
        font-family: 'Jua', sans-serif;
        text-align: center;
        font-size: 48px;
        color: #075a9c;
        text-shadow: 2px 2px 0 #ffffff;
        margin-bottom: 5px;
    }

    .pokemon-type {
        text-align: center;
        font-size: 20px;
        color: #1a6aa8;
        font-weight: 800;
        margin-bottom: 10px;
    }

    /* 태그 */
    .tag-box {
        text-align: center;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .tag {
        display: inline-block;
        background: linear-gradient(135deg, #32a8ff, #0077d9);
        color: white;
        padding: 8px 15px;
        border-radius: 999px;
        margin: 6px;
        font-size: 16px;
        font-weight: 900;
        box-shadow: 0 5px 12px rgba(0, 80, 160, 0.25);
        animation: floatTag 2.2s ease-in-out infinite;
    }

    .tag:nth-child(2) {
        animation-delay: 0.3s;
    }

    .tag:nth-child(3) {
        animation-delay: 0.6s;
    }

    @keyframes floatTag {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }

    /* 설명 박스 */
    .reason-box {
        background: #eaf8ff;
        border-left: 8px solid #249cff;
        padding: 20px;
        border-radius: 20px;
        color: #174b73;
        font-size: 18px;
        line-height: 1.75;
        margin-top: 18px;
        box-shadow: 0 6px 14px rgba(0, 100, 180, 0.12);
    }

    .mini-box {
        background: rgba(255,255,255,0.82);
        border-radius: 22px;
        padding: 18px;
        margin-top: 15px;
        text-align: center;
        color: #075a9c;
        font-size: 18px;
        font-weight: 800;
        box-shadow: 0 8px 18px rgba(0, 75, 140, 0.16);
        border: 2px dashed #76caff;
    }

    /* 버튼 */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #1da1ff, #006bd6);
        color: white;
        border: none;
        border-radius: 24px;
        padding: 16px 22px;
        font-size: 21px;
        font-weight: 900;
        box-shadow: 0 10px 22px rgba(0, 74, 150, 0.32);
        transition: all 0.25s ease;
        animation: pulseButton 1.8s infinite;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #007be8, #004fb8);
        transform: translateY(-3px) scale(1.02);
        color: white;
    }

    @keyframes pulseButton {
        0% { box-shadow: 0 0 0 0 rgba(0, 127, 255, 0.45); }
        70% { box-shadow: 0 0 0 12px rgba(0, 127, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 127, 255, 0); }
    }

    /* 셀렉트박스 라벨 */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextInput"] label {
        color: #075a9c;
        font-size: 19px;
        font-weight: 900;
    }

    /* 이미지 둥둥 효과 */
    .pokemon-img-wrap {
        animation: floatPokemon 2.7s ease-in-out infinite;
        filter: drop-shadow(0 18px 18px rgba(0, 70, 140, 0.22));
    }

    @keyframes floatPokemon {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-14px) rotate(2deg); }
    }

    /* 하단 */
    .footer {
        text-align: center;
        color: #064e89;
        font-size: 14px;
        margin-top: 35px;
        font-weight: 700;
    }

    /* 떠다니는 버블 배경 */
    .bubble {
        position: fixed;
        bottom: -120px;
        width: 40px;
        height: 40px;
        background: rgba(255,255,255,0.35);
        border-radius: 50%;
        animation: rise 12s infinite ease-in;
        z-index: 0;
        pointer-events: none;
    }

    .bubble:nth-child(1) { left: 8%; width: 35px; height: 35px; animation-duration: 10s; }
    .bubble:nth-child(2) { left: 18%; width: 60px; height: 60px; animation-duration: 14s; animation-delay: 2s; }
    .bubble:nth-child(3) { left: 32%; width: 25px; height: 25px; animation-duration: 9s; animation-delay: 1s; }
    .bubble:nth-child(4) { left: 47%; width: 80px; height: 80px; animation-duration: 16s; animation-delay: 3s; }
    .bubble:nth-child(5) { left: 62%; width: 45px; height: 45px; animation-duration: 11s; animation-delay: 2s; }
    .bubble:nth-child(6) { left: 77%; width: 70px; height: 70px; animation-duration: 15s; animation-delay: 4s; }
    .bubble:nth-child(7) { left: 88%; width: 30px; height: 30px; animation-duration: 8s; animation-delay: 1s; }

    @keyframes rise {
        0% { bottom: -120px; transform: translateX(0) scale(1); opacity: 0; }
        20% { opacity: 0.7; }
        50% { transform: translateX(35px) scale(1.1); }
        100% { bottom: 110%; transform: translateX(-25px) scale(0.8); opacity: 0; }
    }

    /* 포켓볼 느낌 장식 */
    .pokeball-line {
        width: 100%;
        height: 8px;
        background: linear-gradient(90deg, #0077d9, #ffffff, #0077d9);
        border-radius: 999px;
        margin: 18px 0;
        animation: lineGlow 2s infinite alternate;
    }

    @keyframes lineGlow {
        from { box-shadow: 0 0 6px rgba(255,255,255,0.4); }
        to { box-shadow: 0 0 18px rgba(255,255,255,0.95); }
    }

    /* Streamlit 기본 메뉴 일부 숨기기 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>

    <div class="bubble"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
    <div class="bubble"></div>
    """,
    unsafe_allow_html=True
)

# =========================
# MBTI별 포켓몬 데이터
# =========================
pokemon_data = {
    "INTJ": {
        "name": "뮤츠",
        "emoji": "🧬",
        "id": 150,
        "type": "에스퍼 타입",
        "color": "#9b59b6",
        "tags": ["전략가", "분석력", "독립적"],
        "reason": "INTJ는 깊이 생각하고 계획을 세우는 전략가 타입이에요. 강력한 지능과 독립적인 분위기를 가진 뮤츠와 잘 어울립니다.",
        "study": "큰 목표를 먼저 세우고, 세부 계획을 단계별로 나누면 집중력이 더 좋아져요."
    },
    "INTP": {
        "name": "메타몽",
        "emoji": "🫧",
        "id": 132,
        "type": "노말 타입",
        "color": "#c678dd",
        "tags": ["호기심", "탐구", "창의적"],
        "reason": "INTP는 새로운 아이디어를 탐구하고 다양한 가능성을 실험하는 타입이에요. 무엇이든 변신할 수 있는 메타몽처럼 유연한 사고력이 있어요.",
        "study": "개념을 외우기보다 '왜 그럴까?'를 질문하며 공부하면 오래 기억돼요."
    },
    "ENTJ": {
        "name": "리자몽",
        "emoji": "🔥",
        "id": 6,
        "type": "불꽃 / 비행 타입",
        "color": "#ff7f50",
        "tags": ["리더십", "추진력", "카리스마"],
        "reason": "ENTJ는 목표를 향해 강하게 나아가는 리더형이에요. 뜨거운 에너지와 강한 존재감을 가진 리자몽과 잘 어울립니다.",
        "study": "오늘 끝낼 과제를 정하고 체크리스트로 완료 표시를 해보세요."
    },
    "ENTP": {
        "name": "팬텀",
        "emoji": "👻",
        "id": 94,
        "type": "고스트 / 독 타입",
        "color": "#6c5ce7",
        "tags": ["재치", "장난기", "아이디어"],
        "reason": "ENTP는 말솜씨와 아이디어가 뛰어나고 장난기 있는 타입이에요. 톡톡 튀는 매력의 팬텀과 찰떡궁합입니다.",
        "study": "친구에게 설명하듯 말하면서 공부하면 이해도가 빠르게 올라가요."
    },
    "INFJ": {
        "name": "루기아",
        "emoji": "🌊",
        "id": 249,
        "type": "에스퍼 / 비행 타입",
        "color": "#74b9ff",
        "tags": ["이상주의", "통찰력", "조용한 힘"],
        "reason": "INFJ는 깊은 내면과 따뜻한 이상을 가진 타입이에요. 바다 깊은 곳에서 조용히 힘을 품고 있는 루기아와 잘 어울립니다.",
        "study": "공부한 내용을 나만의 문장으로 정리하면 생각이 훨씬 선명해져요."
    },
    "INFP": {
        "name": "이브이",
        "emoji": "🤎",
        "id": 133,
        "type": "노말 타입",
        "color": "#a0522d",
        "tags": ["감성", "가능성", "순수함"],
        "reason": "INFP는 따뜻한 마음과 무한한 가능성을 가진 타입이에요. 여러 모습으로 진화할 수 있는 이브이처럼 자신만의 길을 찾아갑니다.",
        "study": "좋아하는 색깔 펜이나 예쁜 노트로 정리하면 공부 의욕이 올라갈 수 있어요."
    },
    "ENFJ": {
        "name": "라프라스",
        "emoji": "🎵",
        "id": 131,
        "type": "물 / 얼음 타입",
        "color": "#00a8ff",
        "tags": ["배려", "소통", "따뜻함"],
        "reason": "ENFJ는 사람들을 잘 이끌고 따뜻하게 챙기는 타입이에요. 사람을 태우고 바다를 건너는 다정한 라프라스와 잘 어울려요.",
        "study": "스터디 그룹에서 내용을 설명해보면 실력이 더 단단해져요."
    },
    "ENFP": {
        "name": "피카츄",
        "emoji": "⚡",
        "id": 25,
        "type": "전기 타입",
        "color": "#f1c40f",
        "tags": ["활발함", "긍정", "친화력"],
        "reason": "ENFP는 밝고 에너지가 넘치며 사람들과 금방 친해지는 타입이에요. 귀엽고 활기찬 피카츄와 딱 맞습니다.",
        "study": "짧은 시간 집중하고 보상을 주는 방식이 잘 맞아요. 25분 공부 후 5분 휴식을 추천해요."
    },
    "ISTJ": {
        "name": "거북왕",
        "emoji": "💧",
        "id": 9,
        "type": "물 타입",
        "color": "#0984e3",
        "tags": ["책임감", "성실함", "안정감"],
        "reason": "ISTJ는 책임감이 강하고 꾸준한 타입이에요. 단단한 방어력과 안정적인 힘을 가진 거북왕과 잘 어울립니다.",
        "study": "매일 같은 시간에 공부하는 루틴을 만들면 큰 효과를 볼 수 있어요."
    },
    "ISFJ": {
        "name": "잠만보",
        "emoji": "🍙",
        "id": 143,
        "type": "노말 타입",
        "color": "#2d98da",
        "tags": ["포근함", "배려", "든든함"],
        "reason": "ISFJ는 주변 사람을 조용히 챙기는 따뜻한 타입이에요. 포근하고 든든한 잠만보처럼 편안한 매력이 있습니다.",
        "study": "무리하지 말고 충분한 휴식과 함께 꾸준히 반복하는 공부가 잘 맞아요."
    },
    "ESTJ": {
        "name": "괴력몬",
        "emoji": "💪",
        "id": 68,
        "type": "격투 타입",
        "color": "#45aaf2",
        "tags": ["실행력", "질서", "책임감"],
        "reason": "ESTJ는 현실적이고 실행력이 뛰어난 타입이에요. 강한 힘과 추진력을 가진 괴력몬과 잘 어울립니다.",
        "study": "문제집 페이지 수나 문제 개수처럼 구체적인 목표를 세우면 좋아요."
    },
    "ESFJ": {
        "name": "푸크린",
        "emoji": "🎀",
        "id": 40,
        "type": "노말 / 페어리 타입",
        "color": "#ff79c6",
        "tags": ["사교성", "친절", "분위기 메이커"],
        "reason": "ESFJ는 사람들과 어울리는 것을 좋아하고 분위기를 밝게 만드는 타입이에요. 사랑스러운 푸크린과 잘 맞아요.",
        "study": "친구와 서로 퀴즈를 내며 공부하면 집중력이 올라갈 수 있어요."
    },
    "ISTP": {
        "name": "개굴닌자",
        "emoji": "🥷",
        "id": 658,
        "type": "물 / 악 타입",
        "color": "#0066cc",
        "tags": ["실용적", "침착함", "순발력"],
        "reason": "ISTP는 조용하지만 상황 판단이 빠르고 실전 능력이 뛰어난 타입이에요. 민첩하고 멋진 개굴닌자와 잘 어울립니다.",
        "study": "이론을 본 뒤 바로 문제에 적용해보는 방식이 효과적이에요."
    },
    "ISFP": {
        "name": "님피아",
        "emoji": "🌸",
        "id": 700,
        "type": "페어리 타입",
        "color": "#ff9ff3",
        "tags": ["감성", "예술적", "다정함"],
        "reason": "ISFP는 감각적이고 부드러운 매력을 가진 타입이에요. 사랑스럽고 우아한 님피아와 잘 어울립니다.",
        "study": "필기 색상과 그림, 도식을 활용하면 기억하기 쉬워져요."
    },
    "ESTP": {
        "name": "윈디",
        "emoji": "🐾",
        "id": 59,
        "type": "불꽃 타입",
        "color": "#ff6b35",
        "tags": ["모험심", "활동적", "용감함"],
        "reason": "ESTP는 즉흥적이고 활동적이며 도전을 즐기는 타입이에요. 빠르고 용감한 윈디와 찰떡입니다.",
        "study": "가만히 오래 앉아 있기보다 짧고 강하게 여러 번 공부하는 방식이 잘 맞아요."
    },
    "ESFP": {
        "name": "파치리스",
        "emoji": "✨",
        "id": 417,
        "type": "전기 타입",
        "color": "#5dade2",
        "tags": ["흥", "귀여움", "에너지"],
        "reason": "ESFP는 밝고 즐거운 분위기를 만드는 타입이에요. 통통 튀는 매력의 파치리스와 잘 어울립니다.",
        "study": "공부 목표를 달성할 때마다 작은 보상을 정하면 동기부여가 잘 돼요."
    }
}

lucky_items = [
    "파란색 노트 💙",
    "반짝이는 볼펜 🖊️",
    "귀여운 스티커 ⭐",
    "시원한 물 한 병 🧊",
    "포켓몬볼 키링 🔴",
    "달콤한 간식 🍪",
    "하늘색 후드티 🩵",
    "작은 응원 메모 📝"
]

cheer_messages = [
    "오늘도 너의 모험은 계속된다!",
    "작은 노력도 경험치가 되고 있어!",
    "실패해도 괜찮아. 다시 도전하면 레벨업!",
    "너는 이미 충분히 멋진 트레이너야!",
    "오늘의 집중력이 내일의 진화를 만든다!"
]

# =========================
# 상단 화면
# =========================
st.markdown("<div class='main-title'>💙 MBTI 포켓몬 추천기 💙</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>나의 MBTI를 고르면 찰떡 포켓몬이 등장해요! 🐾✨</div>",
    unsafe_allow_html=True
)
st.markdown("<div class='pokeball-line'></div>", unsafe_allow_html=True)

# =========================
# 입력 영역
# =========================
left, center, right = st.columns([1, 1.4, 1])

with center:
    st.markdown("<div class='cute-card sparkle'>", unsafe_allow_html=True)

    user_name = st.text_input(
        "이름 또는 닉네임을 입력하세요",
        placeholder="예: 피카츄마스터"
    )

    selected_mbti = st.selectbox(
        "나의 MBTI를 선택하세요!",
        list(pokemon_data.keys()),
        index=list(pokemon_data.keys()).index("ENFP")
    )

    st.caption("※ 이 추천은 재미용입니다. 실제 성격을 정확히 판단하는 도구는 아니에요.")

    start = st.button("내 포켓몬 소환하기 💫")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 결과 출력
# =========================
if start:
    data = pokemon_data[selected_mbti]
    display_name = user_name.strip() if user_name.strip() else "당신"

    # 재미있는 로딩 효과
    with st.spinner("포켓몬을 찾는 중... 🔍"):
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.008)
            progress.progress(i + 1)

    st.balloons()

    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{data['id']}.png"

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.8, 1.5, 0.8])

    with col2:
        st.markdown("<div class='result-card sparkle'>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class='pokemon-name'>
                {data['emoji']} {display_name}님의 포켓몬은<br>
                {data['name']}!
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class='pokemon-type'>
                {selected_mbti} · {data['type']}
            </div>
            """,
            unsafe_allow_html=True
        )

        # 이미지에 애니메이션을 주기 위해 HTML img 사용
        st.markdown(
            f"""
            <div class='pokemon-img-wrap' style='text-align:center;'>
                <img src="{image_url}" width="360" style="max-width:90%;">
            </div>
            """,
            unsafe_allow_html=True
        )

        tag_html = "<div class='tag-box'>"
        for tag in data["tags"]:
            tag_html += f"<span class='tag'>#{tag}</span>"
        tag_html += "</div>"
        st.markdown(tag_html, unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class='reason-box'>
                <b>💙 추천 이유</b><br>
                {data['reason']}
            </div>
            """,
            unsafe_allow_html=True
        )

        random.seed(selected_mbti + display_name)
        lucky_item = random.choice(lucky_items)
        cheer = random.choice(cheer_messages)

        st.markdown(
            f"""
            <div class='mini-box'>
                🎁 오늘의 행운 아이템<br>
                <span style="font-size:24px;">{lucky_item}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class='mini-box'>
                📚 포켓몬이 주는 공부 팁<br>
                <span style="font-size:20px;">{data['study']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class='mini-box'>
                🏆 오늘의 응원 메시지<br>
                <span style="font-size:21px;">"{cheer}"</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.4, 1])

    with col2:
        st.markdown(
            """
            <div class='cute-card sparkle'>
                <div style='text-align:center; font-size:28px; color:#075a9c; font-weight:900;'>
                    아직 포켓몬이 숨어 있어요... 🫧
                </div>
                <div style='text-align:center; font-size:19px; color:#17689e; margin-top:10px;'>
                    MBTI를 고르고 버튼을 누르면<br>
                    귀여운 포켓몬이 나타납니다! 🐾✨
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# 전체 추천표
# =========================
st.markdown("<br>", unsafe_allow_html=True)

with st.expander("📘 전체 MBTI별 추천 포켓몬 보기"):
    cols = st.columns(4)
    for idx, (mbti, data) in enumerate(pokemon_data.items()):
        with cols[idx % 4]:
            st.markdown(
                f"""
                <div style="
                    background: rgba(255,255,255,0.78);
                    border-radius: 18px;
                    padding: 14px;
                    margin-bottom: 12px;
                    text-align: center;
                    box-shadow: 0 6px 14px rgba(0,80,150,0.12);
                    border: 2px solid white;
                ">
                    <div style="font-size:26px;">{data['emoji']}</div>
                    <b style="color:#075a9c;">{mbti}</b><br>
                    <span style="color:#17689e;">{data['name']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================
# 하단
# =========================
st.markdown(
    """
    <div class='footer'>
        Made with Streamlit 💙 | Pokemon images from PokeAPI official artwork URLs<br>
        재미용 MBTI 포켓몬 추천 웹앱입니다 🐳✨
    </div>
    """,
    unsafe_allow_html=True
)
