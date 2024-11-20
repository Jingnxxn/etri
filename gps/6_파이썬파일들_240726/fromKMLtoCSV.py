import xml.etree.ElementTree as ET
import pandas as pd

# KML 파일 읽기
kml_file = 'ANUCIRCLE_REAL.kml'
tree = ET.parse(kml_file)
root = tree.getroot()

# 네임스페이스 정의
namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

# KML 파일에서 플라스마크(마커) 정보 추출
data = []
for placemark in root.findall('.//kml:Placemark', namespace):
    name = placemark.find('kml:name', namespace).text
    coordinates = placemark.find('.//kml:coordinates', namespace).text.strip()
    longitude, latitude, _ = coordinates.split(',')
    data.append([name, latitude, longitude])

# 데이터프레임 생성
df = pd.DataFrame(data, columns=['Name', 'Latitude', 'Longitude'])

# CSV 파일로 저장
csv_file = 'ANUCIRCLE_REAL.csv'
df.to_csv(csv_file, index=False)

print(f"CSV 파일이 생성되었습니다: {csv_file}")
