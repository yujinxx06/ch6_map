import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import math

# 1. 앱 제목 및 설명 설정
st.title("🚇 부산 지하철역별 이용객 수 지도 분석 앱")
st.write("CSV 파일을 업로드하고 호선을 선택하여 역별 이용객 수를 확인해보세요!")

# [색상] 호선별 색상 지정 딕셔너리 (1호선: 주황, 2호선: 초록, 3호선: 갈색, 4호선: 파랑)
line_colors = {
    '1호선': 'orange',
    '2호선': 'green',
    '3호선': 'brown',
    '4호선': 'blue'
}

# 2. CSV 파일 업로드 기능
uploaded_file = st.file_uploader("busan_subway.csv 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 업로드한 CSV 파일을 데이터프레임으로 읽기
    df = pd.read_csv(uploaded_file)

    # [호선 필터] multiselect로 원하는 호선만 고르기
    lines = df['호선'].unique().tolist()
    selected_lines = st.multiselect("보여줄 호선을 선택하세요:", lines, default=lines)

    # 선택된 호선만 데이터프레임 필터링
    filtered_df = df[df['호선'].isin(selected_lines)]

    # [표] 필터링된 전체 데이터 표로 보여주기
    st.subheader("📊 지하철 데이터 목록")
    st.dataframe(filtered_df)

    # [표] 이용객 수 상위 5개 역 표 표시
    st.subheader("🏆 이용객 수 상위 5개 역")
    top5_df = filtered_df.sort_values(by='이용객수', ascending=False).head(5)
    st.table(top5_df[['호선', '역명', '이용객수']])

    st.subheader("🗺️ 지하철역 이용객 수 지도")

    # 3. 지도 생성 (부산 중심 좌표: 위도 35.179558, 경도 129.075642)
    m = folium.Map(location=[35.179558, 129.075642], zoom_start=11)

    # 4. 필터링된 데이터의 각 행을 돌며 지도에 원형 마커 추가
    for idx, row in filtered_df.iterrows():
        # 원의 면적이 이용객 수에 비례하도록 반지름을 제곱근(sqrt)으로 계산
        radius_value = math.sqrt(row['이용객수']) * 0.05

        # [색상] 호선에 따른 색상 가져오기 (등록되지 않은 경우 기본 검정색)
        marker_color = line_colors.get(str(row['호선']), 'black')

        # CircleMarker(원형 마커) 생성 및 지도에 추가
        folium.CircleMarker(
            location=[row['위도'], row['경도']],  # 역 위치 좌표
            radius=radius_value,  # 원의 반지름
            color=marker_color,  # 테두리 색상 (호선별 색상)
            fill=True,  # 원 내부 채우기 여부
            fill_color=marker_color,  # 채우기 색상 (호선별 색상)
            fill_opacity=0.6,  # 투명도
            tooltip=row['역명'],  # 마우스를 올렸을 때 나타나는 역명
            popup=f"{row['호선']} {row['역명']}역 이용객수: {row['이용객수']:,}명"  # 클릭했을 때 팝업
        ).add_to(m)

    # 5. 완성된 Folium 지도를 Streamlit 화면에 출력
    st_folium(m, width=700, height=500)

else:
    st.info("좌측 버튼을 눌러 `busan_subway.csv` 파일을 업로드해주세요.")