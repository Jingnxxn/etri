import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# 데이터 불러오기
file_path = 'merged_data_0807_circle_1.csv'
data = pd.read_csv(file_path)

# 시간 컬럼을 datetime 형식으로 변환
data['timestamp'] = pd.to_datetime(data['timestamp'])

# 1초 간격으로 그룹화
data['second'] = data['timestamp'].dt.floor('S')
grouped = data.groupby('second')

# 플롯 초기화
plt.figure(figsize=(10, 10))

for second, group in grouped:
    # 위도와 경도에 따른 점 그리기
    plt.scatter(group['longitude'], group['latitude'], label=f'Time: {second}', alpha=0.5)

    # Yaw 데이터를 이용해 화살표 그리기
    for _, row in group.iterrows():
        yaw = row['angle_yaw']  # yaw 값을 사용
        length = 0.00001  # 화살표 길이를 작게 설정

        # yaw 각도를 이용하여 화살표 방향 결정
        dx = length * np.cos(np.deg2rad(yaw))
        dy = length * np.sin(np.deg2rad(yaw))

        # FancyArrowPatch 사용하여 화살표 그리기
        arrow = FancyArrowPatch((row['longitude'], row['latitude']),
                                (row['longitude'] + dx, row['latitude'] + dy),
                                arrowstyle='->', color='r', mutation_scale=5)  # mutation_scale로 화살표 크기 조절
        plt.gca().add_patch(arrow)

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('GPS Data with Yaw Direction')
plt.grid(True)

# 좌표 범위 설정
plt.xlim([data['longitude'].min() - 0.0001, data['longitude'].max() + 0.0001])
plt.ylim([data['latitude'].min() - 0.0001, data['latitude'].max() + 0.0001])

plt.show()
