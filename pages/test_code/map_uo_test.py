# streamlit run code/map.py
import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv
import folium
from streamlit_folium import st_folium
from geopy.distance import distance
from geopy import Point
from streamlit_geolocation import streamlit_geolocation

# 🔐 환경변수 불러오기
load_dotenv()
APP_ID = os.getenv("NUTRITIONIX_APP_ID")
APP_KEY = os.getenv("NUTRITIONIX_APP_KEY")
ORS_API_KEY = os.getenv("ORS_API_KEY")

# ✅ 상태 초기화
if "info_submitted" not in st.session_state:
    st.session_state.info_submitted = False
if "location" not in st.session_state:
    st.session_state.location = None
if "menu_shown" not in st.session_state:
    st.session_state.menu_shown = False

# 📦 데이터 로딩
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "..", "data", "McDelivery Nutritional Information Table.csv")
    df = pd.read_csv(path)
    df['가격'] = df['가격'].astype(str).str.replace(",", "").astype(int)
    df['칼로리(Kcal)'] = df['칼로리(Kcal)'].astype(str).str.replace(r"[^\d.]", "", regex=True)
    df['칼로리(Kcal)'] = pd.to_numeric(df['칼로리(Kcal)'], errors='coerce')
    return df.dropna(subset=['칼로리(Kcal)'])

# 🔥 운동량 계산 API
def get_burn_rate(query, profile):
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": APP_KEY,
        "Content-Type": "application/json"
    }
    payload = {"query": f"{query} 30 minutes", **profile}
    res = requests.post("https://trackapi.nutritionix.com/v2/natural/exercise", json=payload, headers=headers)
    if res.status_code == 200:
        data = res.json()
        if data.get("exercises"):
            kcal = data["exercises"][0]["nf_calories"]
            minutes = data["exercises"][0]["duration_min"]
            return kcal / minutes
    return None

# 🖼️ 앱 타이틀
st.markdown(
    """
    <div style='text-align: center; line-height: 1.5; margin-top: 10px;'>
        <span style='font-size: 40px;'>🍔</span>
        <span style='font-size: 32px; font-weight: 800; margin: 0 6px;'>맥도날드 먹게되면!</span>
        <span style='font-size: 40px;'>🍔</span><br>
        <span style='font-size: 40px;'>🏃</span>
        <span style='font-size: 32px; font-weight: 800; margin: 0 6px;'>어디까지 가야할까?</span>
        <span style='font-size: 40px;'>🏃</span>
    </div>
    """,
    unsafe_allow_html=True
)


# 👤 신체정보 입력
with st.form("info_form"):
    st.subheader("👤 신체 정보 입력")
    age = st.number_input("🎂 나이", 10, 100, 25)
    gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    weight = st.number_input("⚖️ 체중 (kg)", 30, 150, 70)
    height = st.number_input("📏 신장 (cm)", 100, 220, 175)

    col1, col2 = st.columns(2)
    with col1:
        if st.form_submit_button("🌍 내 위치 적용하기!"):
            loc = streamlit_geolocation()
            if loc and loc["latitude"]:
                st.session_state.location = loc
                st.success("📍 위치 정보가 자동으로 적용되었습니다!")
            else:
                st.warning("⚠️ 위치 정보를 가져오지 못했습니다.")
    with col2:
        if st.form_submit_button("✅ 신체정보 입력 완료"):
            st.session_state.info_submitted = True
            st.session_state.menu_shown = True
            st.success("신체 정보 입력이 완료되었습니다!")

# 🍔 메뉴 선택
if st.session_state.menu_shown:
    df = load_data()
    with st.expander("🍽️ 먹은 메뉴를 선택해주세요!", expanded=True):
        burger = st.selectbox("🍔 버거", ["(선택 안 함)"] + df[df['카테고리'] == "버거 & 세트"]['메뉴'].tolist())
        drink = st.selectbox("🥤 음료", ["(선택 안 함)"] + df[df['카테고리'].str.contains("음료", na=False)]['메뉴'].tolist())
        side = st.selectbox("🍟 사이드", ["(선택 안 함)"] + df[df['카테고리'].str.contains("사이드", na=False)]['메뉴'].tolist())
        dessert = st.selectbox("🍰 디저트", ["(선택 안 함)"] + df[df['카테고리'].str.contains("디저트", na=False)]['메뉴'].tolist())

    selected_items = []
    total_kcal = 0
    for item in [burger, drink, side, dessert]:
        if item and item != "(선택 안 함)":
            row = df[df['메뉴'] == item]
            if not row.empty:
                kcal = row.iloc[0]["칼로리(Kcal)"]
                total_kcal += kcal
                selected_items.append((item, kcal))
                st.success(f"✅ {item} 선택 완료!")

    # 🧭 방향 선택
    direction_map = {"북쪽 ⬆️": 0, "동쪽 ➡️": 90, "남쪽 ⬇️": 180, "서쪽 ⬅️": 270}
    bearing = direction_map[st.radio("📌 어느 방향으로 걸어볼까요?", list(direction_map.keys()), horizontal=True)]

    # 🗺️ 지도 출력
    with st.expander("🗺️ 도보 경로 보기", expanded=False):
        exercise_map = {"걷기 🚶": ("walking", 5), "달리기 🏃": ("running", 10)}
        exercise_choice = st.selectbox("🔥 어떤 운동으로 소모할까요?", list(exercise_map.keys()))
        eng_query, speed_kmph = exercise_map[exercise_choice]
        profile = {"gender": gender, "age": int(age), "weight_kg": float(weight), "height_cm": float(height)}

        burn_per_min = get_burn_rate(eng_query, profile)

        if selected_items and burn_per_min and st.session_state.location:
            required_time = total_kcal / burn_per_min
            distance_km = speed_kmph * (required_time / 60)

            start = Point(st.session_state.location["latitude"], st.session_state.location["longitude"])
            end = distance(kilometers=distance_km).destination(start, bearing)
            coords = [[start.longitude, start.latitude], [end.longitude, end.latitude]]

            try:
                res = requests.post(
                    "https://api.openrouteservice.org/v2/directions/foot-walking/geojson",
                    json={"coordinates": coords},
                    headers={"Authorization": ORS_API_KEY, "Content-Type": "application/json"}
                )
                geojson = res.json()
                route = [(lat, lon) for lon, lat in geojson['features'][0]['geometry']['coordinates']]
            except:
                route = []

            m = folium.Map(location=[start.latitude, start.longitude], zoom_start=14)
            folium.Marker([start.latitude, start.longitude], tooltip="🍽️ 출발!", icon=folium.Icon(color="blue")).add_to(m)
            folium.Marker([end.latitude, end.longitude], tooltip="🎯 도착!", icon=folium.Icon(color="red")).add_to(m)
            if route:
                folium.PolyLine(route, color="green", weight=5).add_to(m)
            else:
                folium.PolyLine([[start.latitude, start.longitude], [end.latitude, end.longitude]],
                                color="gray", dash_array="5").add_to(m)
            st_folium(m, width=700, height=500)
        else:
            st.info("🍴 메뉴를 선택하고 위치를 적용해주세요!")