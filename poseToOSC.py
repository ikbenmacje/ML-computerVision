'''
    Requirements:
    pip install mediapipe
    pip install pythonosc
'''

import cv2
import mediapipe as mp
from pythonosc import udp_client
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Create OSC client
OSCport = 1234
OSCaddress = '127.0.0.1'
client = udp_client.SimpleUDPClient(OSCaddress, OSCport) # local debug 

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # check if we have landmarks
    # This if statement is not so relaible
    if len(results.pose_landmarks.landmark) != 0:

        # Each pose has 32 landmarks with normalized x/y/z/visiblilty
        poseCoords = []
        for id, lm in enumerate(results.pose_landmarks.landmark):
            print(id,lm)
            poseCoords.append(id)
            poseCoords.append(lm.x)
            poseCoords.append(lm.y)
            poseCoords.append(lm.z)
            poseCoords.append(lm.visibility)

        # send over OSC
        client.send_message("/pose", poseCoords)
    

    print("hgello")

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()