# streamlit run code/specialty.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import os
import platform
from sklearn.preprocessing import MinMaxScaler

# 운영체제별 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux (ex. Streamlit Cloud or Ubuntu)
    plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False


# ✅ 데이터 로드 함수
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.abspath(
        os.path.join(BASE_DIR, "..", "data", "McDelivery Nutritional Information Table.csv")
    )

    try:
        df = pd.read_csv(DATA_PATH)
        df.columns = df.columns.str.strip()  # 컬럼명 공백 제거
        column_mapping = {
            "매뉴얼": "메뉴",
            "컬로리(Kcal)": "칼로리(Kcal)",
        }
        df = df.rename(columns=column_mapping)
        print("✅ 데이터 로드 성공!")
        print("📌 컬럼명:", df.columns.tolist())
    except Exception as e:
        print(f"❌ 데이터 로드 실패: {e}")
        df = pd.DataFrame()

    return df


# ✅ 추천 함수
def recommend_menu(df, preferences):
    # 필터링
    filtered_df = df[
        (df["칼로리(Kcal)"] >= preferences["min_calories"]) &
        (df["칼로리(Kcal)"] <= preferences["max_calories"]) &
        (df["단백질"] >= preferences["min_protein"]) &
        (df["단백질"] <= preferences["max_protein"]) &
        (df["지방"] >= preferences["min_fat"]) &
        (df["지방"] <= preferences["max_fat"]) &
        (df["나트륨"] >= preferences["min_sodium"]) &
        (df["나트륨"] <= preferences["max_sodium"])
    ].copy()

    if preferences["excluded_categories"]:
        filtered_df = filtered_df[~filtered_df["카테고리"].isin(preferences["excluded_categories"])]

    # 정규화용 원본 보존
    original_nutrients = filtered_df[["칼로리(Kcal)", "단백질", "지방", "나트륨"]].copy()

    # 정규화
    nutrients = ["칼로리(Kcal)", "단백질", "지방", "나트륨"]
    scaler = MinMaxScaler()
    filtered_df[nutrients] = scaler.fit_transform(filtered_df[nutrients])

    # 점수 계산
    filtered_df["점수"] = (
        preferences["weight_calories"] * (1 - filtered_df["칼로리(Kcal)"]) +
        preferences["weight_protein"] * filtered_df["단백질"] +
        preferences["weight_fat"] * (1 - filtered_df["지방"]) +
        preferences["weight_sodium"] * (1 - filtered_df["나트륨"])
    )

    # 예산 조건
    if preferences["budget"] > 0:
        filtered_df = filtered_df[filtered_df["가격"] <= preferences["budget"]]

    recommended = filtered_df.sort_values("점수", ascending=False).head(preferences["num_recommendations"])

    # 원본 영양소 값 복원
    recommended[["칼로리(Kcal)", "단백질", "지방", "나트륨"]] = original_nutrients.loc[recommended.index]

    return recommended[["메뉴", "카테고리", "가격", "칼로리(Kcal)", "단백질", "지방", "나트륨", "점수"]]


# ✅ 메인 실행 함수
def run():
    st.title("🍔 맥도날드 메뉴 추천 시스템")

    df = load_data()

    st.sidebar.header("사용자 선호도 설정")
    st.sidebar.subheader("영양소 범위 설정")

    min_calories, max_calories = st.sidebar.slider(
        "칼로리 범위 (kcal)",
        0,
        int(df["칼로리(Kcal)"].max()) if not df.empty else 1000,
        (200, 800),
    )
    min_protein, max_protein = st.sidebar.slider(
        "단백질 범위 (g)", 0, int(df["단백질"].max()) if not df.empty else 50, (10, 30)
    )
    min_fat, max_fat = st.sidebar.slider(
        "지방 범위 (g)", 0, int(df["지방"].max()) if not df.empty else 50, (5, 25)
    )
    min_sodium, max_sodium = st.sidebar.slider(
        "나트륨 범위 (mg)", 0, int(df["나트륨"].max()) if not df.empty else 2000, (200, 1000)
    )

    st.sidebar.subheader("영양소 중요도")
    weight_calories = st.sidebar.slider("칼로리 중요도", 0.0, 1.0, 0.3, 0.1)
    weight_protein = st.sidebar.slider("단백질 중요도", 0.0, 1.0, 0.4, 0.1)
    weight_fat = st.sidebar.slider("지방 중요도", 0.0, 1.0, 0.3, 0.1)
    weight_sodium = st.sidebar.slider("나트륨 중요도", 0.0, 1.0, 0.2, 0.1)

    st.sidebar.subheader("기타 설정")
    budget = st.sidebar.number_input("예산 (원)", 0, value=10000, step=100)
    num_recommendations = st.sidebar.slider("추천 수", 1, 10, 3)
    excluded_categories = st.sidebar.multiselect(
        "제외할 카테고리", df["카테고리"].unique() if not df.empty else []
    )

    preferences = {
        "min_calories": min_calories,
        "max_calories": max_calories,
        "min_protein": min_protein,
        "max_protein": max_protein,
        "min_fat": min_fat,
        "max_fat": max_fat,
        "min_sodium": min_sodium,
        "max_sodium": max_sodium,
        "weight_calories": weight_calories,
        "weight_protein": weight_protein,
        "weight_fat": weight_fat,
        "weight_sodium": weight_sodium,
        "budget": budget,
        "num_recommendations": num_recommendations,
        "excluded_categories": excluded_categories,
    }

    if st.button("메뉴 추천 받기"):
        if df.empty:
            st.warning("데이터를 불러오는 데 실패했습니다.")
        else:
            recommended = recommend_menu(df, preferences)
            if recommended.empty:
                st.warning("조건에 맞는 메뉴가 없습니다.")
            else:
                st.subheader("🥇 추천 메뉴")
                st.dataframe(recommended)

                # 📊 가격 시각화
                st.subheader("📊 가격 비교 (가로 막대 그래프)")
                fig1, ax1 = plt.subplots(figsize=(13, 6))
                ax1.barh(recommended["메뉴"], recommended["가격"], color="skyblue")
                ax1.set_xlabel("가격 (원)")
                ax1.set_ylabel("메뉴")
                ax1.set_title("가격 비교")
                for i, (value, name) in enumerate(zip(recommended["가격"], recommended["메뉴"])):
                    ax1.text(value + 0, i, f"{value:,}원", va="center")
                st.pyplot(fig1)

                # 📊 영양소 시각화
                st.subheader("📊 주요 영양소 비교 (칼로리, 단백질, 지방)")
                nutrients = recommended[["메뉴", "칼로리(Kcal)", "단백질", "지방"]].set_index("메뉴")
                fig2, ax2 = plt.subplots(figsize=(10, 6))
                nutrients.plot(kind="barh", ax=ax2)
                ax2.set_xlabel("영양 성분 수치")
                ax2.set_ylabel("메뉴")
                ax2.set_title("영양 성분 비교 (정수값)")
                ax2.legend(title="영양소", loc="center left", bbox_to_anchor=(1.0, 0.5))
                for bars in ax2.containers:
                    ax2.bar_label(bars, fmt="%d", label_type="edge", padding=3)
                st.pyplot(fig2)

                # 📋 영양소 표
                st.markdown("**🔎 영양 성분 상세 (정수값)**")
                st.table(nutrients)

    # ✅ 홈으로 돌아가기 버튼
    st.markdown("---")
    if st.button("🏠 홈으로 돌아가기"):
        st.session_state.page = "home"
        st.rerun()


# 실행 진입점
if __name__ == "__main__":
    run()