# streamlit run pages/McBTI.py

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib

# ✅ 페이지 설정
st.set_page_config(page_title="🍔 나의 McBTI는?", layout="centered")

# ✅ 경로 설정
BASE_DIR = os.path.dirname(__file__)
IMG_PATH = os.path.join(BASE_DIR, "..", "data", "burgers.png")
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "mcbti.csv")

# ✅ 한글 폰트 설정
font_path = 'C:\\Windows\\Fonts\\malgun.ttf'
font_prop = fm.FontProperties(fname=font_path)
matplotlib.rc('font', family=font_prop.get_name())

# ✅ 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "answers" not in st.session_state:
    st.session_state.answers = []

# ✅ 카드 공통 CSS 정의
st.markdown("""
    <style>
    .option-card {
        background-color: #2e2e2e;
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        border: 2px solid transparent;
        transition: 0.2s ease;
        cursor: pointer;
    }
    .option-card:hover {
        border-color: #f39c12;
        background-color: #3a3a3a;
    }
    .option-card.selected {
        border-color: lime;
        background-color: #3a3a3a;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ 1. 인트로 페이지
# ✅ 1. 인트로 페이지
if st.session_state.page == "intro":
    st.markdown("""
        <div style='text-align: center; padding-top: 20px;'>
            <h1 style='font-size: 60px; font-weight: 900; margin-bottom: 0.1em;'>🍔 나의 <span style="color:#ffcf48;">McBTI</span>는? 🍔</h1>
            <p style='font-size: 20px; color: #CCCCCC; margin-top: 0.2em;'>버거로 알아보는 나의 성격 유형!</p>
        </div>
    """, unsafe_allow_html=True)


    if os.path.exists(IMG_PATH):
        st.image(IMG_PATH, use_column_width=True, caption="당신을 기다리는 버거들")

    else:
        st.warning("이미지를 불러올 수 없습니다.")

    with st.container():
        st.markdown("""
            <div class="option-card" style="text-align: center;">
                <div style="font-size: 40px;">🧠</div>
                <div style="font-weight: bold; font-size: 20px; margin-top: 10px;">McBTI 심리 테스트</div>
                <div style="font-size: 14px; margin-top: 5px; margin-bottom: 18px;">
                    심리 유형을 통해 나에게 어울리는 버거를 추천받아보세요!
                </div>
        """, unsafe_allow_html=True)

        if st.button("🔥 테스트 시작하기", use_container_width=True):
            st.session_state.page = "quiz"
            st.rerun()


        st.markdown("</div>", unsafe_allow_html=True)

# ✅ 2. 질문 페이지
elif st.session_state.page == "quiz":
    questions = [
        {"question": "Q1. 모임에 초대받았을 때 당신은?", "options": ["A. 좋아! 사람들과 어울리면 에너지가 나요. (E)", "B. 부담돼요. 혼자가 편해요. (I)"]},
        {"question": "Q2. 대화할 때 나는?", "options": ["A. 즉흥적으로 말이 술술 나와요. (E)", "B. 생각 정리 후 말해요. (I)"]},
        {"question": "Q3. 정보를 받아들일 때 나는?", "options": ["A. 눈에 보이는 사실이 중요해요. (S)", "B. 의미와 가능성이 더 궁금해요. (N)"]},
        {"question": "Q4. 설명서를 읽을 때 나는?", "options": ["A. 순서대로 꼼꼼히 읽어요. (S)", "B. 대충 보고 감으로 파악해요. (N)"]},
        {"question": "Q5. 친구가 고민 상담할 때 나는?", "options": ["A. 객관적인 해결책을 말해줘요. (T)", "B. 감정을 공감해줘요. (F)"]},
        {"question": "Q6. 결정을 내릴 때 나는?", "options": ["A. 논리적으로 분석해요. (T)", "B. 사람 마음과 분위기를 고려해요. (F)"]},
        {"question": "Q7. 여행 계획을 세울 때 나는?", "options": ["A. 일정을 미리 정해놓고 움직여요. (J)", "B. 즉흥적으로 즐겨요. (P)"]},
        {"question": "Q8. 과제를 할 때 나는?", "options": ["A. 마감 전 미리 끝내야 마음 편해요. (J)", "B. 마감 직전이 집중이 잘 돼요. (P)"]},
        {"question": "Q9. 메뉴를 고를 때 나는?", "options": ["A. 새로운 걸 도전해보고 싶어요! (N)", "B. 먹던 거 또 먹어야 안심돼요. (S)"]},
        {"question": "Q10. 계획이 바뀌면?", "options": ["A. 스트레스 받아요. 원래대로 해야 해요. (J)", "B. 뭐 어때요~ 즉흥도 재밌죠. (P)"]},
        {"question": "Q11. 실수했을 때 나는?", "options": ["A. 원인 분석부터 해요. (T)", "B. 스스로를 위로해요. (F)"]},
        {"question": "Q12. 점심 메뉴를 친구가 정해준다면?", "options": ["A. 편해서 좋아요! (I)", "B. 내가 고르는 게 더 좋아요! (E)"]},
    ]

    total = len(questions)
    current = len(st.session_state.answers)
    q = questions[current]

    selected_key = f"selected_{current}"
    if selected_key not in st.session_state:
        st.session_state[selected_key] = None

    st.markdown(f"<h4 style='text-align:center'>{q['question']}</h4>", unsafe_allow_html=True)

    for i, option in enumerate(q["options"]):
        card_id = f"card_{current}_{i}"
        is_selected = (st.session_state[selected_key] == option)
        card_class = "option-card selected" if is_selected else "option-card"

        st.markdown(f"""
            <div class="{card_class}" onclick="document.getElementById('{card_id}').click()">
                {option}
            </div>
        """, unsafe_allow_html=True)

        if st.button("선택", key=card_id):
            st.session_state[selected_key] = option
            st.session_state.answers.append(option)
            if current + 1 < total:
                st.session_state.page = "quiz"
            else:
                st.session_state.page = "result"
            st.rerun()  # ✅ 최신 버전용

# ✅ 3. 결과 페이지
elif st.session_state.page == "result":
    counts = {c: 0 for c in "EISNTFJP"}
    for ans in st.session_state.answers:
        for c in counts:
            if f"({c})" in ans:
                counts[c] += 1

    mbti = "".join([
        "E" if counts["E"] >= counts["I"] else "I",
        "S" if counts["S"] >= counts["N"] else "N",
        "T" if counts["T"] >= counts["F"] else "F",
        "J" if counts["J"] >= counts["P"] else "P"
    ])

    burger_map = {
        "INTJ": ("더블 1955 버거", "차갑고 진한 고기맛처럼 계획적"),
        "INTP": ("트리플 치즈버거", "치즈처럼 말랑하지만 복잡함"),
        "ENTJ": ("쿼터파운더 치즈", "한 입에 존재감 폭발, 리더맛"),
        "ENTP": ("슈비 버거", "새우+소고기 조합처럼 상상초월"),
        "INFJ": ("토마토 치즈 비프 버거", "부드럽고 진지한 속마음 토핑"),
        "INFP": ("불고기 버거", "달달하고 감성 터지는 맛"),
        "ENFJ": ("빅맥", "모두 챙기는 층층한 다정함"),
        "ENFP": ("맥스파이시 상하이 버거", "매콤하고 톡톡 튀는 자유인"),
        "ISTJ": ("맥치킨", "늘 같은 자리, 기본에 진심"),
        "ISFJ": ("슈슈 버거", "바삭함 속 따뜻한 배려심"),
        "ESTJ": ("더블 치즈버거", "정석대로 두 배로 확실하게"),
        "ESFJ": ("맥크리스피 클래식 버거", "딱 맞는 조합, 모두를 위해"),
        "ISTP": ("더블 불고기 버거", "조용하지만 실속 가득"),
        "ISFP": ("치즈버거", "소박하지만 감성 깊은 맛"),
        "ESTP": ("맥크리스피 디럭스 버거", "바삭! 지금 아니면 못 참음"),
        "ESFP": ("더블 맥스파이시 상하이 버거", "매운 맛도 즐기는 인싸감성")
    }

    burger, label = burger_map[mbti]

    st.subheader("🍔 당신에게 어울리는 버거는 🍔")
    st.markdown(f"## **{burger}**")
    st.markdown(f"**성격 유형:** {label}")
    st.markdown(f"**MBTI 유형:** {mbti}")

    # 영양정보 보기
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        df['메뉴'] = df['메뉴'].str.strip()
        menu_data = df[df['메뉴'] == burger]

        if not menu_data.empty:
            st.markdown("### 🍽 영양성분 정보")
            st.dataframe(menu_data[['단백질', '지방', '나트륨', '당류']])

    # 다시하기
    if st.button("🔄 다시 테스트하기"):
        st.session_state.page = "intro"
        st.session_state.answers = []
        for key in list(st.session_state.keys()):
            if key.startswith("selected_"):
                del st.session_state[key]
        st.rerun()