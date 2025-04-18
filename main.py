# main.py
# streamlit run main.py

import streamlit as st

# 페이지 설정
st.set_page_config(page_title="🍔 햄최몇", layout="centered")

from pages import visual, map_ui, mbti, specialty

if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page_name: str):
    st.session_state.page = page_name
    st.rerun()

# 카드 정의
CARD_DEFINITIONS = [
    {"icon":"📊","title":"영양 성분 비교 & 투표","desc":"메뉴 간 성분을 비교하고<br>마음에 드는 메뉴에 투표해보세요!","button":"🚀시작하기","key":"go_visual","target":"visual"},
    {"icon":"🏃","title":"칼로리 소모 지도","desc":"먹은 칼로리를 운동으로<br>얼마나 소모해야 하는지 확인해보세요!","button":"⚙️실행하기","key":"go_map","target":"map"},
    {"icon":"🧠","title":"McBTI 심리 테스트","desc":"버거로 알아보는<br>당신의 심리 유형!","button":"📝테스트하러 가기","key":"go_mbti","target":"mbti"},
    {"icon":"🍽️","title":"영양 기준 추천","desc":"선호하는 영양 기준에 따라<br>메뉴를 추천받아보세요!","button":"👍추천받기","key":"go_specialty","target":"specialty"},
]

# 여기에 spacing 조절용 CSS 추가
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
    /* 카드들 간의 세로 간격을 넉넉히 */
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
/* 버튼 위쪽에 여백을 줘서 카드 본문과 분리 */
.card-button {
    margin-top: 16px !important;
}
</style>
""", unsafe_allow_html=True)

def show_home():
    st.markdown("""
    <h1 style="text-align:center; font-size:48px;">🍔 햄최몇? 🍔</h1>
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
            # use_container_width=True 로 버튼도 카드 안에서 풀폭을 유지
            if st.button(card["button"], key=card["key"], use_container_width=True, args=None):
                go_to(card["target"])
            st.markdown("</div>", unsafe_allow_html=True)

def main():
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