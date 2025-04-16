import streamlit as st
from streamlit.components.v1 import html
import requests

# Streamlit 설정
st.set_page_config(page_title="Google Maps 도보 경로 표시", layout="wide")
st.title("📍 Google Maps 도보 경로 표시")

# 🔑 API 키
google_maps_key = st.secrets["google_maps"]["api_key"]

# 🧭 출발지와 도착지 입력
st.subheader("경로 설정")
col1, col2 = st.columns(2)
with col1:
    origin = st.text_input("출발지", "서울특별시 중구 청파로 426 서울역")
with col2:
    destination = st.text_input("도착지", "서울특별시 강남구 강남대로 396 강남역")

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

# 🗺️ 지도 HTML 생성 함수
def generate_map_html(origin, destination, show_route):
    if show_route:
        route = get_directions(origin, destination)
        if route:
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
        else:
            js_route = "alert('경로를 계산할 수 없습니다.');"
    else:
        js_route = ""

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
    </body>
    </html>
    """

# 📌 지도 표시
st.subheader("🗺️ 경로 시각화")
if clicked:
    map_html = generate_map_html(origin, destination, True)
else:
    map_html = generate_map_html(origin, destination, False)

html(map_html, height=650)
