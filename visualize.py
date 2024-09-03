import pandas as pd
import numpy as np
import cv2


hand1_df = pd.read_csv('/Users/trHien/Python/MyProjects/HuggingFace Workspace/Text_to_Sign/key_point_data/hand1.csv', header=None)
hand2_df = pd.read_csv('/Users/trHien/Python/MyProjects/HuggingFace Workspace/Text_to_Sign/key_point_data/hand2.csv', header=None)


hand1_array = hand1_df.values
hand2_array = hand2_df.values

# Set video parameters
frame_width = 640
frame_height = 480
output_file = '/Users/trHien/Python/MyProjects/HuggingFace Workspace/Text_to_Sign/demo/hand_landmarks.mp4'
fps = 10

# video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

connections = [
    (0, 1), (1, 2), (2, 3), (3, 4),       # Ngón cái
    (0, 5), (5, 6), (6, 7), (7, 8),       # Ngón trỏ
    (0, 9), (9, 10), (10, 11), (11, 12),  # Ngón giữa
    (0, 13), (13, 14), (14, 15), (15, 16),# Ngón áp út
    (0, 17), (17, 18), (18, 19), (19, 20) # Ngón út
]


def draw_hand_points(frame, hand_points, color):
    points = []
    for i in range(21):
        x = int(hand_points[i * 3] * frame_width)
        y = int(hand_points[i * 3 + 1] * frame_height)
        points.append((x, y))
        if hand_points[i * 3] != -1 and hand_points[i * 3 + 1] != -1:
            cv2.circle(frame, (x, y), 5, color, -1)

    # draw connection line
    for start, end in connections:
        if points[start] is not None and points[end] is not None:
            cv2.line(frame, points[start], points[end], color, 2)
            
    
# Looping
num_frames = min(len(hand1_array), len(hand2_array))
for i in range(num_frames):
    # Tạo nền đen
    frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
    
    # draw hand1 và hand2
    draw_hand_points(frame, hand1_array[i], (0, 0, 255))  # red point
    draw_hand_points(frame, hand2_array[i], (255, 0, 0))  # blue point
    
    # write hand into video
    out.write(frame)

# done
out.release()
print("Video đã được lưu thành công.")
