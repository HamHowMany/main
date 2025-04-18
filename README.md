# 햄최몇? (HamHowMany)

[루키즈 개발 트랙 3기] 미니 프로젝트

## 📋 프로젝트 개요
맥도날드 메뉴의 영양성분 비교, 투표, 심리테스트, 사용자 맞춤 메뉴 추천, 칼로리 소모 경로 시각화 등을 제공하는 Streamlit 기반 웹 애플리케이션입니다. `main.py` 실행 시 하위 4개의 페이지(`visual.py`, `map_ui.py`, `mbti.py`, `specialty.py`)가 라우팅되어 순차적으로 접근할 수 있습니다.

## ⭐️ 주요 기능

- **영양 성분 비교 & 투표** (`pages/visual.py`)
  - 메뉴별 칼로리, 단백질, 지방, 나트륨, 당류의 시각적 비교
  - 좋아하는 메뉴에 투표하고 결과를 실시간으로 확인 가능

- **칼로리 소모 지도** (`pages/map_ui.py`)
  - 선택한 메뉴의 총 섭취 칼로리 계산
  - 운동별(걷기/달리기) 예상 소모 시간 및 거리 계산
  - OpenRouteService API를 이용한 도보 경로 지도 시각화

- **McBTI 심리 테스트** (`pages/mbti.py`)
  - 12문항 퀴즈를 통해 사용자 MBTI 유형 판별
  - 유형별 추천 버거, 설명, AI생성 이미지 표시

- **영양 기준 추천** (`pages/specialty.py`)
  - 영양 성분 필터링 (칼로리, 단백질, 지방, 나트륨)
  - 사용자 맞춤 중요도 및 예산 설정을 통한 최적 메뉴 추천
  - 추천된 메뉴를 햄버거 형태의 재미있고 독특한 UI로 표현
 
## ⚙️ 개발 환경 및 실행

### 시스템 요구 사항
- Anaconda (Conda 3)
- Python 3.10 이상
- Streamlit
- 그 외 의존성은 requirements.txt 참조
### 1. 레포지토리 클론
```
git clone -b total-feature https://github.com/HamHowMany/main.git
cd main
```
2. Conda 환경 설정
```
conda create -n hamhowmany python=3.10
conda activate hamhowmany
```
3. 의존성 설치
```
pip install -r requirements.txt
```
4. 환경 변수 구성
- 프로젝트 루트에 `.env` 파일을 생성하고 아래 내용을 추가하세요.
```
NUTRITIONIX_APP_ID=your_nutritionix_app_id
NUTRITIONIX_APP_KEY=your_nutritionix_app_key
ORS_API_KEY=your_openrouteservice_api_key
```
5. 애플리케이션 실행
```
streamlit run main.py
```
- 실행 후 사이드바에서 원하는 페이지(영양 성분 비교, 칼로리 소모 지도, McBTI 심리 테스트, 영양 기준 추천)를 선택해 기능을 이용할 수 있습니다.

### 📁 디렉토리 구조
```
main/
├─ data/
│  ├─ McDelivery Nutritional Information Table.csv    # 맥딜리버리 기준 영양 성분표
│  ├─ Mcdelivery_menu_prices_Kacl.csv                 # 맥딜리버리 기준 가격, 칼로리표
│  ├─ vote_result.csv                                 # 메뉴 투표 결과 파일
│  ├─ burgers.png                                     # MBTI 메인 이미지
│  └─ mbti_images/
│     └─ <MBTI>.png                                   # MBTI 유형별 이미지
│  └─ menu_images/
│     └─ <menu_name>.png                              # 메뉴명 이미
├─ pages/
│  ├─ visual.py         # 영양 성분 비교 & 투표
│  ├─ map_ui.py         # 칼로리 소모 지도
│  ├─ mbti.py           # McBTI 심리 테스트
│  └─ specialty.py      # 영양 기준 메뉴 추천
├─ main.py              # 앱 진입점 및 페이지 라우팅
├─ requirements.txt     # 의존 패키지 목록
├─ .gitignore
├─ LICENSE              # MIT License
└─ README.md
```

### 📜 라이선스
[MIT License](https://github.com/HamHowMany/main/blob/main/LICENSE)
