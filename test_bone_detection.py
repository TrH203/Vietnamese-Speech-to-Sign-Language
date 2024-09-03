import cv2
import mediapipe as mp
import time
import numpy as np
# Khởi tạo các mô-đun Mediapipe
mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Khởi tạo nhận diện khuôn mặt và bàn tay
# face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)


hand_list = []
pose_list = []

# Mở webcam
cap = cv2.VideoCapture(0)
# Biến để tính toán FPS
prev_time = 0
hand1 = []
hand2 = []

def process_hand_landmarks(hand_landmarks):
    hand_landmarks_list = []
    if len(hand_landmarks.landmark) == 21:
        for landmark in hand_landmarks.landmark:
            hand_landmarks_list.append(landmark.x)
            hand_landmarks_list.append(landmark.y)
            hand_landmarks_list.append(landmark.z)
    else:
        hand_landmarks_list = [-1] * 63  # 21 điểm * 3 tọa độ mỗi điểm
    return hand_landmarks_list

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Chuyển đổi hình ảnh từ BGR sang RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Phát hiện khuôn mặt và bàn tay
    # face_results = face_mesh.process(image)
    hand_results = hands.process(image)
    pose_results = pose.process(image)

    # Chuyển đổi lại hình ảnh từ RGB sang BGR
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Vẽ các landmark và mesh của khuôn mặt
    # if face_results.multi_face_landmarks:
    #     for face_landmarks in face_results.multi_face_landmarks:
    #         mp_drawing.draw_landmarks(
    #             image,
    #             face_landmarks,
    #             mp_face_mesh.FACEMESH_TESSELATION,
    #             landmark_drawing_spec=None,
    #             connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
    #         mp_drawing.draw_landmarks(
    #             image,
    #             face_landmarks,
    #             mp_face_mesh.FACEMESH_CONTOURS,
    #             landmark_drawing_spec=None,
    #             connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())

    # Vẽ các landmark và kết nối của pose
    if pose_results.pose_landmarks:
        pose_list.append(pose_results.pose_landmarks)
        mp_drawing.draw_landmarks(
            image, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())


    if hand_results.multi_hand_landmarks:
        # Xử lý bàn tay đầu tiên
        if len(hand_results.multi_hand_landmarks) > 0 and hand_results.multi_hand_landmarks[0]:
            hand1.append(process_hand_landmarks(hand_results.multi_hand_landmarks[0]))
            mp_drawing.draw_landmarks(image, hand_results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
        else:
            hand1.append([-1] * 63)

        # Xử lý bàn tay thứ hai
        if len(hand_results.multi_hand_landmarks) > 1 and hand_results.multi_hand_landmarks[1]:
            hand2.append(process_hand_landmarks(hand_results.multi_hand_landmarks[1]))
            mp_drawing.draw_landmarks(image, hand_results.multi_hand_landmarks[1], mp_hands.HAND_CONNECTIONS)
        else:
            hand2.append([-1] * 63)



    # Tính toán FPS
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # Hiển thị FPS lên hình ảnh
    cv2.putText(image, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Hiển thị hình ảnh
    cv2.imshow('Mediapipe Face Mesh and Hands', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

# print(hand1)
# print("=============================")
# print(hand2)


hand1 = np.array(hand1)
hand2 = np.array(hand2)


print(hand1.shape)
print("=============================")
print(hand2.shape)

# Nối 2 bàn tay lại với nhau:
matrix3d = np.array([hand1,hand2])
print(matrix3d.shape)

from deployNoSQL import insert_intoDatabase

# insert_intoDatabase("Xin chào mọi người", matrix3d)

np.savetxt("/Users/trHien/Python/MyProjects/HuggingFace Workspace/Text_to_Sign/key_point_data/hand1.csv",hand1,delimiter=',')
np.savetxt("/Users/trHien/Python/MyProjects/HuggingFace Workspace/Text_to_Sign/key_point_data/hand2.csv",hand2,delimiter=',')


hands.close()
pose.close()
cap.release()
cv2.destroyAllWindows()

# print(all_frame_hand)
# all_frame_hand = np.array(all_frame_hand)
# print(all_frame_hand.shape)


# file_path1 = "hand_landmarks.txt"

# # Mở file để ghi dữ liệu tay
# with open(file_path1, "a") as file:
#     for hand in all_hand_landmark_list:
#         for i in hand:
#             file.write(str(i) + ", ")
#         file.write("\n")
    
# file_path2 = "pose_landmarks.txt"

# # Mở file để ghi
# with open(file_path2, "w") as file:
#     for i in pose_list:
#         file.write(str(i) + "\n")


# print("Hand: ",len(hand_list))
# print("Pose: ",len(pose_list))
