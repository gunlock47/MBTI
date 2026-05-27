import streamlit as st
import time

# 1. 페이지 설정 (탭 제목과 귀여운 고래 이모지)
st.set_page_config(
    page_title="나의 MBTI 찰떡 포켓몬 추천! 💙",
    page_icon="🐳",
    layout="centered"
)

# 2. 🎨 CSS를 이용한 커스텀 파란색 배경 및 스타일 설정
st.markdown("""
    <style>
    /* 전체 앱 배경을 부드러운 파스텔톤 파란색 그라데이션으로 설정 */
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 50%, #7dd3fc 100%);
    }
    
    /* 제목(H1) 글자 스타일 지정 */
    h1 {
        color: #1e3a8a !important;
        font-family: 'Comic Sans MS', sans-serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* 소제목 및 서브 타이틀 스타일 */
    h3, h4 {
        color: #1e40af !important;
    }
    
    /* 질문 텍스트 라벨 스타일 수정 */
    .stSelectbox label {
        color: #1e3a8a !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }
    
    /* 결과 카드 스타일 (흰색의 둥글고 투명도 있는 배경 박스) */
    .result-card {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #93c5fd;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)


# 3. MBTI와 매칭되는 포켓몬 데이터 사전 (PokeAPI 공식 도감 ID 포함)
# image_id를 이용해 실시간 고화질 이미지를 가져옵니다!
mbti_pokemon = {
    "INFP": {
        "name": "뮤 (Mew)",
        "emoji": "🧚‍♀️✨",
        "image_id": 151,
        "traits": "감수성이 풍부하고 상상력이 넘치는 평화주의자",
        "desc": "마음이 따뜻하고 조용하지만, 내면에는 무한한 상상력과 에너지가 숨겨져 있어요. 신비롭고 순수한 뮤가 당신과 똑 닮았네요!"
    },
    "INFJ": {
        "name": "에브이 (Espeon)",
        "emoji": "🔮🐱",
        "image_id": 196,
        "traits": "통찰력 있고 깊은 공감 능력을 가진 예언자",
        "desc": "사람의 마음을 꿰뚫어 보는 섬세함과 높은 직관력을 가지고 있어요. 조용히 타인을 돕고 평화를 사랑하는 모습이 에브이의 신비로운 분위기와 어울려요."
    },
    "INTP": {
        "name": "로토무 (Rotom)",
        "emoji": "⚡️📺",
        "image_id": 479,
        "traits": "아이디어가 넘치고 호기심이 많은 천재 분석가",
        "desc": "새로운 지식을 배우는 것을 즐기고 늘 흥미로운 주제에 몰두해요. 전자기기에 들어가 다양한 형태로 변신하는 창의적인 로토무가 떠올라요!"
    },
    "INTJ": {
        "name": "블래키 (Umbreon)",
        "emoji": "🌙🐺",
        "image_id": 197,
        "traits": "독립적이고 전략적인 계획가",
        "desc": "스스로 세운 목표를 향해 묵묵하고 완벽하게 나아가는 사람이에요. 어둠 속에서 스스로 빛나는 신비롭고 똑똑한 블래키와 찰떡궁합이에요."
    },
    "ENFP": {
        "name": "이브이 (Eevee)",
        "emoji": "🦊💖",
        "image_id": 133,
        "traits": "언제나 열정적이고 에너지가 넘치는 재기발랄가",
        "desc": "가능성으로 가득 차 있으며, 주변 사람들에게 긍정적인 에너지를 전파해요. 어떤 환경이든 잘 적응하고 무한한 진화 가능성을 지닌 이브이 그 자체!"
    },
    "ENFJ": {
        "name": "토게피 (Togepi)",
        "emoji": "🐣✨",
        "image_id": 175,
        "traits": "사람을 이끄는 따뜻한 마음의 카리스마 지도자",
        "desc": "주변 사람들의 행복을 진심으로 바라고 챙겨주는 천사 같은 성격이에요. 행복을 부르는 품위의 토게피처럼 모두에게 사랑받는 존재랍니다."
    },
    "ENTP": {
        "name": "팬텀 (Gengar)",
        "emoji": "😈💜",
        "image_id": 94,
        "traits": "장난기 넘치고 똑똑한 발명가",
        "desc": "토론을 즐기고 고정관념에서 벗어난 기발한 생각을 잘해요. 가끔은 짓궂은 장난을 치지만 결코 미워할 수 없는 유쾌한 팬텀과 닮았어요!"
    },
    "ENTJ": {
        "name": "리자몽 (Charizard)",
        "emoji": "🔥🦖",
        "image_id": 6,
        "traits": "목표를 향해 거침없이 나아가는 지도자",
        "desc": "강력한 리더십과 추진력으로 팀을 승리로 이끄는 카리스마 넘치는 사람이에요. 날개로 하늘을 높이 날며 불꽃을 뿜는 리자몽처럼 열정적이에요."
    },
    "ISFP": {
        "name": "메타몽 (Ditto)",
        "emoji": "🫠🎨",
        "image_id": 132,
        "traits": "예술적 감각이 뛰어나고 유연한 영혼",
        "desc": "자유로운 영혼의 소유자로, 어떤 상황이든 물 흐르듯 유연하게 대처해요. 다른 사람들과 잘 융화되고 예술적 끼가 넘치는 메타몽과 잘 어울려요."
    },
    "ISFJ": {
        "name": "럭키 (Chansey)",
        "emoji": "🥚💗",
        "image_id": 113,
        "traits": "헌신적이고 따뜻하며 책임감이 강한 수호자",
        "desc": "늘 남을 먼저 배려하고 꼼꼼하게 챙겨주는 다정한 사람이에요. 상처받은 이들을 치료해주고 행복을 나눠주는 럭키가 바로 당신의 모습입니다."
    },
    "ISTP": {
        "name": "루카리오 (Lucario)",
        "emoji": "🥋🐺",
        "image_id": 448,
        "traits": "조용히 상황을 파악하고 해결하는 해결사",
        "desc": "냉철하고 관찰력이 뛰어나며, 도구를 다루거나 문제를 해결하는 능력이 뛰어납니다. 과묵하지만 내면의 힘과 감각이 발달한 루카리오를 닮았어요."
    },
    "ISTJ": {
        "name": "꼬부기 (Squirtle)",
        "emoji": "🐢💧",
        "image_id": 7,
        "traits": "철저하고 성실하게 약속을 지키는 현실주의자",
        "desc": "자신이 맡은 일은 끝까지 책임지고 해내는 믿음직한 사람이에요. 규칙을 잘 지키며 단체 생활에서도 든든한 버팀목이 되어주는 꼬부기와 닮았네요!"
    },
    "ESFP": {
        "name": "푸린 (Jigglypuff)",
        "emoji": "🎤🎈",
        "image_id": 39,
        "traits": "어디서나 스포트라이트를 받는 분위기 메이커",
        "desc": "인생을 축제처럼 즐기고 사교성이 넘쳐 친구들에게 늘 인기가 많아요. 마이크를 잡고 노래하며 모두의 시선을 사로잡는 사랑스러운 푸린과 똑 닮았어요."
    },
    "ESFJ": {
        "name": "푸크린 (Wigglytuff)",
        "emoji": "🌸🧸",
        "image_id": 40,
        "traits": "다정다감하고 사교성이 풍부한 협력가",
        "desc": "누구에게나 친절하고 공감 능력이 뛰어나 조화로운 관계를 만들어요. 부드러운 털로 안아주며 주변 사람들을 포근하게 챙기는 푸크린의 성격과 같습니다."
    },
    "ESTP": {
        "name": "에이스번 (Cinderace)",
        "emoji": "⚽️🔥",
        "image_id": 815,
        "traits": "행동이 빠르고 도전을 즐기는 모험가",
        "desc": "생각하기보다 먼저 행동으로 옮기는 에너자이저! 운동 신경이 좋고 활기찬 성격으로, 필드를 종횡무진 누비는 에이스번처럼 열정적인 사람이에요."
    },
    "ESTJ": {
        "name": "윈디 (Arcanine)",
        "emoji": "🦁🔥",
        "image_id": 59,
        "traits": "엄격하고 책임감 있는 든든한 리더",
        "desc": "조직을 체계적으로 관리하고 약속과 신의를 매우 중요하게 생각합니다. 위엄이 넘치면서도 동료들에게는 한없이 충성스럽고 든든한 윈디가 연상되네요."
    }
}

# 4. 메인 화면 UI 디자인
st.title("🐳 나의 MBTI 찰떡 포켓몬! 🐳")
st.write("<p style='text-align: center; color: #1e3a8a;'>당신의 MBTI에 꼭 맞는 운명의 포켓몬과 고화질 일러스트를 소환해 드려요! 🔮✨</p>", unsafe_allow_html=True)

# 여백 조절
st.write("")

# 5. MBTI 선택 입력창
mbti_list = list(mbti_pokemon.keys())
selected_mbti = st.selectbox("🤔 당신의 MBTI는 무엇인가요?", mbti_list, index=0)

st.write("")

# 6. 결과 출력 버튼 클릭 시 작동 로직
if st.button("내 포켓몬 소환하기! 🔮✨", use_container_width=True):
    # 파란색 테마에 맞춘 로딩 스피너 연출!
    with st.spinner("몬스터볼이 흔들리는 중... 흔들흔들... 🔵⏳"):
        time.sleep(1.5) 
    
    # 해당 MBTI 데이터 가져오기
    pokemon = mbti_pokemon[selected_mbti]
    
    # 축하 효과 (풍선 발사! 🎈)
    st.balloons()
    
    # 결과 화면을 깔끔하게 보여주기 위한 흰색 카드 상자 만들기
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    
    # 7. 이미지 가운데 정렬을 위해 3개의 컬럼 레이아웃 생성
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 공식 PokeAPI 고화질 이미지 URL 조합하기
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon['image_id']}.png"
        # 캡션(설명)과 함께 이미지 띄우기
        st.image(image_url, caption=f"짜잔! {pokemon['name']}", use_container_width=True)
        
    # 결과 요약
    st.success(f"### 🎉 당신은 **[{pokemon['name']}]** 입니다! {pokemon['emoji']}")
    
    # 파란색 텍스트 상자로 특징 보여주기
    st.info(f"💡 **성격 특징**: {pokemon['traits']}")
    
    # 상세 설명 출력
    st.markdown("#### 📘 포켓몬 도감 상세 분석")
    st.write(pokemon['desc'])
    
    st.markdown("</div>", unsafe_allow_html=True) # 카드 상자 닫기
    
    st.divider()
    st.caption("<p style='text-align: center; color: #1e40af;'>💙 본 프로그램은 당곡고등학교 학생의 아이디어와 실습 수업의 결과물입니다. 💙</p>", unsafe_allow_html=True)
