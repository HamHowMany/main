import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import platform  # ✅ 추가
import matplotlib.font_manager as fm

def setup_fonts():
    system = platform.system()
    if system == "Windows":
        font_path = "C:\\Windows\\Fonts\\malgun.ttf"
    elif system == "Darwin":
        font_path = "/System/Library/Fonts/AppleGothic.ttf"
    else:
        # ✅ Linux (Streamlit Cloud) 환경에는 NanumGothic 또는 DejaVuSans 사용
        font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
        if not os.path.exists(font_path):
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    if os.path.exists(font_path):
        prop = fm.FontProperties(fname=font_path)
        plt.rc("font", family=prop.get_name())
    else:
        print("⚠️ 시스템 폰트를 찾을 수 없습니다. 기본 설정을 사용합니다.")

    plt.rcParams["axes.unicode_minus"] = False

def run():
    setup_fonts()  # ✅ 여기에 호출 추가

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

    st.markdown("<h1 style='text-align:center;'>⚔️메뉴 영양 성분 비교⚔️</h1>", unsafe_allow_html=True)

    categories = df['카테고리'].dropna().unique()
    selected_category = st.selectbox("🍽️카테고리를 선택하세요", categories)
    filtered_df = df[df['카테고리'] == selected_category]
    menu_options = filtered_df['메뉴'].unique()

    col1, col2 = st.columns(2)

    with col1:
        menu1 = st.selectbox("1번 메뉴", menu_options, key="menu1")

    with col2:
        menu2 = st.selectbox("2번 메뉴", menu_options, index=1 if len(menu_options) > 1 else 0, key="menu2")



    nutrients = ['칼로리(Kcal)', '단백질', '지방', '나트륨', '당류']
    display_labels = ['칼로리(Kcal)', '단백질 (g)', '지방 (g)', '나트륨 (mg)', '당류 (g)']
    menu1_vals = filtered_df[filtered_df['메뉴'] == menu1][nutrients].values.flatten()
    menu2_vals = filtered_df[filtered_df['메뉴'] == menu2][nutrients].values.flatten()

    x = np.arange(len(nutrients))
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(x - width/2, menu1_vals, height=width, label=menu1, color='skyblue')
    ax.barh(x + width/2, menu2_vals, height=width, label=menu2, color='lightcoral')
    ax.set_yticks(x)
    ax.set_yticklabels(display_labels)
    ax.invert_yaxis()
    ax.set_xlabel("영양 성분 수치")
    ax.set_title(f"{menu1} vs {menu2} 비교")
    ax.legend()
    for i, (v1, v2) in enumerate(zip(menu1_vals, menu2_vals)):
        ax.text(v1 + 1, i - width/2, f"{v1:.0f}", va='center')
        ax.text(v2 + 1, i + width/2, f"{v2:.0f}", va='center')
    st.pyplot(fig)

    st.markdown("---")
    st.markdown("### 🗳️ 마음에 드는 메뉴에 투표해보세요!")

    if "voted_categories" not in st.session_state:
        st.session_state.voted_categories = []

    selected_vote_menu = st.selectbox("투표할 메뉴를 선택하세요", menu_options, key="vote_select")
    if st.button("✅ 이 메뉴에 투표하기"):
        if selected_category in st.session_state.voted_categories:
            st.warning("이미 투표하신 카테고리입니다.")
        else:
            if not os.path.exists(VOTE_PATH):
                pd.DataFrame(columns=["카테고리", "메뉴"]).to_csv(VOTE_PATH, index=False, encoding="utf-8-sig")
            vote_df = pd.read_csv(VOTE_PATH)
            new_vote = pd.DataFrame([[selected_category, selected_vote_menu]], columns=["카테고리", "메뉴"])
            vote_df = pd.concat([vote_df, new_vote], ignore_index=True)
            vote_df.to_csv(VOTE_PATH, index=False, encoding="utf-8-sig")
            st.session_state.voted_categories.append(selected_category)
            st.success(f"'{selected_vote_menu}'에 투표 감사합니다!")

    if os.path.exists(VOTE_PATH):
        vote_df = pd.read_csv(VOTE_PATH)
        st.markdown("### 📊 현재 카테고리 투표 현황")
        cat_votes = vote_df[vote_df["카테고리"] == selected_category]["메뉴"].value_counts()
        if not cat_votes.empty:
            fig1, ax1 = plt.subplots(figsize=(8, 4))
            ax1.bar(cat_votes.index, cat_votes.values, color=plt.cm.viridis(np.linspace(0, 1, len(cat_votes))))
            ax1.set_title("카테고리별 인기 메뉴")
            st.pyplot(fig1)
        else:
            st.info("아직 투표 데이터가 없습니다.")

        st.markdown("### 🏆 전체 인기 메뉴 TOP 5")
        top_votes = vote_df["메뉴"].value_counts().head(5)
        if not top_votes.empty:
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            ax2.bar(top_votes.index, top_votes.values, color=plt.cm.viridis(np.linspace(0, 1, len(top_votes))))
            ax2.set_title("전체 인기 메뉴 TOP 5")
            st.pyplot(fig2)
        else:
            st.info("아직 투표 데이터가 없습니다.")

    st.markdown("---")
    if st.button("🏠 홈으로 돌아가기"):
        st.session_state.page = "home"
        st.rerun()