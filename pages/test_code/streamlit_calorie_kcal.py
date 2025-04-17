import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# 🔐 API 키 불러오기
load_dotenv()
APP_ID = os.getenv("NUTRITIONIX_APP_ID")
APP_KEY = os.getenv("NUTRITIONIX_APP_KEY")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("../../data/Mcdelivery_menu_prices_Kacl.csv")
    df['가격'] = df['가격'].astype(str).str.replace(",", "").astype(int)
    df['칼로리(Kcal)'] = df['칼로리(Kcal)'].astype(str).str.replace(r"[^\d.]", "", regex=True)
    df['칼로리(Kcal)'] = pd.to_numeric(df['칼로리(Kcal)'], errors='coerce')
    df = df.dropna(subset=['칼로리(Kcal)'])
    return df

# 칼로리 소모량 계산 함수
def get_burn_rate(exercise_query, profile):
    url = "https://trackapi.nutritionix.com/v2/natural/exercise"
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": APP_KEY,
        "Content-Type": "application/json"
    }
    query = {
        "query": f"{exercise_query} 30 minutes",
        **profile
    }
    response = requests.post(url, json=query, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("exercises"):
            kcal = data["exercises"][0]["nf_calories"]
            minutes = data["exercises"][0]["duration_min"]
            return kcal / minutes
    return None

# UI 구성
st.title("🍔 섭취 칼로리 → 운동 시간 계산기")
st.caption("메뉴를 선택하고, 각각의 운동 기준으로 얼마나 해야 칼로리를 소모할 수 있는지 확인해보세요!")

# 사용자 정보 입력
col1, col2 = st.columns(2)
with col1:
    gender = st.radio("성별", ["남성", "여성"])
    age = st.number_input("나이", min_value=10, max_value=100, value=25)
with col2:
    weight = st.number_input("체중 (kg)", min_value=30, max_value=150, value=70)
    height = st.number_input("신장 (cm)", min_value=100, max_value=220, value=175)

user_profile = {
    "gender": gender,
    "age": int(age),
    "weight_kg": float(weight),
    "height_cm": float(height)
}

# 데이터 로딩
df = load_data()
burger_list = df[df['카테고리'] == "버거 & 세트"]['메뉴'].tolist()
drink_list = df[df['카테고리'].str.contains("음료", na=False)]['메뉴'].tolist()
side_list = df[df['카테고리'].str.contains("사이드", na=False)]['메뉴'].tolist()
dessert_list = df[df['카테고리'].str.contains("디저트", na=False)]['메뉴'].tolist()

# 메뉴 선택
st.subheader("🍟 메뉴 선택")
selected_burger = st.selectbox("단품 메뉴", ["(선택 안 함)"] + burger_list)
selected_drink = st.selectbox("음료 메뉴", ["(선택 안 함)"] + drink_list)
selected_side = st.selectbox("사이드 메뉴", ["(선택 안 함)"] + side_list)
selected_dessert = st.selectbox("디저트 메뉴", ["(선택 안 함)"] + dessert_list)

# 총 칼로리 계산
total_kcal = 0
selected_items = []

for item in [selected_burger, selected_drink, selected_side, selected_dessert]:
    if item and item != "(선택 안 함)":
        row = df[df['메뉴'] == item]
        if not row.empty:
            kcal = row.iloc[0]['칼로리(Kcal)']
            total_kcal += kcal
            selected_items.append((item, kcal))

# 운동 종류
exercise_map = {
    "걷기": "walking",
    "달리기": "running",
    "자전거": "bicycling",
    "수영": "swimming"
}

# 결과 출력
if selected_items:
    st.markdown("### 🍽️ 선택한 음식")
    for name, kcal in selected_items:
        st.write(f"- {name}: {kcal:.0f} kcal")
    st.write(f"🔢 **총 섭취 칼로리: {total_kcal:.0f} kcal**")

    st.markdown("### 🏃 운동별 소모 시간")
    results = []

    for kr_name, eng_query in exercise_map.items():
        burn_per_min = get_burn_rate(eng_query, user_profile)
        if burn_per_min:
            required_time = total_kcal / burn_per_min
            results.append((kr_name, burn_per_min, required_time))
        else:
            results.append((kr_name, None, None))

    for ex_name, burn, minutes in results:
        if burn:
            st.write(f"✅ **{ex_name}**: 1분당 {burn:.2f} kcal → 약 **{minutes:.1f}분** 필요")
        else:
            st.write(f"❌ {ex_name}: 계산 실패 (API 응답 없음)")
else:
    st.info("메뉴를 선택하면 총 칼로리와 운동 시간이 계산됩니다.")