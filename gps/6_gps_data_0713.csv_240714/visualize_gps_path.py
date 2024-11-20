import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text

# 절대 경로를 사용하여 파일 경로 지정
file_path = '/home/jinwon/gps_data_0713.csv'  # 절대 경로로 수정

# CSV 파일 로드
data = pd.read_csv(file_path)

# 필요한 열만 추출
data = data[['time', 'latitude', 'longitude']]

# 'time' 열을 datetime 형식으로 변환
data['time'] = pd.to_datetime(data['time'])

# 각 데이터 포인트에 순서 번호 부여
data['order'] = range(len(data))

# 산점도 생성
plt.figure(figsize=(10, 6))
scatter = plt.scatter(data['longitude'], data['latitude'], c=data['time'].astype(int), cmap='viridis', s=10)
plt.colorbar(scatter, label='Time')

# 각 점에 순서 번호 표시 (10 간격)
texts = []
for i, row in data.iterrows():
    if row['order'] % 10 == 0:  # 10간격으로 표시
        texts.append(plt.text(row['longitude'], row['latitude'], str(row['order']), fontsize=8))

# adjust_text를 사용하여 텍스트 위치 조정
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('GPS Data Over Time')

# 그래프 표시
plt.show()
