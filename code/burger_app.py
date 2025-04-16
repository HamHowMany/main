import streamlit as st
import pandas as pd

df = pd.read_csv("data/Mcdelivery_menu_prices_Kacl.csv")
df.columns = df.columns.str.strip()
df['칼로리(Kcal)'] = pd.to_numeric(df['칼로리(Kcal)'], errors='coerce')

st.title("🍔 햄버거 추천 웹사이트")
st.markdown("### 당신에게 딱 맞는 맥도날드 버거를 추천해드릴게요!")

col1, col2, col3 = st.columns(3)
with col1:
    gender = st.radio("성별", ("남", "여"))
with col2:
    height = st.number_input("신장 (cm)", min_value=100, max_value=250, value=170)
with col3:
    weight = st.number_input("체중 (kg)", min_value=30, max_value=200, value=65)

set_choice = st.radio("🍟 버거를 어떤 방식으로 추천받고 싶나요?", ("단품", "세트"))

if gender == "남":
    bmr = 10 * weight + 6.25 * height - 5 * 25 + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * 25 - 161

total_kcal = round(bmr * 1.2)
st.success(f"📊 일일 권장 섭취량은 약 **{total_kcal} kcal** 입니다.")

burger_df = df[df['카테고리'].str.contains("버거")].copy()

if set_choice == "단품":
    burger_df['칼로리당_가격'] = burger_df['가격'] / burger_df['칼로리(Kcal)']
    burger_df_sorted = burger_df.sort_values('칼로리당_가격')
    best = burger_df_sorted.iloc[0]

    st.subheader("🍔 단품 기준 가성비 최고의 버거 추천")
    st.markdown(f"""
    - **메뉴:** {best['메뉴']}
    - **가격:** {best['가격']}원
    - **칼로리:** {best['칼로리(Kcal)']} kcal
    - **칼로리당 가격:** {best['칼로리당_가격']:.2f} 원/kcal
    """)

else:
    fries = df[df['메뉴'].str.contains('후렌치 후라이', na=False)].iloc[0]
    drink = df[df['카테고리'].str.contains('음료')].iloc[0]

    burger_df['총칼로리'] = burger_df['칼로리(Kcal)'] + fries['칼로리(Kcal)'] + drink['칼로리(Kcal)']
    burger_df['칼로리당_가격'] = burger_df['가격'] / burger_df['총칼로리']
    burger_df_sorted = burger_df.sort_values('칼로리당_가격')
    best = burger_df_sorted.iloc[0]

    st.subheader("🍟 세트 기준 가성비 최고의 버거 추천")
    st.markdown(f"""
    - **메뉴:** {best['메뉴']} + {fries['메뉴']} + {drink['메뉴']}
    - **총 칼로리:** {best['총칼로리']} kcal
    - **가격:** {best['가격']}원
    - **칼로리당 가격:** {best['칼로리당_가격']:.2f} 원/kcal
    """)
