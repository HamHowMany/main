# streamlit run code/vote_test.py
import streamlit as st

# ✅ 가장 먼저 호출
st.set_page_config(page_title="🍔 메뉴 투표 테스트", layout="centered")

import pandas as pd
import os

# ✅ 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "McDelivery Nutritional Information Table.csv"))
VOTE_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "vote_result.csv"))

# ✅ 데이터 로딩
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
    return df

df = load_data()

st.markdown("<h1 style='text-align:center;'>🗳️ 메뉴 투표하기</h1>", unsafe_allow_html=True)

# ✅ 세션 상태 초기화
if 'voted_categories' not in st.session_state:
    st.session_state.voted_categories = []

# ✅ 카테고리 및 메뉴 선택
categories = df['카테고리'].dropna().unique()
selected_category = st.selectbox("카테고리를 선택하세요", categories)
filtered_df = df[df['카테고리'] == selected_category]
menu_options = filtered_df['메뉴'].unique()
selected_menu = st.selectbox("투표할 메뉴를 선택하세요", menu_options)

# ✅ 투표 버튼
if st.button("✅ 이 메뉴에 투표하기"):
    if selected_category in st.session_state.voted_categories:
        st.warning(f"'{selected_category}' 카테고리는 이미 투표하셨습니다. 다른 카테고리를 선택해 주세요.")
    else:
        if not os.path.exists(VOTE_PATH):
            pd.DataFrame(columns=["카테고리", "메뉴"]).to_csv(VOTE_PATH, index=False, encoding="utf-8-sig")

        vote_df = pd.read_csv(VOTE_PATH)
        new_vote = pd.DataFrame([[selected_category, selected_menu]], columns=["카테고리", "메뉴"])
        vote_df = pd.concat([vote_df, new_vote], ignore_index=True)
        vote_df.to_csv(VOTE_PATH, index=False, encoding="utf-8-sig")

        st.session_state.voted_categories.append(selected_category)
        st.success(f"'{selected_menu}' 메뉴에 투표해주셔서 감사합니다! 🎉")

# ✅ 투표 결과 시각화
if os.path.exists(VOTE_PATH):
    vote_df = pd.read_csv(VOTE_PATH)

    st.markdown("### 📊 현재 카테고리 투표 현황")
    cat_votes = vote_df[vote_df["카테고리"] == selected_category]["메뉴"].value_counts()
    st.bar_chart(cat_votes)

    st.markdown("### 🏆 전체 인기 메뉴 TOP 5")
    top_votes = vote_df["메뉴"].value_counts().head(5)
    st.bar_chart(top_votes)