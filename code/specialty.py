#streamlit run code/specialty.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import streamlit as st
import os

# 데이터 로드 함수
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "McDelivery Nutritional Information Table.csv"))

    try:
        df = pd.read_csv(DATA_PATH)
        df.columns = df.columns.str.strip()  # 공백 제거
        print("✅ 데이터 로드 성공!")
        print("📌 컬럼명:", df.columns.tolist())
    except Exception as e:
        print(f"❌ 데이터 로드 실패: {e}")
        df = pd.DataFrame()

    return df

# 추천 함수 (한글 컬럼명 사용)
def recommend_menu(df, preferences):
    df = df[
        (df['칼로리(Kcal)'] >= preferences['min_calories']) &
        (df['칼로리(Kcal)'] <= preferences['max_calories']) &
        (df['단백질'] >= preferences['min_protein']) &
        (df['단백질'] <= preferences['max_protein']) &
        (df['지방'] >= preferences['min_fat']) &
        (df['지방'] <= preferences['max_fat']) &
        (df['나트륨'] >= preferences['min_sodium']) &
        (df['나트륨'] <= preferences['max_sodium'])
    ]

    if preferences['excluded_categories']:
        df = df[~df['카테고리'].isin(preferences['excluded_categories'])]

    nutrients = ['칼로리(Kcal)', '단백질', '지방', '나트륨']
    scaler = MinMaxScaler()
    df[nutrients] = scaler.fit_transform(df[nutrients])

    df['점수'] = (
        preferences['weight_calories'] * (1 - df['칼로리(Kcal)']) +
        preferences['weight_protein'] * df['단백질'] +
        preferences['weight_fat'] * (1 - df['지방']) +
        preferences['weight_sodium'] * (1 - df['나트륨'])
    )

    if preferences['budget'] > 0:
        df = df[df['가격'] <= preferences['budget']]

    recommended = df.sort_values('점수', ascending=False).head(preferences['num_recommendations'])

    return recommended[['메뉴', '카테고리', '가격', '칼로리(Kcal)', '단백질', '지방', '나트륨', '점수']]

# Streamlit UI
def main():
    st.title("🍔 맥도날드 메뉴 추천 시스템")

    df = load_data()

    st.sidebar.header("사용자 선호도 설정")
    st.sidebar.subheader("영양소 범위 설정")

    min_calories, max_calories = st.sidebar.slider("칼로리 범위 (kcal)", 0, int(df['칼로리(Kcal)'].max()) if not df.empty else 1000, (200, 800))
    min_protein, max_protein = st.sidebar.slider("단백질 범위 (g)", 0, int(df['단백질'].max()) if not df.empty else 50, (10, 30))
    min_fat, max_fat = st.sidebar.slider("지방 범위 (g)", 0, int(df['지방'].max()) if not df.empty else 50, (5, 25))
    min_sodium, max_sodium = st.sidebar.slider("나트륨 범위 (mg)", 0, int(df['나트륨'].max()) if not df.empty else 2000, (200, 1000))

    st.sidebar.subheader("영양소 중요도")
    weight_calories = st.sidebar.slider("칼로리 중요도", 0.0, 1.0, 0.3, 0.1)
    weight_protein = st.sidebar.slider("단백질 중요도", 0.0, 1.0, 0.4, 0.1)
    weight_fat = st.sidebar.slider("지방 중요도", 0.0, 1.0, 0.3, 0.1)
    weight_sodium = st.sidebar.slider("나트륨 중요도", 0.0, 1.0, 0.2, 0.1)

    st.sidebar.subheader("기타 설정")
    budget = st.sidebar.number_input("예산 (원)", 0, value=10000)
    num_recommendations = st.sidebar.slider("추천 수", 1, 10, 3)
    excluded_categories = st.sidebar.multiselect("제외할 카테고리", df['카테고리'].unique() if not df.empty else [])

    preferences = {
        'min_calories': min_calories, 'max_calories': max_calories,
        'min_protein': min_protein, 'max_protein': max_protein,
        'min_fat': min_fat, 'max_fat': max_fat,
        'min_sodium': min_sodium, 'max_sodium': max_sodium,
        'weight_calories': weight_calories, 'weight_protein': weight_protein,
        'weight_fat': weight_fat, 'weight_sodium': weight_sodium,
        'budget': budget, 'num_recommendations': num_recommendations,
        'excluded_categories': excluded_categories
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

                st.subheader("📊 영양 성분 비교")
                chart_data = recommended.set_index('메뉴')[['칼로리(Kcal)', '단백질', '지방']]
                st.bar_chart(chart_data)

if __name__ == "__main__":
    main()