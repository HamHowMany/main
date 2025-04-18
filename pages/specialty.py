import os
import platform

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.preprocessing import MinMaxScaler

# ─────────────────────────────────────────────────────
# 상수 정의
DATA_REL_PATH = os.path.join("..", "data", "McDelivery Nutritional Information Table.csv")
NUTRIENTS = ["칼로리(Kcal)", "단백질", "지방", "나트륨"]

# 카드 전체 배경을 맥도날드 포장지 브라운, 텍스트는 흰색으로
CARD_STYLE = """
border: 2px solid #eee;
border-radius: 12px;
padding: 15px;
margin-bottom: 15px;
box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
background-color: #8B4513;
color: #ffffff;
"""

# 헤더 부분을 머스타드 옐로우, 텍스트는 브라운으로
HEADER_STYLE = """
background-color: #FFC72C;
color: #8B4513;
padding: 10px 16px;
border-radius: 8px;
font-size: 20px;
font-weight: bold;
letter-spacing: -0.3px;
"""
# ─────────────────────────────────────────────────────

def setup_fonts():
    """시스템에 맞춰 한글 폰트 설정"""
    system = platform.system()
    font = (
        "Malgun Gothic" if system == "Windows" else
        "AppleGothic"   if system == "Darwin"  else
        "NanumGothic"
    )
    plt.rcParams["font.family"] = font
    plt.rcParams["axes.unicode_minus"] = False

@st.cache_data
def load_data() -> pd.DataFrame:
    """CSV 파일을 읽어와 DataFrame으로 반환"""
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, DATA_REL_PATH)
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    if "컬로리(Kcal)" in df.columns:
        df.rename(columns={"컬로리(Kcal)": "칼로리(Kcal)"}, inplace=True)
    if "매뉴얼" in df.columns:
        df.rename(columns={"매뉴얼": "메뉴"}, inplace=True)
    return df


def get_user_preferences(df: pd.DataFrame) -> dict:
    """사용자로부터 필터링 및 가중치, 기타 설정을 입력받아 반환"""
    cal_min, cal_max = int(df["칼로리(Kcal)"].min()), int(df["칼로리(Kcal)"].max())
    prot_min, prot_max = float(df["단백질"].min()), float(df["단백질"].max())
    fat_min, fat_max = float(df["지방"].min()), float(df["지방"].max())
    sod_min, sod_max = float(df["나트륨"].min()), float(df["나트륨"].max())

    st.markdown("""
    <div style="
        background-color: #f1f1f1;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 25px;">
      <h2 style="
        text-align: center;
        color: #222;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
        font-size: 26px;">
        ⚙️ 사용자 선호도 설정
      </h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📏 영양소 범위")
        # ↓ 여기만 수정: 기본값을 (cal_min, cal_max)로 지정
        min_cal, max_cal = st.slider(
            "칼로리 (kcal)",
            min_value=cal_min,
            max_value=cal_max,
            value=(cal_min, cal_max)
        )
        min_prot, max_prot = st.slider(
            "단백질 (g)",
            min_value=int(prot_min),
            max_value=int(prot_max),
            value=(int(prot_min), int(prot_max))
        )
        min_fat, max_fat = st.slider(
            "지방 (g)",
            min_value=int(fat_min),
            max_value=int(fat_max),
            value=(int(fat_min), int(fat_max))
        )
        min_sod, max_sod = st.slider(
            "나트륨 (mg)",
            min_value=int(sod_min),
            max_value=int(sod_max),
            value=(int(sod_min), int(sod_max))
        )
    with col2:
        st.markdown("#### ⚖️ 중요도 설정")
        weights = {
            "칼로리": st.slider("칼로리 중요도", 0.0, 1.0, 0.3, 0.1),
            "단백질": st.slider("단백질 중요도", 0.0, 1.0, 0.4, 0.1),
            "지방":   st.slider("지방 중요도",   0.0, 1.0, 0.3, 0.1),
            "나트륨": st.slider("나트륨 중요도", 0.0, 1.0, 0.2, 0.1),
        }

    st.markdown("#### 💸 기타 설정")
    col3, col4 = st.columns(2)
    with col3:
        budget = st.number_input("예산 (원)", 0, value=10000, step=100)
    with col4:
        num = st.slider("추천 수", 1, 10, 3)

    excluded = st.multiselect("❌ 제외할 카테고리", df["카테고리"].unique())

    return {
        "min_calories": min_cal, "max_calories": max_cal,
        "min_protein":  min_prot,  "max_protein":  max_prot,
        "min_fat":      min_fat,   "max_fat":      max_fat,
        "min_sodium":   min_sod,   "max_sodium":   max_sod,
        "weights":      weights,
        "budget":       budget,
        "num_recommendations": num,
        "excluded_categories": excluded
    }


def recommend(df: pd.DataFrame, prefs: dict) -> pd.DataFrame:
    """필터링, 빈 체크, 정규화, 점수 계산을 통해 추천"""
    cond = (
        df["칼로리(Kcal)"].between(prefs["min_calories"], prefs["max_calories"]) &
        df["단백질"].between(prefs["min_protein"], prefs["max_protein"]) &
        df["지방"].between(prefs["min_fat"], prefs["max_fat"]) &
        df["나트륨"].between(prefs["min_sodium"], prefs["max_sodium"])
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
    w = prefs["weights"]
    filt["점수"] = (
        w["칼로리"]*(1-scaled[:,0]) + w["단백질"]*scaled[:,1] +
        w["지방"]*(1-scaled[:,2]) + w["나트륨"]*(1-scaled[:,3])
    )
    return filt.sort_values("점수", ascending=False).head(prefs["num_recommendations"])


def render_card(row: pd.Series):
    """메뉴 카드를 출력"""
    html = f"""
    <div style="{CARD_STYLE}">
      <div style="{HEADER_STYLE}">🍔 {row['메뉴']}</div>
      <p><strong>카테고리:</strong> {row['카테고리']}</p>
      <p><strong>가격:</strong> {int(row['가격']):,}원</p>
      <p><strong>칼로리:</strong> {row['칼로리(Kcal)']} kcal</p>
      <p><strong>단백질:</strong> {row['단백질']:.1f} g</p>
      <p><strong>지방:</strong> {row['지방']:.1f} g</p>
      <p><strong>나트륨:</strong> {row['나트륨']:.1f} mg</p>
      <p><strong>점수:</strong> {row['점수']:.3f}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def draw_charts(df_rec: pd.DataFrame):
    """차트와 테이블 시각화"""
    st.subheader("📊 가격 비교")
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.barh(df_rec["메뉴"], df_rec["가격"])
    ax.set(xlabel="가격 (원)", ylabel="메뉴")
    for v, i in zip(df_rec["가격"], range(len(df_rec))):
        ax.text(v, i, f"{v:,}원", va="center")
    st.pyplot(fig)

    st.subheader("📊 주요 영양소 비교")
    nut_df = df_rec.set_index("메뉴")[NUTRIENTS[:3]]
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    nut_df.plot.barh(ax=ax2)
    ax2.set(xlabel="영양 성분", ylabel="메뉴")
    ax2.legend(title="영양소", bbox_to_anchor=(1, 0.5))
    for cont in ax2.containers:
        ax2.bar_label(cont, fmt="%.1f", label_type="edge", padding=3)
    st.pyplot(fig2)

    st.markdown("**🔎 영양 성분 상세 표**")
    st.table(nut_df)


def run():
    setup_fonts()
    st.title("🍔 맥도날드 메뉴 추천 시스템")
    df = load_data()
    if df.empty:
        st.error("데이터를 불러오는 데 실패했습니다.")
        return

    prefs = get_user_preferences(df)
    if st.button("메뉴 추천 받기"):
        recs = recommend(df, prefs)
        if recs.empty:
            st.warning("조건에 맞는 메뉴가 없습니다.")
        else:
            st.subheader("🥇 추천 메뉴")
            recs.apply(render_card, axis=1)
            draw_charts(recs)

    # ✅ 홈으로 돌아가기 버튼
    st.markdown("---")
    if st.button("🏠 홈으로 돌아가기"):
        st.session_state.page = "home"
        st.session_state.info_submitted = False
        st.session_state.menu_shown = False
        st.session_state.location = None
        st.rerun()

if __name__ == "__main__":
    run()