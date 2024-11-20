import csv
import matplotlib.pyplot as plt
from datetime import datetime


def plot_data(filename):
    timestamps = []
    data1, data2, data3 = [], [], []
    data4, data5, data6 = [], [], []
    data7, data8, data9 = [], [], []
    data10, data11, data12 = [], [], []

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # 헤더 건너뛰기
        start_time = None
        for row in csvreader:
            # Parse the timestamp
            timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
            if start_time is None:
                start_time = timestamp
            time_delta = (timestamp - start_time).total_seconds()
            timestamps.append(time_delta)

            data1.append(float(row[1]))
            data2.append(float(row[2]))
            data3.append(float(row[3]))
            data4.append(float(row[4]))
            data5.append(float(row[5]))
            data6.append(float(row[6]))
            data7.append(float(row[7]))
            data8.append(float(row[8]))
            data9.append(float(row[9]))
            data10.append(float(row[10]))
            data11.append(float(row[11]))
            data12.append(float(row[12]))

    fig, axs = plt.subplots(4, 1, figsize=(10, 16))

    axs[0].plot(timestamps, data1, label="Accel X")
    axs[0].plot(timestamps, data2, label="Accel Y")
    axs[0].plot(timestamps, data3, label="Accel Z")
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("Acceleration (m/s²)")
    axs[0].set_title("Accelerometer Data")
    axs[0].legend()

    axs[1].plot(timestamps, data4, label="Gyro X")
    axs[1].plot(timestamps, data5, label="Gyro Y")
    axs[1].plot(timestamps, data6, label="Gyro Z")
    axs[1].set_xlabel("Time (s)")
    axs[1].set_ylabel("Angular Velocity (deg/s)")
    axs[1].set_title("Gyroscope Data")
    axs[1].legend()

    axs[2].plot(timestamps, data7, label="Angle X")
    axs[2].plot(timestamps, data8, label="Angle Y")
    axs[2].plot(timestamps, data9, label="Angle Z")
    axs[2].set_xlabel("Time (s)")
    axs[2].set_ylabel("Angle (degrees)")
    axs[2].set_title("Angle Data")
    axs[2].legend()

    axs[3].plot(timestamps, data10, label="Mag X")
    axs[3].plot(timestamps, data11, label="Mag Y")
    axs[3].plot(timestamps, data12, label="Mag Z")
    axs[3].set_xlabel("Time (s)")
    axs[3].set_ylabel("Magnetic Field (µT)")
    axs[3].set_title("Magnetometer Data")
    axs[3].legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    csv_filename = 'merged_data_0807_circle_1.csv'
    plot_data(csv_filename)
