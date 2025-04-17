# streamlit run code/macbti_test.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ✅ 한글 폰트 설정 (윈도우 기준, mac은 제거 가능)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ✅ 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "McDelivery Nutritional Information Table.csv"))
VOTE_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "vote_result.csv"))

# ✅ 데이터 로딩 함수
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
    df[['칼로리(Kcal)', '단백질', '지방', '나트륨', '당류']] = df[['칼로리(Kcal)', '단백질', '지방', '나트륨', '당류']].apply(pd.to_numeric, errors='coerce')
    return df

df = load_data()

# ✅ 타이틀
st.markdown("<h1 style='text-align:center;'>🍔 햄버거 챔피언스 리그: 영양 성분 배틀!</h1>", unsafe_allow_html=True)

# ✅ 카테고리 및 메뉴 선택
categories = df['카테고리'].dropna().unique()
selected_category = st.selectbox("🍽️ 비교할 카테고리를 선택하세요", categories)
filtered_df = df[df['카테고리'] == selected_category]
menu_options = filtered_df['메뉴'].unique()

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div style='text-align:left; font-weight:bold;'>왼쪽 메뉴</div>", unsafe_allow_html=True)
    menu1 = st.selectbox("", menu_options, key='menu1')

with col2:
    st.markdown("<div style='text-align:right; font-weight:bold;'>오른쪽 메뉴</div>", unsafe_allow_html=True)
    menu2 = st.selectbox("", menu_options, index=1 if len(menu_options) > 1 else 0, key='menu2')

# ✅ 비교할 항목
nutrients = ['칼로리(Kcal)', '단백질', '지방', '나트륨', '당류']
menu1_vals = filtered_df[filtered_df['메뉴'] == menu1][nutrients].values.flatten()
menu2_vals = filtered_df[filtered_df['메뉴'] == menu2][nutrients].values.flatten()

# ✅ 비교 그래프
x = np.arange(len(nutrients))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.barh(x - width/2, menu1_vals, height=width, label=menu1, color='skyblue')
bars2 = ax.barh(x + width/2, menu2_vals, height=width, label=menu2, color='lightcoral')

ax.set_yticks(x)
ax.set_yticklabels(nutrients)
ax.invert_yaxis()
ax.set_xlabel("영양 성분 수치")
ax.set_title(f"{menu1} vs {menu2} 비교")
ax.legend()

# ✅ 수치만 표시
for i, (v1, v2) in enumerate(zip(menu1_vals, menu2_vals)):
    ax.text(v1 + 1, i - width/2, f"{v1:.0f}", va='center', fontsize=10)
    ax.text(v2 + 1, i + width/2, f"{v2:.0f}", va='center', fontsize=10)

st.pyplot(fig)

# ====================================
# ✅ 투표 기능
# ====================================

st.markdown("---")
st.markdown("<h2 style='text-align:center;'>📢 당신의 메뉴에 투표하세요!</h2>", unsafe_allow_html=True)

# ✅ 투표 메뉴 선택
selected_vote_menu = st.selectbox("🗳️ 메뉴 투표하기", menu_options)

# ✅ 투표 버튼
if st.button("✅ 이 메뉴에 투표하기"):
    # 파일 없으면 생성
    if not os.path.exists(VOTE_PATH):
        pd.DataFrame(columns=["카테고리", "메뉴"]).to_csv(VOTE_PATH, index=False, encoding="utf-8-sig")

    vote_df = pd.read_csv(VOTE_PATH)
    new_vote = pd.DataFrame([[selected_category, selected_vote_menu]], columns=["카테고리", "메뉴"])
    vote_df = pd.concat([vote_df, new_vote], ignore_index=True)
    vote_df.to_csv(VOTE_PATH, index=False, encoding="utf-8-sig")

    st.success(f"'{selected_vote_menu}' 메뉴에 투표해주셔서 감사합니다!")

# ✅ 투표 결과 시각화
if os.path.exists(VOTE_PATH):
    vote_df = pd.read_csv(VOTE_PATH)

    st.markdown("### 🗳️ 현재 카테고리별 투표 현황")
    cat_votes = vote_df[vote_df["카테고리"] == selected_category]["메뉴"].value_counts()
    st.bar_chart(cat_votes)

    st.markdown("### 🏆 전체 인기 메뉴 TOP 5")
    top_votes = vote_df["메뉴"].value_counts().head(5)
    st.bar_chart(top_votes)