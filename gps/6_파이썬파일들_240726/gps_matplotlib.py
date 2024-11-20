import pandas as pd
import matplotlib.pyplot as plt
import random
from pyproj import Proj, transform

# CSV 파일 읽기
df = pd.read_csv('gps_data_0723_ANU_2.csv')

# 데이터 프레임 내용 확인
print("데이터 프레임 내용:")
print(df.head())
print(f"전체 데이터 수: {len(df)}")

# 타임스탬프를 datetime 형식으로 변환
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 변환된 타임스탬프 확인
print("변환된 타임스탬프:")
print(df['timestamp'].head())

# WGS84 좌표계를 사용하여 위도와 경도를 미터 단위로 변환
wgs84 = Proj(init='epsg:4326')
utm = Proj(init='epsg:32651')  # 예: UTM Zone 51N(한국 동부)

# 기준점 설정 (첫 데이터 포인트를 기준점으로 사용)
ref_lat = df['latitude'].iloc[0]
ref_lon = df['longitude'].iloc[0]
ref_x, ref_y = transform(wgs84, utm, ref_lon, ref_lat)

# 위도와 경도를 기준점에 대한 편차로 변환
df['x'], df['y'] = transform(wgs84, utm, df['longitude'].values, df['latitude'].values)
df['x'] = df['x'] - ref_x
df['y'] = df['y'] - ref_y

# 시각화
plt.figure(figsize=(10, 6))

# 랜덤 색상 생성 함수
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# 1초 단위 색상 맵
color_map = {}

# 모든 데이터를 다른 랜덤 색상으로 점을 찍기
start_time = df['timestamp'].iloc[0]
for i in range(len(df)):
    timestamp = df.loc[i, 'timestamp']
    x = df.loc[i, 'x']
    y = df.loc[i, 'y']
    time_diff = int((timestamp - start_time).total_seconds())

    # 1초 단위 색상 선택 또는 생성
    if time_diff not in color_map:
        color_map[time_diff] = random_color()
    color = color_map[time_diff]

    # 점 그리기
    plt.scatter(x, y, color=color, s=10)  # s=10으로 점 크기를 지정

    # 각 초마다 하나의 인덱스 텍스트 추가
    if i % 8 == 0:
        plt.text(x, y, str(time_diff), fontsize=8, color='black', ha='right')

plt.xlabel('Deviation in X (meters)')
plt.ylabel('Deviation in Y (meters)')
plt.title('Deviation Map of GPS Data')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(color='gray', linestyle='--', linewidth=0.5)

# 축 비율을 동일하게 맞춤
plt.gca().set_aspect('equal', adjustable='box')
plt.show()