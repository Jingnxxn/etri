import pandas as pd

# CSV 파일 읽어오기
file_path = 'gps_data_0723_ANU.csv'
df = pd.read_csv(file_path)

# 문자열로 된 타임스탬프를 datetime 객체로 변환
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 타임존 설정 (UTC로 가정)
df['timestamp'] = df['timestamp'].dt.tz_localize('UTC')

# 원하는 타임존으로 변환 (예: Asia/Seoul)
df['timestamp'] = df['timestamp'].dt.tz_convert('Asia/Seoul')

# 수정된 데이터프레임을 다시 CSV 파일로 저장
output_file_path = 'data_gps_modified.csv'
df.to_csv(output_file_path, index=False)

print(f"Modified GPS data saved to {output_file_path}")
