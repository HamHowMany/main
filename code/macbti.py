# streamlit run code/macbti_test.py
import streamlit as st
import pandas as pd
import random
import os

def run():
    st.header("✨ 맥비티아이 테스트")
    st.markdown("16개의 질문에 답하고 당신의 성향에 맞는 맥도날드 메뉴를 추천받아보세요!")

    # 질문 리스트 (각 MBTI 성향에 4문항씩)
    questions = {
        "EI": [
            ("혼자 있는 시간이 편하다", "사람들과 함께 있는 것이 즐겁다"),
            ("깊은 대화가 좋다", "여러 사람과 가볍게 이야기하는 것이 좋다"),
            ("생각이 많은 편이다", "즉시 말로 표현하는 게 좋다"),
            ("혼자 있는 시간이 필요하다", "바쁘게 지내는 걸 좋아한다")
        ],
        "SN": [
            ("현실적인 편이다", "상상력이 풍부한 편이다"),
            ("현재에 집중하는 편이다", "미래를 자주 상상한다"),
            ("사실 위주로 판단한다", "아이디어와 가능성을 본다"),
            ("실용적인 것이 좋다", "창의적인 것이 좋다")
        ],
        "TF": [
            ("결정을 감정으로 내린다", "결정을 논리로 내린다"),
            ("상대방의 기분을 우선한다", "공정함이 더 중요하다"),
            ("배려하는 것이 중요하다", "효율적인 것이 더 중요하다"),
            ("사람이 먼저다", "원칙이 먼저다")
        ],
        "JP": [
            ("계획 세우는 걸 좋아한다", "즉흥적인 걸 좋아한다"),
            ("일정을 미리 정해둔다", "상황에 맞게 유동적으로 움직인다"),
            ("정해진 계획대로 해야 편하다", "그때그때 즉흥적으로 하는 게 좋다"),
            ("체계적인 걸 선호한다", "자유로운 게 좋다")
        ]
    }

    mbti_score = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

    st.markdown("#### 질문에 응답해주세요")
    for dimension, q_list in questions.items():
        for i, (a, b) in enumerate(q_list):
            answer = st.radio(f"{dimension}-{i+1}.", [a, b], key=f"{dimension}-{i}")
            if answer == a:
                mbti_score[dimension[0]] += 1
            else:
                mbti_score[dimension[1]] += 1

    # 결과 계산
    mbti = ""
    mbti += "E" if mbti_score["E"] > mbti_score["I"] else "I"
    mbti += "S" if mbti_score["S"] > mbti_score["N"] else "N"
    mbti += "T" if mbti_score["T"] > mbti_score["F"] else "F"
    mbti += "J" if mbti_score["J"] > mbti_score["P"] else "P"

    st.markdown("---")
    st.subheader("🧠 당신의 맥비티아이 결과는...")
    st.markdown(f"### 🌟 `{mbti}` 유형입니다!")

    # 메뉴 추천 함수
    def recommend_menu_by_mbti(df, mbti):
        df = df.copy()
        df.columns = df.columns.str.strip()

        # 숫자형 변환
        df["칼로리(Kcal)"] = pd.to_numeric(df["칼로리(Kcal)"], errors='coerce')
        df["단백질"] = pd.to_numeric(df["단백질"], errors='coerce')
        df["지방"] = pd.to_numeric(df["지방"], errors='coerce')
        df["나트륨"] = pd.to_numeric(df["나트륨"], errors='coerce')
        df["당류"] = pd.to_numeric(df["당류"], errors='coerce')
        df["가격"] = pd.to_numeric(df["가격"], errors='coerce')

        if mbti in ["ENFP", "ENTP"]:
            return "🔥 개성 강한 당신을 위한 강렬한 메뉴들!", df[df["칼로리(Kcal)"] > 700].sample(5)

        elif mbti in ["ISTJ", "ISFJ"]:
            classic_keywords = ["빅맥", "쿼터파운더", "1955"]
            return "👑 전통을 사랑하는 당신께 클래식 메뉴를 추천!", df[df["메뉴"].str.contains("|".join(classic_keywords), na=False)].sample(3)

        elif mbti in ["INFP", "INFJ"]:
            return "🌱 감성적인 당신께 어울리는 가벼운 메뉴들!", df[(df["칼로리(Kcal)"] < 500) & (df["당류"] <= 10)].sample(5)

        elif mbti in ["ESTP", "ESFP"]:
            return "💪 에너지 넘치는 당신께 고단백 메뉴를!", df[(df["칼로리(Kcal)"] > 600) & (df["단백질"] > 20)].sample(5)

        elif mbti in ["ENTJ", "INTJ"]:
            df["단백질당칼로리"] = df["칼로리(Kcal)"] / df["단백질"]
            return "📊 효율을 중시하는 당신께 최고의 단백질 대비 칼로리 메뉴!", df.sort_values("단백질당칼로리").head(5)

        elif mbti in ["ISTP", "INTP"]:
            df["칼로리당가격"] = df["가격"] / df["칼로리(Kcal)"]
            return "💸 실용적인 당신을 위한 가성비 메뉴!", df.sort_values("칼로리당가격").head(5)

        elif mbti in ["ESFJ", "ENFJ"]:
            return "⚖️ 균형과 조화를 중요시하는 당신께 저지방 저나트륨 메뉴!", df[(df["나트륨"] < 1000) & (df["지방"] < 10)].sample(5)

        elif mbti in ["ISFP", "ISFJ"]:
            return "🎀 조용하고 감성적인 그대를 위한 부드러운 메뉴~", df[(df["가격"] < 6000) & (df["당류"] < 12)].sample(5)

        else:
            return "🎲 랜덤 추천 메뉴!", df.sample(5)

    # CSV 로딩 및 추천
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # code/ 기준
        DATA_PATH = os.path.join(BASE_DIR, "..", "data", "McDelivery Nutritional Information Table.csv")
        DATA_PATH = os.path.abspath(DATA_PATH)  # 윈도우 경로 정리용
        df = pd.read_csv(DATA_PATH)

        # 추천 실행
        message, recommended = recommend_menu_by_mbti(df, mbti)

        with st.expander("🍔 추천 메뉴를 확인하려면 클릭하세요!"):
            st.success(message)
            st.dataframe(recommended[["메뉴", "칼로리(Kcal)", "단백질", "지방", "나트륨", "당류", "가격"]])

    except Exception as e:
        st.error(f"❌ 메뉴 파일을 불러오는 데 실패했습니다: {e}")

    if st.button("🔙 홈으로 돌아가기"):
        st.session_state.page = 'home'
