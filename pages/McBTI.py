# streamlit run pages/McBTI.py
import streamlit as st
st.set_page_config(page_title="🍔 나의 McBTI는? 🍔", layout="centered")

# 📆 시작 페이지 (인트로) 복사되는 화면)
if "intro" not in st.session_state:
    st.session_state.intro = True
if 'page' not in st.session_state:
    st.session_state.page = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# 인트로 화면 보여주기
if st.session_state.intro:
    st.title("🍔 당신의 McBTI는? 🍔")
    # ✅ 귀여운 햄버거 이미지 넣기 (이미지 경로는 저장 위치에 따라 조정!)
    st.image("data/burger.png", width=300, caption="당신을 기다리는 버거", use_column_width=False)

    st.markdown("**Mc버거로 알아보는 나의 성격 유형!**<br><br>👇 아래 버튼을 눌러 시작해보세요!", unsafe_allow_html=True)
    cols = st.columns([1, 1, 1])  # 좌-중앙-우 나누기
    with cols[1]:
      if st.button("🔥 시작하기"):
        st.session_state.intro = False
    st.stop()

# 프로보안된 기존 컨텐츠들도 여전히 적용
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib

font_path = 'C:\\Windows\\Fonts\\malgun.ttf'
font_prop = fm.FontProperties(fname=font_path)
matplotlib.rc('font', family=font_prop.get_name())

# CSV
df = pd.read_csv("data/mcbti.csv", encoding="utf-8")

st.title("당신의 버거 성격유형을 알아보세요!")

# MBTI 질문
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

# 초기화
if 'page' not in st.session_state:
    st.session_state.page = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# 질문 페이지
if st.session_state.page < len(questions):
    q = questions[st.session_state.page]
     # ✅ 초기 선택 없음 (index=None)
    selected = st.radio(q["question"], q["options"], key=f"q{st.session_state.page}", index=None)

    # ✅ 선택된 경우에만 다음 버튼 활성화
    if selected:
        if st.button("➡ 다음 질문"):
            st.session_state.answers.append(selected)
            st.session_state.page += 1

# 결과 페이지
else:
    # MBTI 계산
    mbti = ""
    dimensions = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    for answer in st.session_state.answers:
        for key in dimensions:
            if f"({key})" in answer:
                dimensions[key] += 1
    mbti += "E" if dimensions["E"] >= dimensions["I"] else "I"
    mbti += "S" if dimensions["S"] >= dimensions["N"] else "N"
    mbti += "T" if dimensions["T"] >= dimensions["F"] else "F"
    mbti += "J" if dimensions["J"] >= dimensions["P"] else "P"

    # 버거 매핑
    burger_results = {
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

    burger = burger_results[mbti][0]
    label = burger_results[mbti][1]

    st.subheader("🍔 당신에게 어울리는 버거는 🍔")
    st.markdown(f"## **{burger}**")
    st.markdown(f"**성격 유형:** {label}")
    st.markdown(f"**MBTI 유형:** {mbti}")
   # 🎈 떠다니는 버거 애니메이션
    st.markdown("""
        <style>
    @keyframes floatBurger {
    0% {
        transform: translateY(0px);
        opacity: 1;
    }
    100% {
        transform: translateY(-600px);
        opacity: 0;
    }
    }
    .burger-float {
    position: fixed;
    font-size: 50px;
    animation: floatBurger 5s ease-in-out infinite;
    }
    </style>

    <div class="burger-float" style="left: 5%; top: 90%; animation-delay: 0s;">🍟🍔</div>
    <div class="burger-float" style="left: 15%; top: 92%; animation-delay: 1.3s;">🍔🍔</div>
    <div class="burger-float" style="left: 25%; top: 95%; animation-delay: 2s;">🍟🍟</div>
    <div class="burger-float" style="left: 35%; top: 91%; animation-delay: 1.5s;">🍔🍔</div>
    <div class="burger-float" style="left: 45%; top: 93%; animation-delay: 0.5s;">🍟🍔</div>
    <div class="burger-float" style="left: 55%; top: 90%; animation-delay: 2.5s;">🍔🍟</div>
    <div class="burger-float" style="left: 65%; top: 94%; animation-delay: 2s;">🍟🍔</div>
    <div class="burger-float" style="left: 75%; top: 91%; animation-delay: 3.5s;">🍔🍔</div>
    <div class="burger-float" style="left: 85%; top: 95%; animation-delay: 3s;">🍔🍟</div>
    <div class="burger-float" style="left: 95%; top: 92%; animation-delay: 4.5s;">🍟🍟</div>
     """, unsafe_allow_html=True)
    

    if st.button("🍽 영양성분 한 눈에 보기🍽"):
        df['메뉴'] = df['메뉴'].str.strip()
        menu_data = df[df['메뉴'] == burger]

        st.dataframe(menu_data[['단백질', '지방', '나트륨', '당류']].rename(
            columns={
                '단백질': '단백질(g)',
                '지방': '지방(g)',
                '나트륨': '나트륨(mg)',
                '당류': '당류(g)'
            }
        ), use_container_width=True, hide_index=True)

        nutrition = menu_data[['단백질', '지방', '나트륨', '당류']].iloc[0]
        korean_labels = ['단백질', '지방', '나트륨', '당류']

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(
            nutrition.values,
            labels=korean_labels,
            autopct='%1.1f%%',
            startangle=140,
            textprops={'fontsize': 14}
        )
        ax.set_title(f"{burger}의 영양소 비율", fontsize=18, fontproperties=font_prop)
        st.pyplot(fig)  

    # 다시하기 버튼
    if st.button("🔄 다시 테스트하기"):
        st.session_state.page = 0
        st.session_state.answers = []
        for i in range(len(questions)):
            st.session_state.pop(f"q{i}", None)