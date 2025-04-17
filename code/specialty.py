#streamlit run code/specialty.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import streamlit as st

# 데이터 로드 함수
def load_data():
    try:
        # 영양 정보 데이터 로드 (파일명이 잘려서 정확한 이름을 확인해야 합니다)
        nutrition_df = pd.read_excel("McDelivery Nutritional Information Ta....xlsx")  # 확장자 수정 필요
    except:
        nutrition_df = pd.read_csv("McDelivery Nutritional Information Table.csv")  # CSV 버전 시도
    
    # 가격 정보 데이터 로드
    price_df = pd.read_csv("Medelivery_menu_prices_kad.csv")
    
    # 두 데이터프레임 병합
    merged_df = pd.merge(nutrition_df, price_df, on="Menu Item", how="inner")
    return merged_df

# 사용자 선호도 기반 추천 함수
def recommend_menu(df, preferences):
    # 영양소 범위 필터링
    df = df[
        (df['Calories'] >= preferences['min_calories']) &
        (df['Calories'] <= preferences['max_calories']) &
        (df['Protein (g)'] >= preferences['min_protein']) &
        (df['Protein (g)'] <= preferences['max_protein']) &
        (df['Carbohydrates (g)'] >= preferences['min_carbs']) &
        (df['Carbohydrates (g)'] <= preferences['max_carbs']) &
        (df['Total Fat (g)'] >= preferences['min_fat']) &
        (df['Total Fat (g)'] <= preferences['max_fat']) &
        (df['Sodium (mg)'] >= preferences['min_sodium']) &
        (df['Sodium (mg)'] <= preferences['max_sodium'])
    ]
    
    # 필터링: 사용자가 원하지 않는 카테고리 제외
    if preferences['excluded_categories']:
        df = df[~df['Category'].isin(preferences['excluded_categories'])]
    
    # 영양소 점수 계산
    nutrients = ['Calories', 'Protein (g)', 'Carbohydrates (g)', 'Total Fat (g)', 'Sodium (mg)']
    
    # MinMax 스케일링
    scaler = MinMaxScaler()
    df[nutrients] = scaler.fit_transform(df[nutrients])
    
    # 점수 계산 (사용자 가중치 적용)
    df['Score'] = (
        preferences['weight_calories'] * (1 - df['Calories']) +  # 칼로리는 낮을수록 좋음
        preferences['weight_protein'] * df['Protein (g)'] +
        preferences['weight_carbs'] * (1 - df['Carbohydrates (g)']) +  # 탄수화물은 낮을수록 좋음
        preferences['weight_fat'] * (1 - df['Total Fat (g)']) +  # 지방은 낮을수록 좋음
        preferences['weight_sodium'] * (1 - df['Sodium (mg)'])  # 나트륨은 낮을수록 좋음
    )
    
    # 가격 고려 (예산 내에서)
    if preferences['budget'] > 0:
        df = df[df['Price'] <= preferences['budget']]
    
    # 점수 기준 정렬
    recommended = df.sort_values('Score', ascending=False).head(preferences['num_recommendations'])
    return recommended[['Menu Item', 'Category', 'Price', 'Calories', 'Protein (g)', 'Carbohydrates (g)', 'Total Fat (g)', 'Sodium (mg)', 'Score']]

# Streamlit 앱 인터페이스
def main():
    st.title("🍔 맥도날드 영양성분 기반 메뉴 추천 시스템")
    
    # 데이터 로드
    df = load_data()
    
    # 사용자 선호도 입력
    st.sidebar.header("사용자 선호도 설정")
    
    # 영양소 범위 설정 섹션
    st.sidebar.subheader("영양소 범위 설정")
    
    # 각 영양소별 최소/최대값 슬라이더
    min_calories, max_calories = st.sidebar.slider(
        "칼로리 범위 (kcal)",
        min_value=0,
        max_value=int(df['Calories'].max()) if not df.empty else 1000,
        value=(200, 800)
    )
    
    min_protein, max_protein = st.sidebar.slider(
        "단백질 범위 (g)",
        min_value=0,
        max_value=int(df['Protein (g)'].max()) if not df.empty else 50,
        value=(10, 30)
    )
    
    min_carbs, max_carbs = st.sidebar.slider(
        "탄수화물 범위 (g)",
        min_value=0,
        max_value=int(df['Carbohydrates (g)'].max()) if not df.empty else 100,
        value=(20, 60)
    )
    
    min_fat, max_fat = st.sidebar.slider(
        "지방 범위 (g)",
        min_value=0,
        max_value=int(df['Total Fat (g)'].max()) if not df.empty else 50,
        value=(5, 25)
    )
    
    min_sodium, max_sodium = st.sidebar.slider(
        "나트륨 범위 (mg)",
        min_value=0,
        max_value=int(df['Sodium (mg)'].max()) if not df.empty else 2000,
        value=(200, 1000)
    )
    
    # 영양소 가중치 섹션
    st.sidebar.subheader("영양소 중요도")
    weight_calories = st.sidebar.slider("칼로리 중요도 (낮을수록 좋음)", 0.0, 1.0, 0.3, step=0.1)
    weight_protein = st.sidebar.slider("단백질 중요도 (높을수록 좋음)", 0.0, 1.0, 0.4, step=0.1)
    weight_carbs = st.sidebar.slider("탄수화물 중요도 (낮을수록 좋음)", 0.0, 1.0, 0.2, step=0.1)
    weight_fat = st.sidebar.slider("지방 중요도 (낮을수록 좋음)", 0.0, 1.0, 0.3, step=0.1)
    weight_sodium = st.sidebar.slider("나트륨 중요도 (낮을수록 좋음)", 0.0, 1.0, 0.2, step=0.1)
    
    # 기타 설정
    st.sidebar.subheader("기타 설정")
    budget = st.sidebar.number_input("예산 (원)", min_value=0, value=10000)
    num_recommendations = st.sidebar.slider("추천 메뉴 수", 1, 10, 3)
    excluded_categories = st.sidebar.multiselect("제외할 메뉴 카테고리", df['Category'].unique() if not df.empty else [])
    
    preferences = {
        'min_calories': min_calories,
        'max_calories': max_calories,
        'min_protein': min_protein,
        'max_protein': max_protein,
        'min_carbs': min_carbs,
        'max_carbs': max_carbs,
        'min_fat': min_fat,
        'max_fat': max_fat,
        'min_sodium': min_sodium,
        'max_sodium': max_sodium,
        'weight_calories': weight_calories,
        'weight_protein': weight_protein,
        'weight_carbs': weight_carbs,
        'weight_fat': weight_fat,
        'weight_sodium': weight_sodium,
        'budget': budget,
        'num_recommendations': num_recommendations,
        'excluded_categories': excluded_categories
    }
    
    # 추천 실행
    if st.button("메뉴 추천 받기"):
        if df.empty:
            st.warning("데이터를 불러오는 데 문제가 발생했습니다. 파일 경로를 확인해주세요.")
        else:
            recommended = recommend_menu(df, preferences)
            
            if recommended.empty:
                st.warning("조건에 맞는 메뉴를 찾을 수 없습니다. 필터 조건을 완화해주세요.")
            else:
                st.subheader("추천 메뉴")
                st.dataframe(recommended)
                
                # 시각화
                st.subheader("영양 성분 비교")
                chart_data = recommended.set_index('Menu Item')[['Calories', 'Protein (g)', 'Carbohydrates (g)', 'Total Fat (g)']]
                st.bar_chart(chart_data)

if __name__ == "__main__":
    main()