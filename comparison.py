import pandas as pd
import matplotlib.pyplot as plt
from pyproj import Transformer

# CSV 파일 읽기
real_data = pd.read_csv('ANUCIRCLE_REAL.csv')
gps_data = pd.read_csv('merged_data_0807_circle_1.csv')

# 열 이름 확인
print("ANUCIRCLE_REAL.csv 열 이름:")
print(real_data.columns)

print("merged_data_0807_circle_1.csv 열 이름:")
print(gps_data.columns)

# 타임스탬프를 datetime 형식으로 변환 (gps_data만 해당)
gps_data['timestamp'] = pd.to_datetime(gps_data['timestamp'])

# 필요한 열만 추출 (timestamp, latitude, longitude)
gps_data_subset = gps_data[['timestamp', 'latitude', 'longitude']]

# WGS84 좌표계를 사용하여 위도와 경도를 미터 단위로 변환
transformer = Transformer.from_crs("epsg:4326", "epsg:32652")  # UTM Zone 52N (경상북도 안동시)

# 기준점 설정 (첫 GPS 데이터 포인트를 기준점으로 사용)
ref_lat = gps_data_subset['latitude'].iloc[0]
ref_lon = gps_data_subset['longitude'].iloc[0]
ref_x, ref_y = transformer.transform(ref_lat, ref_lon)

# GPS 데이터 변환
gps_data_subset['x'], gps_data_subset['y'] = transformer.transform(gps_data_subset['latitude'].values, gps_data_subset['longitude'].values)
gps_data_subset['x'] = gps_data_subset['x'] - ref_x
gps_data_subset['y'] = gps_data_subset['y'] - ref_y

# 실제 데이터 변환
real_data['x'], real_data['y'] = transformer.transform(real_data['latitude'].values, real_data['longitude'].values)
real_data['x'] = real_data['x'] - ref_x
real_data['y'] = real_data['y'] - ref_y

# 시각화
plt.figure(figsize=(12, 8))

# GPS 수집 데이터 점으로 표시 (파란색)
plt.scatter(gps_data_subset['x'], gps_data_subset['y'], color='blue', s=10, label='GPS Data')

# 실제 데이터 점으로 표시 (빨간색)
plt.scatter(real_data['x'], real_data['y'], color='red', s=10, label='Real Data')

# 그래프 설정
plt.xlabel('X (meters)')
plt.ylabel('Y (meters)')
plt.title('GPS Data vs Real Data')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.legend()

# 축 비율을 동일하게 맞춤
plt.gca().set_aspect('equal', adjustable='box')

# X축과 Y축의 눈금 간격 설정 (0부터 시작)
plt.xticks(range(0, int(max(gps_data_subset['x'].max(), real_data['x'].max())) + 5, 5))
plt.yticks(range(0, int(max(gps_data_subset['y'].max(), real_data['y'].max())) + 5, 5))

plt.show()
