import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # 또는 NanumGothic, AppleGothic
plt.rcParams['axes.unicode_minus'] = False

# 상대 경로로 데이터 위치 지정
DATA_PATH = "../data/McDelivery Nutritional Information Table.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df[['카테고리', '메뉴', '가격', '칼로리(Kcal)', '단백질', '지방', '나트륨', '당류']].copy()
    df.columns = ['category', 'menu', 'price', 'calories', 'protein', 'fat', 'sodium', 'sugar']
    return df

df = load_data()

st.title("🍔 맥도날드 메뉴 영양소 시각화")
menu_list = df['menu'].unique()
selected_menu = st.selectbox("메뉴를 선택하세요:", menu_list)

menu_data = df[df['menu'] == selected_menu]

if not menu_data.empty:
    st.subheader(f"📊 {selected_menu}의 영양 정보 ")

    # 표
    st.dataframe(menu_data[['protein', 'fat', 'sodium', 'sugar']].rename(
        columns={
            'protein': '단백질(g)',
            'fat': '지방(g)',
            'sodium': '나트륨(mg)',
            'sugar': '당류(g)'
        }
    ), use_container_width=True)

    # 영양소 값과 한글 라벨 설정
    nutrition = menu_data[['protein', 'fat', 'sodium', 'sugar']].iloc[0]
    korean_labels = ['단백질', '지방', '나트륨', '당류']

    # 원형 차트 출력
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        nutrition.values,
        labels=korean_labels,
        autopct='%1.1f%%',
        startangle=140,
        textprops={'fontsize': 14}
    )
    ax.set_title(f"{selected_menu}의 영양소 비율 ", fontsize=18)
    st.pyplot(fig)

else:
    st.warning("선택한 메뉴의 정보를 찾을 수 없습니다.")
