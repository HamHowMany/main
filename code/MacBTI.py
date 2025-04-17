#streamlit run code/MacBTI.py

import streamlit as st

st.set_page_config(page_title="🍔 나의 MacBTI는?", layout="centered")
st.title("🍔 당신의 버거 성격유형을 알아보세요!")
st.write("아래 질문에 답하면, 당신에게 어울리는 맥도날드 버거를 추천해드립니다!")

# 질문 목록
questions = [
    {
        "question": "Q1. 새로운 메뉴를 봤을 때, 당신은?",
        "options": ["A. 일단 도전! 새로운 조합 좋아해요.", "B. 익숙한 메뉴가 좋아요. 늘 먹던 거로 만족해요."]
    },
    {
        "question": "Q2. 나의 식사 스타일은?",
        "options": ["A. 바쁘고 효율적으로! 칼로리와 영양 따지며 먹어요.", "B. 분위기와 감성도 중요해요. 맛있는 걸 천천히 즐겨요."]
    },
    {
        "question": "Q3. 사람들과 있을 때 나는?",
        "options": ["A. 분위기 메이커! 같이 먹는 재미를 즐겨요.", "B. 조용히 나만의 시간을 즐겨요. 혼밥도 괜찮아요."]
    },
    {
        "question": "Q4. ‘버거’에 대해 더 중요하다고 생각하는 건?",
        "options": ["A. 맛과 식감! 맛있으면 열량은 생각 안 해요.", "B. 구성과 영양! 단백질, 열량, 나트륨 따져요."]
    },
    {
        "question": "Q5. 당신이 꿈꾸는 이상적인 식사는?",
        "options": ["A. 색다른 재료 조합과 경험이 있는 메뉴!", "B. 전통 있고 정돈된 맛, 깔끔한 구성!"]
    },
    {
        "question": "Q6. 당신은 평소 어떤 유형에 가까운가요?",
        "options": ["A. 열정적이고 에너지 넘치며 즉흥적인 편", "B. 신중하고 계획적이며 관찰하는 편"]
    },
]

# 답변 수집
answers = []
for i, q in enumerate(questions):
    answer = st.radio(q["question"], q["options"], key=f"q{i}")
    answers.append(answer[0])  # 'A' 또는 'B' 저장

# 제출 버튼
if st.button("🔍 결과 보기"):
    a_count = answers.count('A')
    b_count = answers.count('B')

    # 매우 간단한 분류 논리: A가 많으면 활동적/열정적, B가 많으면 안정적/계획적
    if a_count >= 5:
        burger = "트리플 치즈버거"
        personality = "🔥 도전과 열정을 즐기는 실행가형"
        desc = "압도적인 단백질과 중량! 당신은 인생에서도 강력한 존재감을 발휘하는 리더예요."
    elif b_count >= 5:
        burger = "불고기 버거"
        personality = "🌿 전통을 중시하는 감성 실용가형"
        desc = "당신은 따뜻하고 안정적인 사람. 익숙하고 편안한 버거가 잘 어울려요."
    elif a_count == b_count:
        burger = "빅맥"
        personality = "⚖️ 모두와 잘 어울리는 조화형"
        desc = "적절한 균형과 센스를 갖춘 당신, 국민버거 빅맥이 딱이죠!"
    elif a_count > b_count:
        burger = "맥스파이시 상하이 버거"
        personality = "🌶 외향적이고 매운 자극을 즐기는 모험가형"
        desc = "항상 에너지 넘치고 도전적인 당신! 매콤한 버거가 찰떡이에요."
    else:
        burger = "맥치킨"
        personality = "🧊 담백하고 실속 있는 현실주의자형"
        desc = "조용하지만 확실한 실속파인 당신에겐 맥치킨이 가장 잘 어울려요."

    st.subheader(f"🍔 당신에게 어울리는 버거는: {burger}!")
    st.markdown(f"**성격 유형:** {personality}")
    st.info(desc)
