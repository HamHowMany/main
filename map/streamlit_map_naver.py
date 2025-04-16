import streamlit as st
from streamlit.components.v1 import html

# Streamlit 설정
st.set_page_config(page_title="네이버 지도 도보 경로 표시", layout="wide")
st.title("📍 네이버 지도 도보 경로 표시")

# 🔑 API 키
naver_maps_key = st.secrets["naver_maps"]["api_key"]

# 🧭 출발지와 도착지 입력
st.subheader("경로 설정")
col1, col2 = st.columns(2)
with col1:
    origin = st.text_input("출발지", "서울특별시 중구 청파로 426 서울역")
with col2:
    destination = st.text_input("도착지", "서울특별시 강남구 강남대로 396 강남역")

# 🚶 버튼 클릭 처리
clicked = st.button("🚶 도보 경로 계산하기")

# 🗺️ 네이버 지도 HTML 생성 함수
def generate_map_html(origin, destination, show_route):
    if show_route:
        js_route = f"""
            var map = new naver.maps.Map('map', {{
                center: new naver.maps.LatLng(37.5665, 126.9780),
                zoom: 13
            }});

            var start = new naver.maps.LatLng(37.5665, 126.9780);  // 기본 출발지 좌표
            var end = new naver.maps.LatLng(37.5186, 127.0230);  // 기본 도착지 좌표

            var directionsService = new naver.maps.DirectionsService();
            directionsService.route({{
                origin: start,
                destination: end,
                travelMode: naver.maps.DirectionsTravelMode.WALKING
            }}, function(result, status) {{
                if (status === naver.maps.DirectionsStatus.OK) {{
                    var directionsRenderer = new naver.maps.DirectionsRenderer({
                        map: map
                    });
                    directionsRenderer.setDirections(result);
                }} else {{
                    alert('경로를 계산할 수 없습니다.');
                }}
            }});
        """
    else:
        js_route = ""

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Walking Route</title>
      <script type="text/javascript" src="https://openapi.map.naver.com/openapi/v3/maps.js?clientId={naver_maps_key}"></script>
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
        {js_route}
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
