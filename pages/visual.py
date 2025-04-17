import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def run():
    # ✅ 폰트 설정 (한글 깨짐 방지)
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False

    # ✅ 경로 설정
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "McDelivery Nutritional Information Table.csv"))
    VOTE_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "vote_result.csv"))

    # ✅ 데이터 로딩
    @st.cache_data
    def load_data():
        df = pd.read_csv(DATA_PATH, encoding='utf-8')
        df[['칼로리(Kcal)', '단백질', '지방', '나트륨', '당류']] = df[['칼로리(Kcal)', '단백질', '지방', '나트륨', '당류']].apply(pd.to_numeric, errors='coerce')
        return df

    df = load_data()

    # ✅ 타이틀
    st.markdown("<h1 style='text-align:center;'>⚔️메뉴 영양 성분 비교⚔️</h1>", unsafe_allow_html=True)

    # ✅ 카테고리 & 메뉴 선택
    categories = df['카테고리'].dropna().unique()
    selected_category = st.selectbox("🍽️카테고리를 선택하세요", categories)

    filtered_df = df[df['카테고리'] == selected_category]
    menu_options = filtered_df['메뉴'].unique()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='text-align:left; font-weight:bold;'>👈왼쪽 메뉴</div>", unsafe_allow_html=True)
        menu1 = st.selectbox("", menu_options, key='menu1')

    with col2:
        st.markdown("<div style='text-align:right; font-weight:bold;'>오른쪽 메뉴👉</div>", unsafe_allow_html=True)
        menu2 = st.selectbox("", menu_options, index=1 if len(menu_options) > 1 else 0, key='menu2')

    # ✅ 비교 항목
    nutrients = ['칼로리(Kcal)', '단백질', '지방', '나트륨', '당류']
    menu1_vals = filtered_df[filtered_df['메뉴'] == menu1][nutrients].values.flatten()
    menu2_vals = filtered_df[filtered_df['메뉴'] == menu2][nutrients].values.flatten()

    # ✅ 그래프 그리기
    x = np.arange(len(nutrients))
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(x - width/2, menu1_vals, height=width, label=menu1, color='skyblue')
    ax.barh(x + width/2, menu2_vals, height=width, label=menu2, color='lightcoral')

    ax.set_yticks(x)
    ax.set_yticklabels(nutrients)
    ax.invert_yaxis()
    ax.set_xlabel("영양 성분 수치")
    ax.set_title(f"{menu1} vs {menu2} 비교")
    ax.legend()

    for i, (v1, v2) in enumerate(zip(menu1_vals, menu2_vals)):
        ax.text(v1 + 1, i - width/2, f"{v1:.0f}", va='center', fontsize=10)
        ax.text(v2 + 1, i + width/2, f"{v2:.0f}", va='center', fontsize=10)

    st.pyplot(fig)

    # ✅ 메뉴 투표 기능
    st.markdown("---")
    st.markdown("<h2 style='text-align:center;'>🗳️ 마음에 드는 메뉴에 투표해보세요!</h2>", unsafe_allow_html=True)

    if 'voted_categories' not in st.session_state:
        st.session_state.voted_categories = []

    selected_vote_menu = st.selectbox("투표할 메뉴를 선택하세요", menu_options, key='vote_select')

    if st.button("✅ 이 메뉴에 투표하기"):
        if selected_category in st.session_state.voted_categories:
            st.warning(f"'{selected_category}' 카테고리는 이미 투표하셨습니다. 다른 카테고리를 선택해 주세요.")
        else:
            if not os.path.exists(VOTE_PATH):
                pd.DataFrame(columns=["카테고리", "메뉴"]).to_csv(VOTE_PATH, index=False, encoding="utf-8-sig")

            vote_df = pd.read_csv(VOTE_PATH)
            new_vote = pd.DataFrame([[selected_category, selected_vote_menu]], columns=["카테고리", "메뉴"])
            vote_df = pd.concat([vote_df, new_vote], ignore_index=True)
            vote_df.to_csv(VOTE_PATH, index=False, encoding="utf-8-sig")

            st.session_state.voted_categories.append(selected_category)
            st.success(f"'{selected_vote_menu}' 메뉴에 투표해주셔서 감사합니다! 🎉")

    # ✅ 투표 결과 시각화
    if os.path.exists(VOTE_PATH):
        vote_df = pd.read_csv(VOTE_PATH)

        # ✅ 카테고리별 결과
        st.markdown("### 📊 현재 카테고리 투표 현황")
        cat_votes = vote_df[vote_df["카테고리"] == selected_category]["메뉴"].value_counts()

        if not cat_votes.empty:
            fig_cat, ax_cat = plt.subplots(figsize=(8, 4))
            viridis_colors = plt.cm.viridis(np.linspace(0, 1, len(cat_votes)))[::-1]
            ax_cat.bar(cat_votes.index, cat_votes.values, color=viridis_colors)
            ax_cat.set_ylabel("투표 수")
            ax_cat.set_title(f"{selected_category} 카테고리 인기 메뉴")
            ax_cat.tick_params(axis='x', rotation=30)
            st.pyplot(fig_cat)
        else:
            st.info("이 카테고리는 아직 투표 데이터가 없습니다.")

        # ✅ 전체 인기 메뉴 TOP 5
        st.markdown("### 🏆 전체 인기 메뉴 TOP 5")
        top_votes = vote_df["메뉴"].value_counts().head(5)

        if not top_votes.empty:
            fig_top, ax_top = plt.subplots(figsize=(8, 4))
            viridis_colors2 = plt.cm.viridis(np.linspace(0, 1, len(top_votes)))[::-1]
            ax_top.bar(top_votes.index, top_votes.values, color=viridis_colors2)
            ax_top.set_ylabel("투표 수")
            ax_top.set_title("전체 인기 메뉴 TOP 5")
            ax_top.tick_params(axis='x', rotation=30)
            st.pyplot(fig_top)
        else:
            st.info("전체 투표 데이터가 아직 없습니다.")

    # ✅ 홈으로 돌아가기 버튼
    st.markdown("---")
    if st.button("🏠 홈으로 돌아가기"):
        st.session_state.page = "home"
        st.rerun()