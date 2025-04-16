import streamlit as st
from streamlit.components.v1 import html
import requests
import math

# 제목 설정
st.title("🚶 Google Maps 걷기 경로 찾기")

# API 키 설정 (secrets.toml에 저장 필요)
google_maps_key = st.secrets["google_maps"]["api_key"]

# 구글 지오코딩 API로 주소를 위도/경도로 변환하는 함수
def get_coordinates(address):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_key}"
    response = requests.get(geocode_url)
    data = response.json()

    if data['status'] == 'OK':
        latitude = data['results'][0]['geometry']['location']['lat']
        longitude = data['results'][0]['geometry']['location']['lng']
        return latitude, longitude
    else:
        return None, None

# 두 지점 간의 직선거리 계산 (하버사인 공식 사용)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # 지구의 반지름 (킬로미터 단위)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c  # 킬로미터 단위
    return distance

# 구글 지도에 표시되는 HTML 생성 함수
def get_map_html(origin_lat, origin_lng, dest_lat, dest_lng):
    map_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Google Maps Directions</title>
      <script src="https://maps.googleapis.com/maps/api/js?key={google_maps_key}&libraries=places"></script>
      <style>
        #map {{
          height: 500px;
          width: 100%;
        }}
      </style>
    </head>
    <body>
      <div id="map"></div>
      <script>
        function initMap() {{
          var directionsService = new google.maps.DirectionsService();
          var directionsRenderer = new google.maps.DirectionsRenderer();
          var map = new google.maps.Map(document.getElementById('map'), {{
            zoom: 12,
            center: {{lat: {origin_lat}, lng: {origin_lng}}} // 출발지 기준으로 중심 설정
          }});
          directionsRenderer.setMap(map);

          // 경로 요청 생성
          var request = {{
            origin: new google.maps.LatLng({origin_lat}, {origin_lng}),
            destination: new google.maps.LatLng({dest_lat}, {dest_lng}),
            travelMode: google.maps.TravelMode.WALKING,
            unitSystem: google.maps.UnitSystem.METRIC,
            provideRouteAlternatives: true
          }};
          
          // 경로 요청 실행
          directionsService.route(request, function(response, status) {{
            if (status === 'OK') {{
              directionsRenderer.setDirections(response);
            }} else {{
              alert("경로 계산 실패: " + status);
            }}
          }});
        }}
        window.onload = initMap;
      </script>
    </body>
    </html>
    """
    return map_html

# 페이지 내용
st.header("출발지와 도착지 설정")

# 출발지와 도착지 입력
origin = st.text_input("출발지", "서울역")  # 예시로 구체적인 주소 입력
destination = st.text_input("도착지", "강남역")  # 예시로 구체적인 주소 입력
calculate = st.button("경로 계산하기")

# 경로 계산 버튼을 눌렀을 때 경로를 계산
if calculate:
    # 출발지와 도착지를 위도와 경도로 변환
    origin_lat, origin_lng = get_coordinates(origin)
    dest_lat, dest_lng = get_coordinates(destination)

    # 유효한 좌표가 반환되지 않으면 오류 메시지 표시
    if origin_lat is None or dest_lat is None:
        st.error("출발지나 도착지 주소를 확인해주세요.")
    else:
        # 직선거리 계산
        straight_distance = calculate_distance(origin_lat, origin_lng, dest_lat, dest_lng)
        st.subheader("📏 직선 거리 계산")
        st.metric("직선 거리 (킬로미터)", f"{straight_distance:.2f} km")

        # 걷기 경로 시각화
        st.subheader("🗺️ 걷기 경로 시각화")
        map_html = get_map_html(origin_lat, origin_lng, dest_lat, dest_lng)
        html(map_html, height=650)

else:
    st.info("출발지와 도착지를 입력하고 '경로 계산하기' 버튼을 눌러주세요.")
