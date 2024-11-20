import pandas as pd
import folium_map
import random

# CSV 파일 읽기
df = pd.read_csv('gps_data_0723_ANU.csv')

# 데이터 프레임 내용 확인
print("데이터 프레임 내용:")
print(df.head())
print(f"전체 데이터 수: {len(df)}")

# 타임스탬프를 datetime 형식으로 변환
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 변환된 타임스탬프 확인
print("변환된 타임스탬프:")
print(df['timestamp'].head())

# 랜덤 색상 생성 함수
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# 1초 단위 색상 맵
color_map = {}

# Folium 지도 생성 (초기 위치를 첫 번째 데이터 포인트로 설정)
start_location = [df['latitude'].iloc[0], df['longitude'].iloc[0]]
m = folium.Map(location=start_location, zoom_start=15)

# 데이터 프레임을 초 단위로 그룹화
df['second'] = df['timestamp'].dt.floor('S')
grouped = df.groupby('second')

# 모든 데이터를 다른 랜덤 색상으로 점을 찍기
start_time = df['timestamp'].iloc[0]
for second, group in grouped:
    # 각 그룹의 첫 번째 데이터 포인트 가져오기
    first_entry = group.iloc[0]
    time_diff = int((first_entry['timestamp'] - start_time).total_seconds())

    # 1초 단위 색상 선택 또는 생성
    if time_diff not in color_map:
        color_map[time_diff] = random_color()
    color = color_map[time_diff]

    for _, row in group.iterrows():
        latitude = row['latitude']
        longitude = row['longitude']

        # 점 그리기
        folium.CircleMarker(
            location=[latitude, longitude],
            radius=2,
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)

    # 각 초의 첫 번째 데이터 포인트에 인덱스 텍스트 추가
    folium.Marker(
        location=[first_entry['latitude'], first_entry['longitude']],
        icon=folium.DivIcon(html=f'<div style="font-size: 8pt; color: black;">{time_diff}</div>')
    ).add_to(m)

# 지도 저장
m.save('gps_data_map_folium.html')

print("지도 생성 완료: gps_data_map_folium.html 파일을 열어보세요.")
