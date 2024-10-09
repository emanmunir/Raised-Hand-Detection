import cv2
import mediapipe as mp
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

class HandRaiseDetector(VideoTransformerBase):
    def __init__(self):
        self.hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract Y coordinates of important hand landmarks
                wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y
                index_finger_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                middle_finger_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
                ring_finger_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
                pinky_finger_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

                index_finger_pip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
                middle_finger_pip_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
                ring_finger_pip_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
                pinky_finger_pip_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y
                thumb_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                thumb_ip_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y

                # Check if all fingers are pointing straight up by comparing the Y values of the tips to their lower joints
                if (index_finger_tip_y < index_finger_pip_y and
                    middle_finger_tip_y < middle_finger_pip_y and
                    ring_finger_tip_y < ring_finger_pip_y and
                    pinky_finger_tip_y < pinky_finger_pip_y and
                    thumb_tip_y < thumb_ip_y):

                    # If the condition is met, we say the hand is raised
                    print("I raised my hand!")  # Print to console for logging purposes
                    cv2.putText(img, 'I raised my hand!', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        return img

def main():
    st.title("Raise Hand Detector")
    st.write("Raise your hand in front of the camera to get a response!")
    webrtc_streamer(key="hand-raise", video_processor_factory=HandRaiseDetector)

if __name__ == "__main__":
    main()
