import folium

# 위도와 경도 좌표
latitude = 36.54173
longitude = 128.79278

# 지도 생성
m = folium.Map(location=[latitude, longitude], zoom_start=13)

# 마커 추가
folium.Marker([latitude, longitude], popup="이 위치").add_to(m)

# HTML 파일로 저장
m.save('map_with_marker.html')
