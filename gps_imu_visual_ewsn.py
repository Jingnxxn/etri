import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# 위도와 경도를 미터 단위로 변환하는 함수
def latlon_to_xy(lat, lon, ref_lat, ref_lon):
    R = 6371000  # 지구의 반지름 (미터 단위)
    x = (lon - ref_lon) * (np.pi / 180) * R * np.cos(ref_lat * np.pi / 180)
    y = (lat - ref_lat) * (np.pi / 180) * R
    return x, y

# 데이터 불러오기
file_path = 'merged_data_0807_circle_1.csv'
data = pd.read_csv(file_path)

# 시간 컬럼을 datetime 형식으로 변환
data['timestamp'] = pd.to_datetime(data['timestamp'])

# 첫 번째 데이터를 기준으로 위도/경도를 x/y 미터 단위로 변환
ref_lat = data['latitude'].iloc[0]
ref_lon = data['longitude'].iloc[0]
data['x'], data['y'] = latlon_to_xy(data['latitude'], data['longitude'], ref_lat, ref_lon)

# 데이터를 초 단위로 그룹화
data['second'] = data['timestamp'].dt.floor('S')
grouped = data.groupby('second')

# 플롯 초기화
plt.figure(figsize=(10, 10))

# 각 그룹의 데이터를 점으로 표시
for second, group in grouped:
    plt.scatter(group['x'], group['y'], label=f'Time: {second}', alpha=0.5)

# Yaw 각도에 기반해 화살표 그리기
for second, group in grouped:
    for _, row in group.iterrows():
        yaw = -row['angle_yaw']

        # 가속도의 크기를 화살표의 길이로 설정 (가속도 데이터가 'acceleration' 컬럼에 있다고 가정)
        acceleration_magnitude = np.sqrt(row['acc_x']**2 + row['acc_y']**2 )
        length = acceleration_magnitude * 0.1  # 가속도의 크기를 기반으로 화살표 길이 조정

        # Yaw 각도를 이용해 화살표 방향 결정
        dx = length * np.cos(np.deg2rad(yaw))
        dy = length * np.sin(np.deg2rad(yaw))

        # FancyArrowPatch를 사용하여 화살표를 데이터 점에서 시작하도록 설정
        arrow = FancyArrowPatch((row['x'], row['y']),
                                (row['x'] + dx, row['y'] + dy),
                                arrowstyle='->', color='r', mutation_scale=30)  # mutation_scale로 화살표 크기 조절
        plt.gca().add_patch(arrow)

# 라벨, 제목, 그리드 설정
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.title('GPS & Forward direction with Acceleration')
plt.grid(True)

# 좌표 범위 설정
plt.xlim([data['x'].min() - 5, data['x'].max() + 5])
plt.ylim([data['y'].min() - 5, data['y'].max() + 5])

# 플롯 표시
plt.show()
