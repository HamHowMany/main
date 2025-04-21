# main.py
# streamlit run main.py
import streamlit as st
# ✅ 페이지 설정 + 사이드바 숨기기
st.set_page_config(
    page_title="🍔 햄최몇",
    layout="centered",
    initial_sidebar_state="collapsed"
)

import os
import platform
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pages import visual, map_ui, mbti, specialty

# setup_fonts 함수 수정
def setup_fonts():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_font_path = os.path.join(base_dir, "assets", "fonts", "NanumGothic.ttf")

    if os.path.exists(local_font_path):
        fm.fontManager.addfont(local_font_path)
        nanum_font = fm.FontProperties(fname=local_font_path)
        plt.rcParams['font.family'] = nanum_font.get_name()
        plt.rcParams["axes.unicode_minus"] = False
        print(f"✅ matplotlib에 폰트 직접 등록: {nanum_font.get_name()}")
    else:
        print("❌ NanumGothic.ttf 경로를 찾을 수 없습니다.")


# ✅ 사이드바 자체 숨기기 (Streamlit 기본 탐색 제거)
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# ✅ 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "home"

# ✅ 카드 UI 정의
CARD_DEFINITIONS = [
    {"icon":"📊","title":"영양 성분 비교 & 투표","desc":"메뉴 간 성분을 비교하고<br>마음에 드는 메뉴에 투표해보세요!","button":"🚀 시작하기","key":"go_visual","target":"visual"},
    {"icon":"🏃","title":"칼로리 소모 지도","desc":"먹은 칼로리를 운동으로<br>얼마나 소모해야 하는지 확인해보세요!","button":"⚙️ 실행하기","key":"go_map","target":"map"},
    {"icon":"🧠","title":"McBTI 심리 테스트","desc":"버거로 알아보는<br>당신의 심리 유형!","button":"📝 테스트하러 가기","key":"go_mbti","target":"mbti"},
    {"icon":"🍽️","title":"영양 기준 추천","desc":"선호하는 영양 기준에 따라<br>메뉴를 추천받아보세요!","button":"👍 추천받기","key":"go_specialty","target":"specialty"},
]

# ✅ 카드 스타일
st.markdown("""
<style>
.card {
    background-color: var(--gray-100);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    text-align: center;
    transition: transform 0.2s ease-in-out;
    border: 2px solid transparent;
    margin-bottom: 32px;
    height: 200px;
}
.card:hover {
    transform: translateY(-4px);
    border-color: #4CAF50;
}
.card-icon {
    font-size: 36px;
    margin-bottom: 10px;
}
.card-title {
    font-weight: 600;
    font-size: 18px;
    margin-bottom: 6px;
}
.card-desc {
    font-size: 14px;
    margin-bottom: 12px;
    color: var(--text-secondary);
}
.card-button {
    margin-top: 16px !important;
}
</style>
""", unsafe_allow_html=True)

# ✅ 이동 함수
def go_to(page_name: str):
    st.session_state.page = page_name
    st.rerun()

# ✅ 홈 화면
def show_home():
    st.markdown("""
    <h1 style="text-align:center; font-size:48px;">ㅤ햄최몇..?</h1>
    <p style="text-align:center; font-size:16px;">원하는 기능을 아래 카드에서 선택해보세요!</p>
    """, unsafe_allow_html=True)

    cols = st.columns(2, gap="large")
    for idx, card in enumerate(CARD_DEFINITIONS):
        col = cols[idx % 2]
        with col:
            st.markdown(f"""
                <div class="card">
                  <div class="card-icon">{card['icon']}</div>
                  <div class="card-title">{card['title']}</div>
                  <div class="card-desc">{card['desc']}</div>
            """, unsafe_allow_html=True)
            if st.button(card["button"], key=card["key"], use_container_width=True):
                go_to(card["target"])
            st.markdown("</div>", unsafe_allow_html=True)

# ✅ 메인 실행 함수
def main():
    setup_fonts()
    if st.session_state.page == "home":
        show_home()
    elif st.session_state.page == "visual":
        visual.run()
    elif st.session_state.page == "map":
        map_ui.run()
    elif st.session_state.page == "mbti":
        mbti.run()
    elif st.session_state.page == "specialty":
        specialty.run()

if __name__ == "__main__":
    main()