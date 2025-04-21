import os
import platform

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
import matplotlib.font_manager as fm

# ─────────────────────────────────────────────────────
# 전역 CSS: 카드 hover 효과 + nutrient-text 스타일
st.markdown("""
<style>
.menu-card {
    border-radius: 16px;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.menu-card:hover {
    transform: scale(1.02);
    box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}
.nutrient-text {
    background-color: #ffffff !important;
    color: #333333 !important;
    padding: 8px;
    border-radius: 8px;
    margin-left: 16px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# 상수 정의
DATA_REL_PATH = os.path.join("..", "data", "McDelivery Nutritional Information Table.csv")
NUTRIENTS      = ["칼로리(Kcal)", "단백질", "지방", "나트륨"]

STYLE = {
    "category": """
        background-color: #F4B400;
        padding: 12px;
        font-weight: bold;
        text-align: center;
        font-size: 18px;
        color: black;
    """,
    "menu_name": """
        background-color: #2ECC71;
        padding: 14px;
        font-size: 20px;
        font-weight: bold;
        color: white;
        text-align: center;
    """,
    "patty_top": """
        background-color: #8B4513;
        height: 30px;
        margin: 0;
    """,
    "patty_bottom": """
        background-color: #FFDD57;
        height: 30px;
        margin: 0;
    """,
    "score": """
        background-color: #E74C3C;
        padding: 12px;
        color: white;
        font-weight: bold;
        text-align: center;
        font-size: 16px;
    """,
    "price": """
        background-color: #F4B400;
        padding: 12px;
        color: black;
        font-weight: bold;
        text-align: center;
        font-size: 16px;
    """
}
# ─────────────────────────────────────────────────────

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



@st.cache_data
def load_data() -> pd.DataFrame:
    """CSV 파일을 읽어와 DataFrame으로 반환"""
    base = os.path.dirname(os.path.abspath(__file__))
    df   = pd.read_csv(os.path.join(base, DATA_REL_PATH))
    df.columns = df.columns.str.strip()
    if "컬로리(Kcal)" in df.columns:
        df.rename(columns={"컬로리(Kcal)": "칼로리(Kcal)"}, inplace=True)
    if "매뉴얼" in df.columns:
        df.rename(columns={"매뉴얼": "메뉴"}, inplace=True)
    return df

def get_user_preferences(df: pd.DataFrame) -> dict:
    """사용자로부터 필터링 및 기타 설정을 입력받아 반환"""
    cal_min, cal_max   = int(df["칼로리(Kcal)"].min()),  int(df["칼로리(Kcal)"].max())
    prot_min, prot_max = float(df["단백질"].min()),      float(df["단백질"].max())
    fat_min, fat_max   = float(df["지방"].min()),        float(df["지방"].max())
    sod_min, sod_max   = float(df["나트륨"].min()),      float(df["나트륨"].max())

    st.markdown("#### 📏 영양소 범위")
    min_cal, max_cal     = st.slider("칼로리 (kcal)",  cal_min,      cal_max,      (cal_min, cal_max))
    min_prot, max_prot   = st.slider("단백질 (g)",    int(prot_min), int(prot_max), (int(prot_min), int(prot_max)))
    min_fat, max_fat     = st.slider("지방 (g)",      int(fat_min),  int(fat_max),  (int(fat_min), int(fat_max)))
    min_sod, max_sod     = st.slider("나트륨 (mg)",   int(sod_min),  int(sod_max),  (int(sod_min), int(sod_max)))

    st.markdown("#### ⚖️ 중요도 설정")
    weights = {
        "칼로리": st.slider("칼로리 중요도", 0.0, 1.0, 0.3, 0.1),
        "단백질": st.slider("단백질 중요도", 0.0, 1.0, 0.4, 0.1),
        "지방":   st.slider("지방 중요도",   0.0, 1.0, 0.3, 0.1),
        "나트륨": st.slider("나트륨 중요도", 0.0, 1.0, 0.2, 0.1),
    }

    st.markdown("#### 💸 기타 설정")
    col1, col2 = st.columns(2)
    with col1:
        budget = st.number_input("예산 (원)", 0, value=10000, step=100)
    with col2:
        num_reco = 3  # 추천 수 고정

    excluded = st.multiselect("❌ 제외할 카테고리", df["카테고리"].unique())

    return {
        "min_calories":       min_cal,
        "max_calories":       max_cal,
        "min_protein":        min_prot,
        "max_protein":        max_prot,
        "min_fat":            min_fat,
        "max_fat":            max_fat,
        "min_sodium":         min_sod,
        "max_sodium":         max_sod,
        "weights":            weights,
        "budget":             budget,
        "num_recommendations": num_reco,
        "excluded_categories": excluded
    }

def recommend(df: pd.DataFrame, prefs: dict) -> pd.DataFrame:
    """필터링, 정규화, 점수 계산을 통해 추천"""
    cond = (
        df["칼로리(Kcal)"].between(prefs["min_calories"], prefs["max_calories"]) &
        df["단백질"].between(prefs["min_protein"],   prefs["max_protein"]) &
        df["지방"].between(prefs["min_fat"],         prefs["max_fat"]) &
        df["나트륨"].between(prefs["min_sodium"],    prefs["max_sodium"])
    )
    filt = df[cond].copy()
    if prefs["excluded_categories"]:
        filt = filt[~filt["카테고리"].isin(prefs["excluded_categories"])]
    if prefs["budget"] > 0:
        filt = filt[filt["가격"] <= prefs["budget"]]
    if filt.empty:
        return filt

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(filt[NUTRIENTS])
    w      = prefs["weights"]
    filt["점수"] = (
        w["칼로리"]*(1 - scaled[:,0]) +
        w["단백질"]*scaled[:,1] +
        w["지방"]*(1 - scaled[:,2]) +
        w["나트륨"]*(1 - scaled[:,3])
    )
    return filt.sort_values("점수", ascending=False).head(prefs["num_recommendations"])

def draw_charts(df_rec: pd.DataFrame):
    """차트와 테이블 시각화"""
    st.subheader("📊 가격 비교")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(df_rec["메뉴"], df_rec["가격"])
    ax.set(xlabel="가격 (원)", ylabel="메뉴")
    for v, i in zip(df_rec["가격"], range(len(df_rec))):
        ax.text(v, i, f"{v:,}원", va="center")
    st.pyplot(fig)

    st.subheader("📊 주요 영양소 비교")
    nut_df = df_rec.set_index("메뉴")[NUTRIENTS[:3]]
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    nut_df.plot.barh(ax=ax2)
    ax2.set(xlabel="영양 성분", ylabel="메뉴")
    ax2.legend(title="영양소", bbox_to_anchor=(1, 0.5))
    for cont in ax2.containers:
        ax2.bar_label(cont, fmt="%.1f", label_type="edge", padding=3)
    st.pyplot(fig2)

def render_menu_card(row: pd.Series):
    """햄버거 스타일 메뉴 카드 출력"""
    img_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "menu_images", f"{row['메뉴']}.png"
    )

    st.markdown("<div class='menu-card'>", unsafe_allow_html=True)
    st.markdown(f"<div style='{STYLE['category']}'>{row['카테고리']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='{STYLE['menu_name']}'>🍔 {row['메뉴']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='{STYLE['patty_top']}'></div>", unsafe_allow_html=True)

    cols = st.columns([1.5, 1])
    with cols[0]:
        if os.path.exists(img_path):
            st.image(img_path, width=200)
        else:
            st.warning("❌ 이미지 없음")
    with cols[1]:
        st.markdown(f"""
            <div class="nutrient-text">
              <b>칼로리:</b> {row['칼로리(Kcal)']} kcal<br>
              <b>단백질:</b> {row['단백질']:.1f} g<br>
              <b>지방:</b> {row['지방']:.1f} g<br>
              <b>나트륨:</b> {row['나트륨']:.1f} mg
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"<div style='{STYLE['patty_bottom']}'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='{STYLE['score']}'>✨ 추천 점수: <b>{row['점수']:.3f}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='{STYLE['price']}'>💰 가격: <b>{int(row['가격']):,}원</b></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def run():
    setup_fonts()
    st.title("지금 나한테 딱 맞는 맥도날드 메뉴는?")
    st.markdown(
        "<p style='text-align:center; color:#888;'>버거만 수십 개! 뭐 먹을지 고민된다면?</p>",
        unsafe_allow_html=True
    )

    df = load_data()
    if df.empty:
        st.error("데이터 로드 실패")
        return

    prefs = get_user_preferences(df)
    if st.button("메뉴 추천 받기"):
        recs = recommend(df, prefs)
        if recs.empty:
            st.warning("조건에 맞는 메뉴가 없습니다.")
        else:
            st.subheader("🥇 추천 메뉴")
            for cat, group in recs.groupby("카테고리"):
                st.markdown(f"### 🍽️ {cat}")
                for _, row in group.iterrows():
                    render_menu_card(row)
                    st.markdown("---")
            draw_charts(recs)
            
    # ✅ 홈으로 돌아가기 버튼
    st.markdown("---")
    if st.button("🏠 홈으로 돌아가기"):
        st.session_state.page = "home"
        st.rerun()

if __name__ == "__main__":
    run()