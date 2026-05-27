import streamlit as st
import random

# -----------------------------
# 페이지 기본 설정
# -----------------------------
st.set_page_config(
    page_title="MBTI 포켓몬 추천기",
    page_icon="💙",
    layout="centered"
)

# -----------------------------
# CSS 스타일
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gamja+Flower&family=Noto+Sans+KR:wght@400;700;900&display=swap');

    .stApp {
        background: linear-gradient(135deg, #dff6ff 0%, #b8e8ff 35%, #7fc8ff 70%, #4aa3ff 100%);
        font-family: 'Noto Sans KR', sans-serif;
    }

    .main-title {
        text-align: center;
        font-size: 46px;
        font-weight: 900;
        color: #0b4f8a;
        text-shadow: 2px 2px 0px #ffffff;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        font-size: 20px;
        color: #155f9c;
        margin-bottom: 30px;
    }

    .cute-card {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 25px;
        padding: 25px;
        box-shadow: 0 8px 20px rgba(0, 75, 140, 0.25);
        border: 3px solid #ffffff;
        margin-top: 20px;
    }

    .pokemon-name {
        text-align: center;
        font-size: 38px;
        font-weight: 900;
        color: #0b4f8a;
        margin-bottom: 5px;
    }

    .pokemon-type {
        text-align: center;
        font-size: 20px;
        color: #2979b8;
        margin-bottom: 20px;
    }

    .reason-box {
        background: #eaf8ff;
        border-left: 7px solid #4aa3ff;
        padding: 18px;
        border-radius: 15px;
        color: #174b73;
        font-size: 18px;
        line-height: 1.7;
        margin-top: 15px;
    }

    .tag {
        display: inline-block;
        background: #4aa3ff;
        color: white;
        padding: 7px 13px;
        border-radius: 20px;
        margin: 5px;
        font-size: 15px;
        font-weight: 700;
    }

    .small-text {
        text-align: center;
        color: #1e5f91;
        font-size: 14px;
        margin-top: 30px;
    }

    div[data-testid="stSelectbox"] label {
        color: #0b4f8a;
        font-size: 20px;
        font-weight: 800;
    }

    .stButton > button {
        background-color: #1e9bff;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 12px 25px;
        font-size: 18px;
        font-weight: 800;
        box-shadow: 0 5px 12px rgba(0, 75, 140, 0.3);
    }

    .stButton > button:hover {
        background-color: #0077d9;
        color: white;
        transform: scale(1.03);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# MBTI별 포켓몬 데이터
# -----------------------------
pokemon_data = {
    "INTJ": {
        "name": "뮤츠",
        "emoji": "🧬",
        "id": 150,
        "type": "에스퍼 타입",
        "tags": ["전략가", "분석력", "독립적"],
        "reason": "INTJ는 깊이 생각하고 계획을 세우는 전략가 타입이에요. 강력한 지능과 독립적인 분위기를 가진 뮤츠와 잘 어울립니다."
    },
    "INTP": {
        "name": "메타몽",
        "emoji": "🫧",
        "id": 132,
        "type": "노말 타입",
        "tags": ["호기심", "탐구", "창의적"],
        "reason": "INTP는 새로운 아이디어를 탐구하고 다양한 가능성을 실험하는 타입이에요. 무엇이든 변신할 수 있는 메타몽처럼 유연한 사고력을 가지고 있어요."
    },
    "ENTJ": {
        "name": "리자몽",
        "emoji": "🔥",
        "id": 6,
        "type": "불꽃 / 비행 타입",
        "tags": ["리더십", "추진력", "카리스마"],
        "reason": "ENTJ는 목표를 향해 강하게 나아가는 리더형이에요. 뜨거운 에너지와 강한 존재감을 가진 리자몽과 잘 어울립니다."
    },
    "ENTP": {
        "name": "팬텀",
        "emoji": "👻",
        "id": 94,
        "type": "고스트 / 독 타입",
        "tags": ["재치", "장난기", "아이디어"],
        "reason": "ENTP는 말솜씨와 아이디어가 뛰어나고 장난기 있는 타입이에요. 톡톡 튀는 매력의 팬텀과 찰떡궁합입니다."
    },
    "INFJ": {
        "name": "루기아",
        "emoji": "🌊",
        "id": 249,
        "type": "에스퍼 / 비행 타입",
        "tags": ["이상주의", "통찰력", "조용한 힘"],
        "reason": "INFJ는 깊은 내면과 따뜻한 이상을 가진 타입이에요. 바다 깊은 곳에서 조용히 힘을 품고 있는 루기아와 잘 어울립니다."
    },
    "INFP": {
        "name": "이브이",
        "emoji": "🤎",
        "id": 133,
        "type": "노말 타입",
        "tags": ["감성", "가능성", "순수함"],
        "reason": "INFP는 따뜻한 마음과 무한한 가능성을 가진 타입이에요. 여러 모습으로 진화할 수 있는 이브이처럼 자신만의 길을 찾아갑니다."
    },
    "ENFJ": {
        "name": "라프라스",
        "emoji": "🎵",
        "id": 131,
        "type": "물 / 얼음 타입",
        "tags": ["배려", "소통", "따뜻함"],
        "reason": "ENFJ는 사람들을 잘 이끌고 따뜻하게 챙기는 타입이에요. 사람을 태우고 바다를 건너는 다정한 라프라스와 잘 어울려요."
    },
    "ENFP": {
        "name": "피카츄",
        "emoji": "⚡",
        "id": 25,
        "type": "전기 타입",
        "tags": ["활발함", "긍정", "친화력"],
        "reason": "ENFP는 밝고 에너지가 넘치며 사람들과 금방 친해지는 타입이에요. 귀엽고 활기찬 피카츄와 딱 맞습니다."
    },
    "ISTJ": {
        "name": "거북왕",
        "emoji": "💧",
        "id": 9,
        "type": "물 타입",
        "tags": ["책임감", "성실함", "안정감"],
        "reason": "ISTJ는 책임감이 강하고 꾸준한 타입이에요. 단단한 방어력과 안정적인 힘을 가진 거북왕과 잘 어울립니다."
    },
    "ISFJ": {
        "name": "잠만보",
        "emoji": "🍙",
        "id": 143,
        "type": "노말 타입",
        "tags": ["포근함", "배려", "든든함"],
        "reason": "ISFJ는 주변 사람을 조용히 챙기는 따뜻한 타입이에요. 포근하고 든든한 잠만보처럼 편안한 매력을 가지고 있습니다."
    },
    "ESTJ": {
        "name": "괴력몬",
        "emoji": "💪",
        "id": 68,
        "type": "격투 타입",
        "tags": ["실행력", "질서", "책임감"],
        "reason": "ESTJ는 현실적이고 실행력이 뛰어난 타입이에요. 강한 힘과 추진력을 가진 괴력몬과 잘 어울립니다."
    },
    "ESFJ": {
        "name": "푸크린",
        "emoji": "🎀",
        "id": 40,
        "type": "노말 / 페어리 타입",
        "tags": ["사교성", "친절", "분위기 메이커"],
        "reason": "ESFJ는 사람들과 어울리는 것을 좋아하고 분위기를 밝게 만드는 타입이에요. 귀엽고 사랑스러운 푸크린과 잘 맞아요."
    },
    "ISTP": {
        "name": "개굴닌자",
        "emoji": "🥷",
        "id": 658,
        "type": "물 / 악 타입",
        "tags": ["실용적", "침착함", "순발력"],
        "reason": "ISTP는 조용하지만 상황 판단이 빠르고 실전 능력이 뛰어난 타입이에요. 민첩하고 멋진 개굴닌자와 잘 어울립니다."
    },
    "ISFP": {
        "name": "님피아",
        "emoji": "🌸",
        "id": 700,
        "type": "페어리 타입",
        "tags": ["감성", "예술적", "다정함"],
        "reason": "ISFP는 감각적이고 부드러운 매력을 가진 타입이에요. 사랑스럽고 우아한 님피아와 잘 어울립니다."
    },
    "ESTP": {
        "name": "윈디",
        "emoji": "🐾",
        "id": 59,
        "type": "불꽃 타입",
        "tags": ["모험심", "활동적", "용감함"],
        "reason": "ESTP는 즉흥적이고 활동적이며 도전을 즐기는 타입이에요. 빠르고 용감한 윈디와 찰떡입니다."
    },
    "ESFP": {
        "name": "파치리스",
        "emoji": "✨",
        "id": 417,
        "type": "전기 타입",
        "tags": ["흥", "귀여움", "에너지"],
        "reason": "ESFP는 밝고 즐거운 분위기를 만드는 타입이에요. 통통 튀는 매력의 파치리스와 잘 어울립니다."
    }
}

# -----------------------------
# 부가 데이터
# -----------------------------
lucky_items = [
    "파란색 노트 💙",
    "귀여운 스티커 ⭐",
    "달콤한 간식 🍪",
    "반짝이는 볼펜 🖊️",
    "포켓몬볼 키링 🔴",
    "시원한 물 한 병 🧊",
    "작은 응원 메모 📝",
    "하늘색 후드티 🩵"
]

study_tips = [
    "오늘은 25분 집중하고 5분 쉬는 방법을 써보세요.",
    "어려운 문제는 바로 답을 보지 말고, 먼저 조건을 표시해보세요.",
    "공부 시작 전 오늘 할 일을 3개만 정하면 집중하기 쉬워요.",
    "암기할 내용은 소리 내어 설명하면 오래 기억됩니다.",
    "틀린 문제는 왜 틀렸는지 한 문장으로 적어보세요."
]

mbti_list = list(pokemon_data.keys())

# -----------------------------
# 상단 제목
# -----------------------------
st.markdown("<div class='main-title'>💙 MBTI 포켓몬 추천기 💙</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>나의 MBTI를 고르면 어울리는 포켓몬을 추천해드려요! 🐾✨</div>",
    unsafe_allow_html=True
)

st.info("이 웹앱은 재미용 추천입니다. 실제 성격을 정확히 판단하는 도구는 아니에요!")

# -----------------------------
# MBTI 선택
# -----------------------------
selected_mbti = st.selectbox(
    "나의 MBTI를 선택하세요!",
    mbti_list,
    index=mbti_list.index("ENFP")
)

button_clicked = st.button("내 포켓몬 만나기 💫")

# -----------------------------
# 결과 출력
# -----------------------------
if button_clicked:
    data = pokemon_data[selected_mbti]

    st.balloons()

    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{data['id']}.png"

    st.markdown("<div class='cute-card'>", unsafe_allow_html=True)

    st.markdown(
        f"<div class='pokemon-name'>{data['emoji']} {selected_mbti}의 포켓몬은 {data['name']}! {data['emoji']}</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='pokemon-type'>{data['type']}</div>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image_url, use_container_width=True)

    tag_html = ""
    for tag in data["tags"]:
        tag_html += f"<span class='tag'>#{tag}</span>"

    st.markdown(
        f"<div style='text-align:center;'>{tag_html}</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class='reason-box'>
        <b>추천 이유</b><br>
        {data['reason']}
        </div>
        """,
        unsafe_allow_html=True
    )

    random.seed(selected_mbti)
    lucky_item = random.choice(lucky_items)
    study_tip = random.choice(study_tips)

    st.markdown(
        f"""
        <div class='reason-box'>
        <b>오늘의 행운 아이템</b><br>
        {lucky_item}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class='reason-box'>
        <b>포켓몬이 주는 오늘의 공부 팁</b><br>
        {study_tip}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown(
        """
        <div class='cute-card'>
            <div style='text-align:center; font-size:24px; color:#0b4f8a; font-weight:800;'>
                아직 포켓몬이 숨어 있어요... 🫧<br>
                MBTI를 고르고 버튼을 눌러주세요!
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# 전체 MBTI 추천표
# -----------------------------
with st.expander("전체 MBTI별 추천 포켓몬 보기 📘"):
    for mbti, data in pokemon_data.items():
        st.write(f"{data['emoji']} **{mbti}** → **{data['name']}** / {data['type']}")

# -----------------------------
# 하단 안내
# -----------------------------
st.markdown(
    """
    <div class='small-text'>
    Made with Streamlit 💙 | Pokemon images from PokeAPI official artwork URLs
    </div>
    """,
    unsafe_allow_html=True
)
