import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
import platform
import matplotlib.font_manager as fm
from streamlit_geolocation import streamlit_geolocation
from google.oauth2 import service_account
import gspread

# ✅ 구글 시트 설정
SHEET_NAME = "google_vote_result"
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID/edit"

# ✅ 서비스 계정 인증
@st.cache_resource
def get_gsheet():
    import json

    # 1. 비밀키를 secrets.toml에서 가져옴
    json_str = st.secrets["GOOGLE_SERVICE_ACCOUNT"]
    info = json.loads(json_str)

    # 2. 자격증명 객체 생성
    credentials = service_account.Credentials.from_service_account_info(info)
    
    # 3. gspread 클라이언트 초기화
    gc = gspread.authorize(credentials)

    # 4. 시트 접근
    sheet = gc.open("google_vote_result").sheet1
    return sheet

# ✅ 폰트 설정
def setup_fonts():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(base_dir, "assets", "fonts", "NanumGothic.ttf")
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        nanum_font = fm.FontProperties(fname=font_path)
        plt.rcParams["font.family"] = nanum_font.get_name()
    plt.rcParams["axes.unicode_minus"] = False

# ✅ 데이터 로딩
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "McDelivery Nutritional Information Table.csv")
    df = pd.read_csv(path)
    df[['칼로리(Kcal)', '단백질', '지방', '나트륨', '당류']] = df[['칼로리(Kcal)', '단백질', '지방', '나트륨', '당류']].apply(pd.to_numeric, errors='coerce')
    return df

# ✅ 메인 실행 함수
def run():
    setup_fonts()
    df = load_data()
    sheet = get_gsheet()

    st.markdown("<h1 style='text-align:center;'>⚔️ 메뉴 영양 성분 비교 & 실시간 투표 ⚔️</h1>", unsafe_allow_html=True)
    categories = df['카테고리'].dropna().unique()
    selected_category = st.selectbox("🍽️ 카테고리를 선택하세요", categories)
    filtered_df = df[df['카테고리'] == selected_category]
    menu_options = filtered_df['메뉴'].unique()

    col1, col2 = st.columns(2)
    with col1:
        menu1 = st.selectbox("1번 메뉴", menu_options, key="menu1")
    with col2:
        menu2 = st.selectbox("2번 메뉴", menu_options, index=1, key="menu2")

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

    st.markdown("---")
    st.subheader("🗳️ 마음에 드는 메뉴에 투표하세요!")

    if "voted" not in st.session_state:
        st.session_state.voted = []

    selected_vote_menu = st.selectbox("투표할 메뉴 선택", menu_options, key="vote_select")
    if st.button("✅ 이 메뉴에 투표하기"):
        if selected_category in st.session_state.voted:
            st.warning("이미 해당 카테고리에 투표하셨습니다.")
        else:
            loc = streamlit_geolocation()
            timestamp = datetime.now().isoformat()
            ip = st.experimental_get_query_params().get("ip", ["익명"])[0]
            location_str = f"{loc['latitude']:.4f}, {loc['longitude']:.4f}" if loc else "위치 미제공"
            row = [selected_category, selected_vote_menu, timestamp, ip, location_str]
            sheet.append_row(row)
            st.session_state.voted.append(selected_category)
            st.success(f"'{selected_vote_menu}'에 투표 완료!")

    # ✅ 실시간 집계
    st.markdown("### 📊 현재 카테고리 투표 현황")
    all_votes = pd.DataFrame(sheet.get_all_records())
    cat_votes = all_votes[all_votes["카테고리"] == selected_category]["메뉴"].value_counts()
    if not cat_votes.empty:
        st.bar_chart(cat_votes)

    st.markdown("### 🏆 전체 인기 메뉴 TOP 5")
    top5 = all_votes["메뉴"].value_counts().head(5)
    if not top5.empty:
        st.bar_chart(top5)

    st.markdown("---")
    if st.button("🏠 홈으로 돌아가기"):
        st.session_state.page = "home"
        st.rerun()