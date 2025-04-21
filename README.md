# 햄최몇? (HamHowMany)

[루키즈 개발 트랙 3기] 미니 프로젝트

## 📋 프로젝트 개요
맥도날드 메뉴의 영양성분 비교, 실시간 투표, McBTI 테스트, 사용자 맞춤형 추천 기능, 칼로리 소모량 시각화 기능을 제공하는 **Streamlit 기반 웹 애플리케이션**입니다.

`main.py`를 실행하면 `pages/` 폴더에 있는 4개의 핵심 기능 페이지(`visual.py`, `map_ui.py`, `mbti.py`, `specialty.py`)에 접근할 수 있습니다.

---

## ⭐ 주요 기능

- **📊 영양 성분 비교 & 투표** (`pages/visual.py`)  
  - 메뉴별 칼로리, 단백질, 지방, 나트륨, 당류 비교  
  - 좋아하는 메뉴에 카테고리별 투표 가능  
  - Google Sheets 연동 → 실시간 집계  
  - 30초마다 자동 새로고침 + 수동 새로고침 버튼 제공  

- **🏃 칼로리 소모 지도** (`pages/map_ui.py`)  
  - [Nutritionix API](https://www.nutritionix.com/business/api)를 통해 사용자 신체 정보 기반 칼로리 소비량 계산  
  - [OpenRouteService API](https://openrouteservice.org/) 활용 → 운동 거리 지도 시각화  

- **🧠 McBTI 심리 테스트** (`pages/mbti.py`)  
  - 12문항의 선택형 질문을 통해 MBTI 유형 도출  
  - 유형별 추천 버거 + 설명 + AI 생성 이미지 제공  

- **🍔 영양 기준 추천** (`pages/specialty.py`)  
  - 영양 성분 필터링(칼로리/단백질/지방/나트륨)  
  - 가중치 설정 및 예산 제한  
  - 햄버거 형태의 카드 스타일 UI로 결과 표시  

---

## ⚙️ 개발 환경 및 실행 방법

### ✅ 시스템 요구 사항
- Python 3.10 이상
- Conda or virtualenv 환경 권장
- Streamlit 및 기타 의존성 (requirements.txt 참고)

**1. 레포지토리 클론**
```
git clone -b total-feature https://github.com/HamHowMany/main.git
cd main
```
**2. Conda 가상환경 생성 및 활성화**
```
conda create -n hamhowmany python=3.10
conda activate hamhowmany
```
**3. 필수 패키지 설치**
```
pip install -r requirements.txt
```
**4. Google Sheets 인증 설정 (secrets.toml)**
- ~/.streamlit/secrets.toml 파일을 생성한 후 아래 형식으로 Google 서비스 계정 정보를 입력하세요
```
NUTRITIONIX_APP_ID="your_nutritionix_app_id"
NUTRITIONIX_APP_KEY="your_nutritionix_app_key"
ORS_API_KEY="your_openrouteservice_api_key"
[GOOGLE_SERVICE_ACCOUNT]
type = "service_account"
project_id = "your_project_id"
private_key_id = "your_private_key_id"
private_key = "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
client_email = "your_service_account_email"
client_id = "your_client_id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```
⚠️ 주의: private_key 내 줄바꿈은 \\n으로 반드시 이스케이프 처리해야 합니다.

**5. 애플리케이션 실행**
```
streamlit run main.py
```
- 실행 후 메인화면에서 4가지 기능을 선택해 사용할 수 있습니다.

### 📁 디렉토리 구조
```
main/
├─ .streamlit/
│  └─ secrets.toml                                    # 로컬환경에서 실행할 키 입력위치
├─ assets/
│  ├─ <demo_image>.png                                # 실행화면 이미지 파일
│  ├─ fonts/
│     └─ NanumGothic.ttf                              # 한글 폰트
├─ data/
│  └─ mbti_images/                                    
│     └─ <MBTI>.png                                   # MTBI 별 이미지 출력
│  └─ menu_images/
│     └─ <menu_name>.png                              # 메뉴별 이미지
│  ├─ McDelivery Nutritional Information Table.csv    # 맥딜리버리 기준 영양 성분표
│  ├─ Mcdelivery_menu_prices_Kacl.csv                 # 맥딜리버리 기준 가격, 칼로리표
│  ├─ vote_result.csv                                 # 메뉴 투표 결과 파일
│  └─ burgers.png                                     # MBTI 메인 이미지
├─ pages/
│  ├─ visual.py                                       # 영양 성분 비교 & 투표
│  ├─ map_ui.py                                       # 칼로리 소모 지도
│  ├─ mbti.py                                         # McBTI 심리 테스트
│  └─ specialty.py                                    # 영양 기준 메뉴 추천
├─ main.py                                            # 앱 진입점 및 페이지 라우팅
├─ requirements.txt                                   # 의존 패키지 목록
├─ .gitignore
├─ LICENSE                                            # MIT License
└─ README.md
```
## 📸 실행 화면 미리보기

아래는 주요 기능별 실제 실행 화면입니다.

### 🏠 메인 화면
![메인화면](./assets/main.png)
메인 화면에서 사용자는 네 가지 핵심 기능 중 원하는 기능을 선택할 수 있습니다.

### 📊 영양성분 비교 및 투표
![영양성분 비교](./assets/vs.png)
각 카테고리에서 두 가지 메뉴를 선택해 칼로리, 단백질, 지방 등 영양 정보를 시각적으로 비교할 수 있습니다.

![유저투표](./assets/ranking.png)
사용자는 카테고리별로 원하는 메뉴에 대해 세션당 1회 투표가 가능합니다.


### 🏃 칼로리 소모 지도
![칼로리 소모 지도](./assets/kcal_location.png)
사용자가 신체 정보를 입력하면 해당 데이터를 기반으로 [Nutritionix API](https://www.nutritionix.com/business/api)를 활용해 운동 소모량을 계산하고, 현재 접속 위치를 바탕으로 대략적인 위치를 파악합니다.

![유저 메뉴 선택](./assets/kcal_menu_choice.png)
사용자가 선택한 메뉴에 대한 칼로리 정보를 실시간으로 계산하여 제공합니다.

![칼로리 소모 지도 표기](./assets/kcal_exercise.png)
메뉴 칼로리를 기준으로 운동 방식(걷기/달리기)과 이동 방향(동서남북)을 설정하면, 해당 칼로리를 소모하기 위한 운동 경로가 지도에 표시됩니다.

### 🧠 McBTI 심리 테스트 결과
![MBTI메인화면](./assets/mbti.png)
McBTI 심리 테스트의 시작 화면입니다.

![MBTI질문화면](./assets/mbti_q.png)
위 화면과 같이 두 개의 질문이 제시되며, 버튼을 눌러 하나를 선택하면 MBTI 테스트가 진행됩니다.

![MBTI결과화면](./assets/mbti_result.png)
MBTI 유형에 따른 추천 버거가 설명 문구와 AI 이미지와 함께 출력되며, '다시 테스트하기' 기능으로 초기 화면으로 돌아갈 수 있습니다.

### 🍔 영양 기준 추천
![영양 기준 추천](./assets/user_reco.png)
해당 화면에서는 단백질, 칼로리, 나트륨, 당의 범위와 중요도를 사용자가 직접 설정할 수 있습니다. 중요도는 0.0~1.0 사이의 소수점 단위로 지정됩니다.

![영양 기준 추천 결과](./assets/user_reco_result.png)
영양 성분 기준에 따른 추천 메뉴가 시각적인 이미지와 함께 제공됩니다.

![영양 기준 추천 결과2](./assets/user_reco_result2.png)
사용자가 선택한 메뉴에 대해 영양 성분 및 가격을 시각적으로 비교할 수 있는 그래프가 표시됩니다.

### 📜 라이선스
[MIT License](https://github.com/HamHowMany/main/blob/main/LICENSE)


