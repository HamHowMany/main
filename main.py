import streamlit as st
from code import macbti, exercise_calc, kcal_analysis, smart_recommend

# 페이지 초기화 (최초 로딩 시 session_state 설정)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# 화면 전환 함수
def go_to(page_name):
    st.session_state.page = page_name

# 🍔 메인 홈 화면
def show_home():
    st.title("🍔 햄최몇?")
    st.markdown("### 맥도날드 메뉴, 얼마나 먹어도 괜찮을까?")
    st.write("아래 기능 중 하나를 선택해보세요!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✨ 맥비티아이"):
            go_to("macbti")
        if st.button("🔥 운동량 계산 & 지도 시각화"):
            go_to("exercise")
    with col2:
        if st.button("📊 영양성분 시각화"):
            go_to("kcal_analysis")
        if st.button("🎯 나에게 맞는 추천 메뉴"):
            go_to("recommend")

    st.markdown("---")
    st.caption("Made with ❤️ by 햄최몇 팀")

# 페이지 라우팅
if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'macbti':
    macbti.run()
elif st.session_state.page == 'exercise':
    exercise_calc.run()
elif st.session_state.page == 'kcal_analysis':
    kcal_analysis.run()
elif st.session_state.page == 'recommend':
    smart_recommend.run()
