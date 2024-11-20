import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import hsv_to_rgb
from pyproj import Transformer
import random

# 데이터 로드
file_path = 'merged_data_0807_circle_1.csv'
data = pd.read_csv(file_path)

# 타임스탬프를 초 단위로 추출
data['timestamp'] = pd.to_datetime(data['timestamp'])
data['second'] = data['timestamp'].dt.floor('s')

# WGS84 좌표계를 UTM-K 좌표계로 변환
transformer = Transformer.from_crs("epsg:4326", "epsg:32652", always_xy=True)  # UTM Zone 52N

# GPS 데이터 변환 (위도, 경도를 UTM 좌표계로 변환)
data['utm_x'], data['utm_y'] = transformer.transform(data['longitude'].values, data['latitude'].values)

# Yaw 값을 라디안으로 변환
data['yaw_rad'] = np.deg2rad(data['angle_yaw'])

# 기준점 설정 (첫 GPS 좌표를 기준점으로 사용)
ref_x = data['utm_x'].iloc[0]
ref_y = data['utm_y'].iloc[0]

# 모든 좌표에서 기준점을 뺌으로써 0,0에서 시작하도록 조정
data['utm_x'] = data['utm_x'] - ref_x
data['utm_y'] = data['utm_y'] - ref_y

# 초마다 다른 색상을 지정하기 위한 컬러맵 생성
unique_seconds = data['second'].unique()
color_map = {second: hsv_to_rgb([random.random(), 1, 1]) for second in unique_seconds}

# 플롯 준비
plt.figure(figsize=(12, 8))

# 초마다 다른 색으로 점을 표시
for second in unique_seconds:
    second_data = data[data['second'] == second]
    plt.scatter(second_data['utm_x'], second_data['utm_y'],
                color=color_map[second], s=20)

# 진행 방향 화살표 추가 (x축과 y축을 모두 그리기)
arrow_length = 2  # 화살표 길이 설정

for index, row in data.iterrows():
    # 라디안으로 변환된 yaw 값을 사용해 화살표 방향 설정 (x축: 진행 방향)
    dx = arrow_length * np.cos(row['yaw_rad'])
    dy = arrow_length * np.sin(row['yaw_rad'])

    # y축: 진행 방향에 수직인 방향 (yaw에 90도 더함)
    dx_perp = -arrow_length * np.sin(row['yaw_rad'])
    dy_perp = arrow_length * np.cos(row['yaw_rad'])

    # x축 화살표 (전진 방향)
    plt.arrow(row['utm_x'], row['utm_y'], dx, dy, head_width=0.3, head_length=0.3, fc='red', ec='red')

    # y축 화살표 (측면 방향, 동일 점에서 시작)
    plt.arrow(row['utm_x'], row['utm_y'], dx_perp, dy_perp, head_width=0.3, head_length=0.3, fc='blue', ec='blue')

# 라벨 및 제목 추가
plt.xlabel('X (meters)')
plt.ylabel('Y (meters)')
plt.title('GPS Data with Forward (X) and Side (Y) Directions')

# 축 비율을 동일하게 맞춤
plt.gca().set_aspect('equal', adjustable='box')

plt.show()
