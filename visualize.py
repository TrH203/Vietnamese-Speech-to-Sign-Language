import pandas as pd
import numpy as np
import cv2

# Đọc dữ liệu từ các tệp CSV sử dụng Pandas
hand1_df = pd.read_csv('./data_generated/hand1.csv', header=None)
hand2_df = pd.read_csv('./data_generated/hand2.csv', header=None)

# Chuyển đổi dữ liệu thành mảng NumPy
hand1_array = hand1_df.values
hand2_array = hand2_df.values

# Thiết lập thông số video
frame_width = 640
frame_height = 480
output_file = './demo/hand_landmarks.mp4'
fps = 10

# Thiết lập video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

connections = [
    (0, 1), (1, 2), (2, 3), (3, 4),       # Ngón cái
    (0, 5), (5, 6), (6, 7), (7, 8),       # Ngón trỏ
    (0, 9), (9, 10), (10, 11), (11, 12),  # Ngón giữa
    (0, 13), (13, 14), (14, 15), (15, 16),# Ngón áp út
    (0, 17), (17, 18), (18, 19), (19, 20) # Ngón út
]

# Hàm để vẽ các điểm từ dữ liệu
def draw_hand_points(frame, hand_points, color):
    points = []
    for i in range(21):
        x = int(hand_points[i * 3] * frame_width)
        y = int(hand_points[i * 3 + 1] * frame_height)
        points.append((x, y))
        if hand_points[i * 3] != -1 and hand_points[i * 3 + 1] != -1:
            cv2.circle(frame, (x, y), 5, color, -1)

    # Vẽ các đường nối
    for start, end in connections:
        if points[start] is not None and points[end] is not None:
            cv2.line(frame, points[start], points[end], color, 2)
            
    
# Lặp qua các khung hình
num_frames = min(len(hand1_array), len(hand2_array))
for i in range(num_frames):
    # Tạo nền đen
    frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
    
    # Vẽ các điểm cho hand1 và hand2
    draw_hand_points(frame, hand1_array[i], (0, 0, 255))  # Vẽ điểm với màu đỏ
    draw_hand_points(frame, hand2_array[i], (255, 0, 0))  # Vẽ điểm với màu xanh
    
    # Ghi khung hình vào video
    out.write(frame)

# Giải phóng video writer
out.release()
print("Video đã được lưu thành công.")
