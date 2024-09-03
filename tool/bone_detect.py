import cv2
import mediapipe as mp
import time
import numpy as np

class bone_detect:
    def __init__(self) -> None:
        # Khởi tạo các mô-đun Mediapipe
        self.mp_pose = mp.solutions.pose
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles


        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.8)
        self.pose = self.mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.8)
        
        self.hand_list = []
        self.pose_list = []

        self.hand1 = []
        self.hand2 = []



    
    def process_hand_landmarks(self, hand_landmarks):
        hand_landmarks_list = []
        if len(hand_landmarks.landmark) == 21:
            for landmark in hand_landmarks.landmark:
                hand_landmarks_list.append(landmark.x)
                hand_landmarks_list.append(landmark.y)
                hand_landmarks_list.append(landmark.z)
        else:
            hand_landmarks_list = [-1] * 63  # 21 points * 3 (x,y,z)
        return hand_landmarks_list

    
    def detect(self,image,returnValue = False):
        image.flags.writeable = False
        hand_results = self.hands.process(image)
        pose_results = self.pose.process(image)
        image.flags.writeable = True
        if pose_results.pose_landmarks:
            self.pose_list.append(pose_results.pose_landmarks)
            self.mp_drawing.draw_landmarks(
                image, pose_results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())
            
        if hand_results.multi_hand_landmarks:
            # process hand1 
            if len(hand_results.multi_hand_landmarks) > 0 and hand_results.multi_hand_landmarks[0]:
                self.hand1.append(self.process_hand_landmarks(hand_results.multi_hand_landmarks[0]))
                self.mp_drawing.draw_landmarks(image, hand_results.multi_hand_landmarks[0], self.mp_hands.HAND_CONNECTIONS)
            else:
                self.hand1.append([-1] * 63)

            # process hand2
            if len(hand_results.multi_hand_landmarks) > 1 and hand_results.multi_hand_landmarks[1]:
                self.hand2.append(self.process_hand_landmarks(hand_results.multi_hand_landmarks[1]))
                self.mp_drawing.draw_landmarks(image, hand_results.multi_hand_landmarks[1], self.mp_hands.HAND_CONNECTIONS)
            else:
                self.hand2.append([-1] * 63)
              
        if returnValue:
            return (image, [self.hand1, self.hand2])  
      
        return image
                
        