# main.py
# 실행: streamlit run main.py

import streamlit as st
from pages import visual, map_ui, mbti  # ✅ MBTI 모듈 포함

# ✅ 페이지 설정
st.set_page_config(page_title="🍔 햄최몇", layout="centered")

# ✅ 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "home"

# ✅ 페이지 전환 함수 (🔁 rerun 포함)
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()  # ✅ 버튼 두 번 누르는 문제 해결

# ✅ 홈 화면
def show_home():
    st.markdown("""
        <h1 style='text-align: center; font-size: 48px;'>🍔 햄최몇?</h1>
        <h3 style='text-align: center;'>햄버거... 최대 몇 개까지 괜찮을까? 🤯</h3>
        <p style='text-align: center; font-size: 16px;'>원하는 기능을 아래 카드에서 선택해보세요!</p>
        <br>
    """, unsafe_allow_html=True)

    # ✅ 카드 스타일 정의
    card_css = """
        <style>
            .card {
                background-color: #1e1e1e;
                padding: 20px;
                border-radius: 16px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                text-align: center;
                transition: all 0.2s ease-in-out;
                border: 2px solid transparent;
                height: 220px;
                margin-bottom: 8px;
            }
            .card:hover {
                transform: scale(1.02);
                border-color: #4CAF50;
            }
            .card-icon {
                font-size: 40px;
                margin-bottom: 10px;
            }
            .card-title {
                font-weight: bold;
                font-size: 20px;
                margin-top: 5px;
            }
            .card-desc {
                font-size: 14px;
                margin-top: 5px;
                margin-bottom: 18px;
            }
        </style>
    """
    st.markdown(card_css, unsafe_allow_html=True)

    # ✅ 상단 두 개 카드
    col1, col2 = st.columns(2)

    with col1:
        with st.container():
            st.markdown("""
            <div class="card">
                <div class="card-icon">📊</div>
                <div class="card-title">영양 성분 비교 & 투표</div>
                <div class="card-desc">메뉴 간 성분을 비교하고<br>마음에 드는 메뉴에 투표해보세요!</div>
            """, unsafe_allow_html=True)

            if st.button("✅ 시작하기", key="go_visual", use_container_width=True):
                go_to("visual")

            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        with st.container():
            st.markdown("""
            <div class="card">
                <div class="card-icon">🏃</div>
                <div class="card-title">칼로리 소모 지도</div>
                <div class="card-desc">먹은 칼로리를 운동으로<br>얼마나 소모해야 하는지 확인해보세요!</div>
            """, unsafe_allow_html=True)

            if st.button("🏁 실행하기", key="go_map", use_container_width=True):
                go_to("map")

            st.markdown("</div>", unsafe_allow_html=True)

    # ✅ 하단 MBTI 카드
    st.markdown("<br>", unsafe_allow_html=True)
    col_center, _ = st.columns([1, 1])
    with col_center:
        with st.container():
            st.markdown("""
            <div class="card">
                <div class="card-icon">🧠</div>
                <div class="card-title">MBTI 심리 테스트</div>
                <div class="card-desc">버거로 알아보는<br>당신의 심리 유형!</div>
            """, unsafe_allow_html=True)

            if st.button("🔍 테스트하러 가기", key="go_mbti", use_container_width=True):
                go_to("mbti")

            st.markdown("</div>", unsafe_allow_html=True)

# ✅ 페이지 라우팅
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "visual":
    visual.run()
elif st.session_state.page == "map":
    map_ui.run()
elif st.session_state.page == "mbti":
    mbti.run()
    
print("현재 페이지:", st.session_state.page)