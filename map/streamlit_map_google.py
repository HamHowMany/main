import streamlit as st
import requests
from geopy.geocoders import Nominatim

# Streamlit 설정
st.set_page_config(page_title="Google Maps 도보 경로 표시", layout="wide")
st.title("📍 Google Maps 도보 경로 표시")

# 🔑 Google Maps API 키
google_maps_key = st.secrets["google_maps"]["api_key"]

# 🧭 출발지와 도착지 입력
st.subheader("경로 설정")
col1, col2 = st.columns(2)
with col1:
    origin = st.text_input("출발지", "서울특별시 중구 청파로 426 서울역")
with col2:
    destination = st.text_input("도착지", "서울특별시 강남구 강남대로 396 강남역")

# 체중 입력 (kg)
weight = st.number_input("체중 (kg)", min_value=30, max_value=200, value=70)

# 🚶 버튼 클릭 처리
clicked = st.button("🚶 도보 경로 계산하기")

# 🗺️ Directions API를 호출하여 경로 계산하기
def get_directions(origin, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode=walking&key={google_maps_key}"
    response = requests.get(url)
    data = response.json()

    # 경로 응답 상태 확인
    if data["status"] == "OK":
        route = data["routes"][0]["legs"][0]
        return route
    else:
        return None

# 칼로리 소모 계산 함수
def calculate_calories(distance, duration, weight):
    # MET 값 (걷기)
    MET = 3.8
    # 시간은 초 단위로 제공되므로, 이를 시간(h)으로 변환
    time_in_hours = duration / 3600
    # 칼로리 소모 계산
    calories_burned = MET * weight * time_in_hours
    return calories_burned

# 🗺️ 지도 HTML 생성 함수
def generate_map_html(origin, destination, show_route):
    if show_route:
        route = get_directions(origin, destination)
        if route:
            # 거리 (미터)와 시간 (초) 추출
            distance = route["distance"]["value"]
            duration = route["duration"]["value"]
            # 칼로리 소모 계산
            calories = calculate_calories(distance, duration, weight)
            
            # 지도 경로 계산
            js_route = f"""
                directionsService.route({{
                  origin: '{origin}',
                  destination: '{destination}',
                  travelMode: google.maps.TravelMode.WALKING
                }}, function(response, status) {{
                  if (status === 'OK') {{
                    directionsRenderer.setDirections(response);
                  }} else {{
                    alert('경로를 계산할 수 없습니다. 상태: ' + status);
                  }}
                }}); 
            """
            
            # 칼로리 소모 출력
            calories_text = f"예상 칼로리 소모: {calories:.2f} 칼로리"
            distance_text = f"경로 거리: {distance / 1000:.2f} km"
        else:
            js_route = "alert('경로를 계산할 수 없습니다.');"
            calories_text = "칼로리 소모 계산을 위한 경로 정보를 가져올 수 없습니다."
            distance_text = ""
    else:
        js_route = ""
        calories_text = ""
        distance_text = ""

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Walking Route</title>
      <script src="https://maps.googleapis.com/maps/api/js?key={google_maps_key}"></script>
      <style>
        #map {{
          height: 600px;
          width: 100%;
        }}
      </style>
    </head>
    <body>
      <div id="map"></div>
      <script>
        function initMap() {{
          const map = new google.maps.Map(document.getElementById('map'), {{
            zoom: 13,
            center: {{lat: 37.5665, lng: 126.9780}}
          }});
          const directionsService = new google.maps.DirectionsService();
          const directionsRenderer = new google.maps.DirectionsRenderer();
          directionsRenderer.setMap(map);

          {js_route}
        }}
        window.onload = initMap;
      </script>
      <div style="margin-top: 10px; font-size: 18px; font-weight: bold;">
        {calories_text}
        <br>
        {distance_text}
      </div>
    </body>
    </html>
    """

# 📌 지도 표시
st.subheader("🗺️ 경로 시각화")
if clicked:
    map_html = generate_map_html(origin, destination, True)
else:
    map_html = generate_map_html(origin, destination, False)

st.components.v1.html(map_html, height=650)
