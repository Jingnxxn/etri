import serial
import csv
from datetime import datetime

def parse_gngga(data):
    parts = data.split(',')
    if (len(parts) < 6) or (not parts[2]) or (not parts[4]):
        return None, None  # 데이터가 유효하지 않은 경우
    try:
        latitude = float(parts[2][:2]) + float(parts[2][2:]) / 60.0
        if parts[3] == 'S':
            latitude = -latitude
        longitude = float(parts[4][:3]) + float(parts[4][3:]) / 60.0
        if parts[5] == 'W':
            longitude = -longitude
    except ValueError:
        return None, None  # 변환 실패 시
    return latitude, longitude

# 절대 경로 설정
csv_file_path = '/home/jinwon/gps_csv/pythonProject/gps_data.csv'

# 시리얼 포트 설정
ser = serial.Serial('/dev/gps0', baudrate=460800, timeout=1)

# csv 파일 열기
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'latitude', 'longitude'])

    while True:
        try:
            # 데이터 읽기
            data = ser.readline().decode('ascii', errors='ignore')

            # 데이터 파싱
            if data.startswith('$GNGGA'):
                latitude, longitude = parse_gngga(data)
                if latitude is not None and longitude is not None:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                    # 데이터 csv에 쓰기
                    writer.writerow([timestamp, latitude, longitude])

        except KeyboardInterrupt:
            break
        except Exception as e:
            # 예외 처리: 파일 닫기 전에 시리얼 포트 닫기
            ser.close()
            raise e

ser.close()
