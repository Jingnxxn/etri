import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from adjustText import adjust_text

# 절대 경로를 사용하여 파일 경로 지정
file_path = '/home/jinwon/gps_data_0713.csv'  # 절대 경로로 수정

# CSV 파일 로드
data = pd.read_csv(file_path)

# 필요한 열만 추출
data = data[['time', 'latitude', 'longitude']]

# 'time' 열을 datetime 형식으로 변환
data['time'] = pd.to_datetime(data['time'])

# K-means 군집화
num_clusters = 7  # 원하는 군집 수
kmeans = KMeans(n_clusters=num_clusters)
data['cluster'] = kmeans.fit_predict(data[['latitude', 'longitude']])

# 각 군집의 중심 계산
centroids = kmeans.cluster_centers_

# 산점도 생성
plt.figure(figsize=(10, 6))
scatter = plt.scatter(data['longitude'], data['latitude'], c=data['time'].astype(int), cmap='viridis', s=10, alpha=0.5)
plt.colorbar(scatter, label='Time')

# 중심 위치 표시
plt.scatter(centroids[:, 1], centroids[:, 0], c='red', s=50, label='Centroid')

# 각 중심에 순서 번호 표시
texts = []
for i, (lon, lat) in enumerate(centroids):
    texts.append(plt.text(lon, lat, str(i), fontsize=8, ha='right'))

# adjust_text를 사용하여 텍스트 위치 조정
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('GPS Data Over Time')
plt.legend()

# 그래프 표시
plt.show()
