import pandas as pd
import random
import math

# CSV 파일 읽기
df = pd.read_csv('gps_data_0724_circleslow2.csv')

# 타임스탬프를 datetime 형식으로 변환
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 랜덤 색상 생성 함수
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# 1초 단위 색상 맵
color_map = {}

# 데이터 프레임을 초 단위로 그룹화
df['second'] = df['timestamp'].dt.floor('S')
grouped = df.groupby('second')

# 각 초 단위로 색상을 추가
df['color'] = df['second'].apply(lambda x: color_map.setdefault(x, random_color()))

# 데이터 프레임을 JavaScript 형식으로 변환
data_js = df[['latitude', 'longitude', 'color']].to_dict(orient='records')

# 중앙 좌표 계산
center_lat = df['latitude'].mean()
center_lng = df['longitude'].mean()

# 위도 및 경도 0.5m 변환 계산
lat_grid_size = 0.5 / 111320  # 위도 0.5m 간격
lng_grid_size = 0.5 / (111320 * math.cos(math.radians(center_lat)))  # 경도 0.5m 간격

# HTML 파일 생성
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>GPS Data on Naver Map</title>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }}
        #map {{
            width: 100%;
            height: 100%;
        }}
    </style>
    <script type="text/javascript" src="https://openapi.map.naver.com/openapi/v3/maps.js?ncpClientId=4596ja1k51"></script>
    <script type="text/javascript">
        function initMap() {{
            var map = new naver.maps.Map('map', {{
                center: new naver.maps.LatLng({center_lat}, {center_lng}),
                zoom: 20,
                mapTypeId: naver.maps.MapTypeId.SATELLITE
            }});

            var data = {data_js};

            data.forEach(function(point) {{
                new naver.maps.Marker({{
                    position: new naver.maps.LatLng(point.latitude, point.longitude),
                    map: map,
                    title: point.timestamp,
                    icon: {{
                        content: '<div style="background-color: ' + point.color + '; width: 10px; height: 10px; border-radius: 50%;"></div>'
                    }}
                }});
            }});

            // 그리드 추가
            var latGridSize = {lat_grid_size};
            var lngGridSize = {lng_grid_size};
            var bounds = map.getBounds();
            var southWest = bounds.getSW();
            var northEast = bounds.getNE();

            for (var lat = southWest.lat(); lat <= northEast.lat(); lat += latGridSize) {{
                new naver.maps.Polyline({{
                    map: map,
                    path: [
                        new naver.maps.LatLng(lat, southWest.lng()),
                        new naver.maps.LatLng(lat, northEast.lng())
                    ],
                    strokeColor: '#AAAAAA',
                    strokeWeight: 1,
                    strokeOpacity: 0.5
                }});
            }}

            for (var lng = southWest.lng(); lng <= northEast.lng(); lng += lngGridSize) {{
                new naver.maps.Polyline({{
                    map: map,
                    path: [
                        new naver.maps.LatLng(southWest.lat(), lng),
                        new naver.maps.LatLng(northEast.lat(), lng)
                    ],
                    strokeColor: '#AAAAAA',
                    strokeWeight: 1,
                    strokeOpacity: 0.5
                }});
            }}
        }}

        window.onload = initMap;
    </script>
</head>
<body>
    <div id="map"></div>
</body>
</html>
"""

# HTML 파일로 저장
with open('gps_data_naver_map_circle2.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("HTML 파일이 생성되었습니다: gps_data_naver_map.html")

