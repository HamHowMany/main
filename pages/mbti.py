# pages/mbti.py

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def setup_fonts():
    """한글 폰트 설정 (Malgun Gothic)"""
    font_path = "C:\\Windows\\Fonts\\malgun.ttf"
    prop = fm.FontProperties(fname=font_path)
    plt.rc("font", family=prop.get_name())

def inject_css():
    """라이트/다크 모드 대응 + 옵션 카드 스타일"""
    st.markdown(
        """
        <style>
        .option-card {
            padding: 16px;
            border-radius: 12px;
            margin: 12px 0;
            border: 2px solid transparent;
            transition: background-color 0.2s, border-color 0.2s, transform 0.2s;
            cursor: pointer;
        }
        .option-card:hover {
            transform: translateY(-2px);
        }
        /* Light mode */
        [data-theme="light"] .option-card {
            background-color: #f9f9f9;
            color: #111;
        }
        [data-theme="light"] .option-card:hover {
            background-color: #eeeeee;
            border-color: #f39c12;
        }
        /* Dark mode */
        [data-theme="dark"] .option-card {
            background-color: #2e2e2e;
            color: #eee;
        }
        [data-theme="dark"] .option-card:hover {
            background-color: #3a3a3a;
            border-color: #f39c12;
        }
        /* 선택된 상태 */
        .option-card.selected {
            border-color: #4caf50 !important;
            background-color: #444 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def show_intro(base_dir: str):
    """인트로 화면: 제목 + 이미지 + 테스트 시작 카드"""
    st.markdown(
        "<h1 style='text-align:center;'>🍔 나의 "
        "<span style='color:#ffcf48;'>McBTI</span>는?</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; color:#888;'>"
        "버거로 알아보는 나의 성격 유형!</p>",
        unsafe_allow_html=True
    )

    img_path = os.path.join(base_dir, "..", "data", "burgers.png")
    if os.path.exists(img_path):
        st.image(img_path, use_column_width=True, caption="당신을 기다리는 버거들")
    else:
        st.warning("인트로 이미지를 불러올 수 없습니다.")

    # 시작 카드
    st.markdown(
        '<div class="option-card" style="text-align:center;">'
        '<div style="font-size:40px;">🧠</div>'
        '<b>McBTI 심리 테스트</b><br>'
        '심리 유형을 통해 어울리는 버거를 추천받아보세요!'
        '</div>',
        unsafe_allow_html=True
    )
    if st.button("🔥 테스트 시작하기", use_container_width=True):
        st.session_state.mbti_page = "quiz"
        st.session_state.answers    = []
        st.rerun()

def show_quiz(base_dir: str):
    """퀴즈 화면: 12개 문항 순차 출력"""
    questions = [
        {"q":"모임에 초대받았을 때 당신은?",         "opts":["A. 좋아! 사람들과 어울리면 에너지가 나요.","B. 부담돼요. 혼자가 편해요."]},
        {"q":"대화할 때 나는?",                   "opts":["A. 즉흥적으로 말이 술술 나와요.","B. 생각 정리 후 말해요."]},
        {"q":"정보를 받아들일 때 나는?",           "opts":["A. 눈에 보이는 사실이 중요해요.","B. 의미와 가능성이 더 궁금해요."]},
        {"q":"설명서를 읽을 때 나는?",             "opts":["A. 순서대로 꼼꼼히 읽어요.","B. 대충 보고 감으로 파악해요."]},
        {"q":"친구가 고민 상담할 때 나는?",         "opts":["A. 객관적인 해결책을 말해줘요.","B. 감정을 공감해줘요."]},
        {"q":"결정을 내릴 때 나는?",               "opts":["A. 논리적으로 분석해요.","B. 사람 마음과 분위기를 고려해요."]},
        {"q":"여행 계획을 세울 때 나는?",           "opts":["A. 일정을 미리 정해놓고 움직여요.","B. 즉흥적으로 즐겨요."]},
        {"q":"과제를 할 때 나는?",                 "opts":["A. 마감 전 미리 끝내야 마음 편해요.","B. 마감 직전이 집중이 잘 돼요."]},
        {"q":"메뉴를 고를 때 나는?",               "opts":["A. 새로운 걸 도전해보고 싶어요!","B. 먹던 거 또 먹어야 안심돼요."]},
        {"q":"계획이 바뀌면?",                   "opts":["A. 스트레스 받아요. 원래대로 해야 해요.","B. 뭐 어때요~ 즉흥도 재밌죠."]},
        {"q":"실수했을 때 나는?",                 "opts":["A. 원인 분석부터 해요.","B. 스스로를 위로해요."]},
        {"q":"점심 메뉴를 친구가 정해준다면?",     "opts":["A. 편해서 좋아요!","B. 내가 고르는 게 더 좋아요!"]},
    ]

    idx = len(st.session_state.answers)
    current = questions[idx]
    st.markdown(f"<h4>{idx+1}. {current['q']}</h4>", unsafe_allow_html=True)

    sel_key = f"sel_{idx}"
    if sel_key not in st.session_state:
        st.session_state[sel_key] = None

    for i, opt in enumerate(current["opts"]):
        card_cls = "option-card selected" if st.session_state[sel_key] == opt else "option-card"
        btn_id = f"btn_{idx}_{i}"
        st.markdown(
            f'<div class="{card_cls}" onclick="document.getElementById(\'{btn_id}\').click()">{opt}</div>',
            unsafe_allow_html=True
        )
        if st.button("선택", key=btn_id):
            st.session_state[sel_key] = opt
            st.session_state.answers.append(opt)
            if idx+1 < len(questions):
                st.session_state.mbti_page = "quiz"
            else:
                st.session_state.mbti_page = "result"
            st.rerun()

def show_result(base_dir: str):
    import os
    import pandas as pd
    import streamlit as st

    # MBTI 결과 계산
    counts = {c: 0 for c in "EISNTFJP"}
    for ans in st.session_state.answers:
        for c in counts:
            if f"({c})" in ans:
                counts[c] += 1

    mbti = "".join([
        "E" if counts["E"] >= counts["I"] else "I",
        "S" if counts["S"] >= counts["N"] else "N",
        "T" if counts["T"] >= counts["F"] else "F",
        "J" if counts["J"] >= counts["P"] else "P"
    ])

    burger_map = {
        "INTJ": ("더블 1955 버거", "차갑고 진한 고기맛처럼 계획적"),
        "INTP": ("트리플 치즈버거", "치즈처럼 말랑하지만 복잡함"),
        "ENTJ": ("쿼터파운더 치즈", "한 입에 존재감 폭발, 리더맛"),
        "ENTP": ("슈비 버거", "새우+소고기 조합처럼 상상초월"),
        "INFJ": ("토마토 치즈 비프 버거", "부드럽고 진지한 속마음 토핑"),
        "INFP": ("불고기 버거", "달달하고 감성 터지는 맛"),
        "ENFJ": ("빅맥", "모두 챙기는 층층한 다정함"),
        "ENFP": ("맥스파이시 상하이 버거", "매콤하고 톡톡 튀는 자유인"),
        "ISTJ": ("맥치킨", "늘 같은 자리, 기본에 진심"),
        "ISFJ": ("슈슈 버거", "바삭함 속 따뜻한 배려심"),
        "ESTJ": ("더블 치즈버거", "정석대로 두 배로 확실하게"),
        "ESFJ": ("맥크리스피 클래식 버거", "딱 맞는 조합, 모두를 위해"),
        "ISTP": ("더블 불고기 버거", "조용하지만 실속 가득"),
        "ISFP": ("치즈버거", "소박하지만 감성 깊은 맛"),
        "ESTP": ("맥크리스피 디럭스 버거", "바삭! 지금 아니면 못 참음"),
        "ESFP": ("더블 맥스파이시 상하이 버거", "매운 맛도 즐기는 인싸감성")
    }

    burger, label = burger_map[mbti]

    # ───────────── UI ─────────────
    st.markdown("<h2 style='text-align:center;'>🍔당신의 버거 유형은?🍔</h2>", unsafe_allow_html=True)

    # 이미지 중앙 정렬
    MBTI_IMG_PATH = os.path.join(base_dir, "..", "data", "mbti_images", f"{mbti}.png")
    img_cols = st.columns([1, 2, 1])
    with img_cols[1]:
        if os.path.exists(MBTI_IMG_PATH):
            st.image(MBTI_IMG_PATH, caption=f"{mbti} 타입", use_column_width=True)
        else:
            st.warning(f"{mbti}에 대한 이미지를 찾을 수 없습니다: {MBTI_IMG_PATH}")

    # 버거 이름 + 설명 중앙 정렬
    st.markdown("<br>", unsafe_allow_html=True)
    info_cols = st.columns([1, 2, 1])
    with info_cols[1]:
        st.markdown(f"""
            <div style='text-align:center;'>
                <h3>🍔<b>{burger}</b>🍔</h3>
                <p style='font-size:18px; margin:6px 0;'><b>{mbti}</b></p>
                <p style='color:#777; font-size:16px;'>{label}</p>
            </div>
        """, unsafe_allow_html=True)

    # 버튼 정렬
    st.markdown("<br>", unsafe_allow_html=True)
    btn_cols = st.columns([1, 2, 1])
    with btn_cols[1]:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 다시 테스트하기"):
                st.session_state.mbti_page = "intro"
                st.session_state.answers = []
                for key in list(st.session_state.keys()):
                    if key.startswith("selected_"):
                        del st.session_state[key]
                st.rerun()
        with col2:
            if st.button("🏠 홈으로 돌아가기"):
                st.session_state.page = "home"
                st.session_state.mbti_page = "intro"
                st.session_state.answers = []
                for key in list(st.session_state.keys()):
                    if key.startswith("selected_"):
                        del st.session_state[key]
                st.rerun()

def run():
    """MBTI 페이지 엔트리포인트"""
    setup_fonts()
    inject_css()

    if "mbti_page" not in st.session_state:
        st.session_state.mbti_page = "intro"
        st.session_state.answers    = []

    base_dir = os.path.dirname(__file__)
    page     = st.session_state.mbti_page

    if page == "intro":
        show_intro(base_dir)
    elif page == "quiz":
        show_quiz(base_dir)
    else:
        show_result(base_dir)