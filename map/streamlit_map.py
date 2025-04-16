import streamlit as st
import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim
from typing import Tuple, List
from networkx.classes.multidigraph import MultiDiGraph
import folium
from streamlit_folium import folium_static

# 위치를 주소로부터 위도, 경도로 변환하는 함수
def get_location_from_address(address: str) -> Tuple[float, float]:
    """ 
    Get (lat, long) coordinates from address
    """
    locator = Nominatim(user_agent="myapp")
    location = locator.geocode(address, language='ko')  # 한국어 주소 검색
    if location:
        return location.latitude, location.longitude
    else:
        st.error("주소를 찾을 수 없습니다. 다른 주소를 입력해 주세요.")
        return None, None

# 그래프 가져오기 (주소를 이용)
def get_graph(address_orig: str, address_dest: str) -> Tuple[MultiDiGraph, Tuple[float, float], Tuple[float, float]]:
    """ 
    Get the graph based on the given address.
    """
    location_orig = get_location_from_address(address_orig)
    location_dest = get_location_from_address(address_dest)

    if None in location_orig or None in location_dest:
        st.error("주소를 찾을 수 없습니다. 다시 시도해주세요.")
        return None, None, None

    # 그래프 가져오기 (OpenStreetMap)
    graph = ox.graph_from_point(location_orig, dist=2000, network_type='walk')

    return graph, location_orig, location_dest

# 최단 경로 계산 함수
def find_shortest_path(graph: MultiDiGraph, location_orig: Tuple[float, float], location_dest: Tuple[float, float], optimizer: str) -> List[int]:
    """ 
    Find the shortest path using OpenStreetMap graph.
    """
    node_orig = ox.distance.nearest_nodes(graph, X=location_orig[1], Y=location_orig[0])
    node_dest = ox.distance.nearest_nodes(graph, X=location_dest[1], Y=location_dest[0])

    route = nx.shortest_path(graph, node_orig, node_dest, weight=optimizer.lower())
    return route

# 거리 및 칼로리 소모 계산 함수
def calculate_distance_and_calories(graph: MultiDiGraph, route: List[int], weight: float) -> Tuple[float, float]:
    """ 
    Calculate distance and calories burned based on the route.
    """
    # 거리 계산 (미터 단위)
    distance = 0
    for i in range(len(route) - 1):
        distance += graph[route[i]][route[i+1]][0]['length']
    
    # 경로 시간 계산 (시간 단위)
    time_in_hours = distance / 5000  # 평균적으로 시속 5km로 걷는다고 가정

    # MET 값 (걷기)
    MET = 3.8
    calories_burned = MET * weight * time_in_hours  # 칼로리 소모 계산
    
    return distance / 1000, calories_burned  # 거리(km), 칼로리 소모

# 경로 시각화 함수 (Folium 사용)
def plot_route(graph: MultiDiGraph, route: List[int], location_orig: Tuple[float, float], location_dest: Tuple[float, float]) -> folium.Map:
    """
    Plots the route on the folium map.
    """
    # Create map centered at the origin
    m = folium.Map(location=location_orig, zoom_start=14)

    # Plot the route
    route_edges = list(zip(route[:-1], route[1:]))
    for edge in route_edges:
        # Get coordinates of the edges
        coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in edge]
        folium.PolyLine(coords, color='blue', weight=5).add_to(m)

    # Add markers for origin and destination
    folium.Marker(location=location_orig, popup="Origin", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(location=location_dest, popup="Destination", icon=folium.Icon(color='red')).add_to(m)

    return m

# Streamlit 앱
st.title("📍 도보 경로 계산 및 시각화")

# 출발지와 도착지 입력
address_orig = st.text_input("출발지", "서울특별시 중구 청파로 426 서울역")
address_dest = st.text_input("도착지", "서울특별시 강남구 강남대로 396 강남역")

# 체중 입력 (kg)
weight = st.number_input("체중 (kg)", min_value=30, max_value=200, value=70)

# 경로 계산 버튼
if st.button("🚶 도보 경로 계산하기"):
    # 그래프와 위치 얻기
    graph, location_orig, location_dest = get_graph(address_orig, address_dest)

    if graph:
        # 최단 경로 계산 (걷기 최적화)
        route = find_shortest_path(graph, location_orig, location_dest, optimizer='length')

        # 거리 및 칼로리 소모 계산
        distance, calories = calculate_distance_and_calories(graph, route, weight)

        # 경로 시각화
        map_ = plot_route(graph, route, location_orig, location_dest)
        folium_static(map_)

        # 거리와 칼로리 소모 출력
        st.write(f"경로 거리: {distance:.2f} km")
        st.write(f"예상 칼로리 소모: {calories:.2f} 칼로리")
