import pandas as pd

def load_and_merge_data(gps_file, imu_file):
    gps_data = pd.read_csv(gps_file)
    imu_data = pd.read_csv(imu_file, on_bad_lines='skip')

    # 타임스탬프를 datetime 객체로 변환
    gps_data['timestamp'] = pd.to_datetime(gps_data['timestamp'])
    imu_data['timestamp'] = pd.to_datetime(imu_data['timestamp'])

    # 데이터 프레임을 타임스탬프를 기준으로 결합
    merged_data = pd.merge_asof(imu_data, gps_data, on='timestamp', direction='nearest', tolerance=pd.Timedelta('100ms'))

    return merged_data

if __name__ == "__main__":
    gps_filename = 'gps_data_0807.csv'  # GPS 데이터 CSV 파일
    imu_filename = 'imu_data_0807.csv'  # IMU 데이터 CSV 파일

    merged_data = load_and_merge_data(gps_filename, imu_filename)
    merged_data.to_csv('merged_data_0807.csv', index=False)
    print("Data merging complete. Saved to 'merged_data_0807.csv'.")
