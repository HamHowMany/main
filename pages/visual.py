import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime
import matplotlib.font_manager as fm
from google.oauth2 import service_account
import gspread
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh

SHEET_NAME = "google_vote_result"

# ✅ Google Sheets 연결
@st.cache_resource
def get_gsheet():
    if "GOOGLE_SERVICE_ACCOUNT" in st.secrets:
        info = st.secrets["GOOGLE_SERVICE_ACCOUNT"]
    else:
        load_dotenv()
        cred_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        if not cred_path or not os.path.exists(cred_path):
            raise FileNotFoundError("❌ .env에 GOOGLE_SERVICE_ACCOUNT_JSON 경로가 없거나 파일이 존재하지 않습니다.")
        with open(cred_path, "r", encoding="utf-8") as f:
            info = json.load(f)

    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = service_account.Credentials.from_service_account_info(info, scopes=scopes)
    gc = gspread.authorize(credentials)
    sheet = gc.open(SHEET_NAME).sheet1
    return sheet

# ✅ 폰트 설정
def setup_fonts():
    font_path = os.path.join(os.path.dirname(__file__), "assets", "fonts", "NanumGothic.ttf")
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        font_prop = fm.FontProperties(fname=font_path)
        plt.rcParams["font.family"] = font_prop.get_name()
    plt.rcParams["axes.unicode_minus"] = False

# ✅ 데이터 로딩
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "McDelivery Nutritional Information Table.csv")
    df = pd.read_csv(path)
    df[['칼로리(Kcal)', '단백질', '지방', '나트륨', '당류']] = df[['칼로리(Kcal)', '단백질', '지방', '나트륨', '당류']].apply(pd.to_numeric, errors='coerce')
    return df

# ✅ 시각화 함수
def draw_vote_chart(title, vote_series):
    import matplotlib.cm as cm
    fig, ax = plt.subplots(figsize=(8, 4))
    colors = cm.Set3(np.linspace(0, 1, len(vote_series)))
    bars = ax.bar(vote_series.index, vote_series.values, color=colors)

    ax.set_title(title, fontsize=14)
    ax.set_ylabel("투표 수")
    ax.set_xticks(range(len(vote_series)))
    ax.set_xticklabels(vote_series.index, rotation=15, ha="right")

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.1, f"{int(height)}", ha='center', va='bottom', fontsize=9)

    st.pyplot(fig)

# ✅ 실행 함수
def run():
    setup_fonts()
    st_autorefresh(interval=30 * 1000, key="auto_refresh")
    df = load_data()
    sheet = get_gsheet()

    # ✅ 타이틀
    st.markdown("<h1 style='text-align:center;'>ㅤ 메뉴 별 영양성분 비교! </h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>내 최애 메뉴, 생각보다 짜다고...?</p>", unsafe_allow_html=True)

    # ✅ 메뉴 선택
    categories = df['카테고리'].dropna().unique()
    selected_category = st.selectbox("🍽️ 카테고리를 선택하세요", categories)
    filtered_df = df[df['카테고리'] == selected_category]
    menu_options = filtered_df['메뉴'].unique()

    col1, col2 = st.columns(2)
    with col1:
        menu1 = st.selectbox("1번 메뉴", menu_options, key="menu1")
    with col2:
        menu2 = st.selectbox("2번 메뉴", menu_options, index=1, key="menu2")

    # ✅ 영양성분 비교 그래프
    nutrients = ['칼로리(Kcal)', '단백질', '지방', '나트륨', '당류']
    labels = ['칼로리(Kcal)', '단백질 (g)', '지방 (g)', '나트륨 (mg)', '당류 (g)']
    menu1_vals = filtered_df[filtered_df['메뉴'] == menu1][nutrients].values.flatten()
    menu2_vals = filtered_df[filtered_df['메뉴'] == menu2][nutrients].values.flatten()

    x = np.arange(len(nutrients))
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(x - width/2, menu1_vals, height=width, label=menu1, color='skyblue')
    ax.barh(x + width/2, menu2_vals, height=width, label=menu2, color='salmon')
    ax.set_yticks(x)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_title(f"{menu1} vs {menu2} 비교")
    ax.legend()
    st.pyplot(fig)

    # ✅ 투표 인터페이스
    st.markdown("---")
    st.subheader("🗳️ 실시간 선호 메뉴 투표!")
    st.markdown("<p style='text-align:left; color:#888;'>내 최애 버거, 지금 몇 위일까?</p>", unsafe_allow_html=True)

    if "voted" not in st.session_state:
        st.session_state.voted = []

    selected_vote_menu = st.selectbox("투표할 메뉴 선택", menu_options, key="vote_select")
    if st.button("✅ 이 메뉴에 투표하기"):
        if selected_category in st.session_state.voted:
            st.warning("이미 해당 카테고리에 투표하셨습니다.")
        else:
            timestamp = datetime.now().isoformat()
            row = [selected_category, selected_vote_menu, timestamp]
            sheet.append_row(row)
            st.session_state.voted.append(selected_category)
            st.success(f"'{selected_vote_menu}'에 투표 완료!")

    # ✅ 실시간 투표 집계 표시 전 새로고침 섹션
    st.caption(f"⏰ 마지막 새로고침 시각: {datetime.now().strftime('%H:%M:%S')}")
    if st.button("🔁 수동 새로고침"):
        st.rerun()

    # ✅ 실시간 투표 시각화
    st.markdown("### 📊 현재 카테고리 별 투표 현황")
    all_votes = pd.DataFrame(sheet.get_all_records())
    cat_votes = all_votes[all_votes["카테고리"] == selected_category]["메뉴"].value_counts()
    if not cat_votes.empty:
        draw_vote_chart("현재 카테고리 별 투표 현황", cat_votes)

    st.markdown("### 🏆 전체 인기 메뉴 TOP 5")
    top5 = all_votes["메뉴"].value_counts().head(5)
    if not top5.empty:
        draw_vote_chart("전체 인기 메뉴 TOP 5", top5)

    # ✅ 홈으로 돌아가기
    st.markdown("---")
    if st.button("🏠 홈으로 돌아가기"):
        st.session_state.page = "home"
        st.rerun()