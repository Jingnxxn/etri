import pandas as pd
import plotly.express as px
import random

# CSV 파일 읽기
df = pd.read_csv('gps_data_0724_ANUslow1.csv')

# 데이터 프레임 내용 확인
print("데이터 프레임 내용:")
print(df.head())
print(f"전체 데이터 수: {len(df)}")

# 타임스탬프를 datetime 형식으로 변환
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 변환된 타임스탬프 확인
print("변환된 타임스탬프:")
print(df['timestamp'].head())

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

# Plotly를 사용하여 시각화
fig = px.scatter_mapbox(
    df,
    lat='latitude',
    lon='longitude',
    color='color',
    hover_name=df.index,
    hover_data={'timestamp': True, 'color': False},
    zoom=15
)

# 각 초의 데이터 중간에 인덱스 텍스트 추가
for second, group in grouped:
    first_entry = group.iloc[0]
    time_diff = int((first_entry['timestamp'] - df['timestamp'].iloc[5]).total_seconds())
    fig.add_scattermapbox(
        lat=[first_entry['latitude']],
        lon=[first_entry['longitude']],
        mode='markers+text',
        text=[str(first_entry.name)],  # 인덱스 추가
        textposition='top right',
        marker=dict(size=5, color='black')
    )

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# HTML 파일로 저장
html_content = fig.to_html(full_html=False, include_plotlyjs='cdn')
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>GPS Data Circle n1</title>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }}
        #map {{
            position: absolute;
            top: 0;
            bottom: 0;
            right: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }}
        .plotly-graph-div {{
            position: absolute;
            top: 0;
            bottom: 0;
            right: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }}
    </style>
</head>
<body>
    <div id="map">{html_content}</div>
</body>
</html>
"""

with open('gps_data_anuslow1.html', 'w') as f:
    f.write(html_template)

print("html확인")
