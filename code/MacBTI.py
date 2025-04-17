#streamlit run code/MacBTI.py
import streamlit as st
st.set_page_config(page_title="🍔 나의 MacBTI는? 🍔", layout="centered")

# 📆 시작 페이지 (인트로) 복사되는 화면)
if "intro" not in st.session_state:
    st.session_state.intro = True
if 'page' not in st.session_state:
    st.session_state.page = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# 인트로 화면 보여주기
if st.session_state.intro:
    st.title("🍔 당신의 MacBTI는? 🍔")
    # ✅ 귀여운 햄버거 이미지 넣기 (이미지 경로는 저장 위치에 따라 조정!)
    st.image("data/burger.png", width=300, caption="당신을 기다리는 버거", use_column_width=False)

    st.markdown("**Mac버거로 알아보는 나의 성격 유형!**<br><br>👇 아래 버튼을 눌러 시작해보세요!", unsafe_allow_html=True)
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
df = pd.read_csv("data/macbti.csv", encoding="utf-8")

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
    st.radio(q["question"], q["options"], key=f"q{st.session_state.page}")
    if st.button("➡ 다음 질문"):
        choice = st.session_state[f"q{st.session_state.page}"]
        st.session_state.answers.append(choice)
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
        "INTJ": ("더블 1955 버거", "계획 세우다 하루 다 감"),
        "INTP": ("트리플 치즈버거", "뇌는 바쁨, 몸은 침대에 붙어있음"),
        "ENTJ": ("쿼터파운더 치즈", "사장병 있음 (본인도 인정함)"),
        "ENTP": ("슈비 버거", "시작은 잘함, 끝은 모르겠음"),
        "INFJ": ("토마토 치즈 비프 버거", "내가 왜 이렇게 피곤하지...?"),
        "INFP": ("불고기 버거", "혼자 영화 보고 울고, 다시 보고 또 울고"),
        "ENFJ": ("빅맥", "다 괜찮다고 하면서 본인이 제일 힘듦"),
        "ENFP": ("맥스파이시 상하이 버거", "인생은 즉흥! 계획은 없어도 감성은 있음"),
        "ISTJ": ("맥치킨", "정리 안 돼 있으면 잠 못 잠"),
        "ISFJ": ("슈슈 버거", "남 챙기느라 본인 밥 식는 사람"),
        "ESTJ": ("더블 치즈버거", "이건 이렇게 해야 합니다 (강조함)"),  # 대체: 트리플 베이컨 치즈버거 → 더블 치즈버거
        "ESFJ": ("맥크리스피 클래식 버거", "친구 문제도 본인이 더 속상함"),
        "ISTP": ("더블 불고기 버거", "가만히 있다가 기계 다 고침"),
        "ISFP": ("치즈버거", "감성사진 폴더에만 3천장 있음"),
        "ESTP": ("맥크리스피 디럭스 버거", "지금 안 하면 죽을 것 같음"),
        "ESFP": ("더블 맥스파이시 상하이 버거", "나 지금 심심해 죽을 것 같음 ㅠㅠ")
    }

    burger = burger_results[mbti][0]
    label = burger_results[mbti][1]

    st.subheader("🍔 당신에게 어울리는 버거는 🍔")
    st.markdown(f"## **{burger}**")
    st.markdown(f"**성격 유형:** {label}")
    st.markdown(f"**MBTI 유형:** {mbti}")
   

    # ✅ 정확한 방식으로 영양정보 가져오기
    df['메뉴'] = df['메뉴'].str.strip()  # 공백 제거
    try:
        row = df.loc[df['메뉴'] == burger_results[mbti][0], ['칼로리(Kcal)', '단백질', '지방', '나트륨', '당류']]
        if not row.empty:
            values = row.iloc[0]
            fig, ax = plt.subplots()
            ax.bar(values.index, values.values, color="orange")
            ax.set_title(f"{burger} 영양성분 분석", fontproperties=font_prop)
            ax.set_ylabel("g / mg / kcal", fontproperties=font_prop)
            ax.set_xticklabels(values.index, fontproperties=font_prop)
            st.pyplot(fig)
        else:
            st.warning("⚠️ CSV에서 해당 버거의 영양정보를 찾을 수 없습니다.")
    except Exception as e:
        st.error(f"에러 발생: {e}")

    # 다시하기 버튼
    if st.button("🔄 다시 테스트하기"):
        st.session_state.page = 0
        st.session_state.answers = []
        for i in range(len(questions)):
            st.session_state.pop(f"q{i}", None)

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