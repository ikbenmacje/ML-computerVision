'''
Requirements:

pip install mediapipe

'''

import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

#Variable for Drawing
fontFace = cv2.FONT_HERSHEY_PLAIN
fontScale = 2;
thickness = 2;
fontColor = (255,0,255)

# For static images:
#file = "gezicht.jpg"
file = "LeafM02.png" 
with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
    image = cv2.imread(file)
    # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
    results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    annotated_image = image.copy()

    # Draw face detections of each face.
    if results.detections:
        for detection in results.detections:
            print('Nose tip:')
            print(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
            mp_drawing.draw_detection(annotated_image, detection)

            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = image.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.putText(annotated_image, f'{"confidence: "+str(int(detection.score[0]*100))}%',(bbox[0],bbox[1]-20),fontFace, fontScale, fontColor,thickness)
    else:
        print("Not a face: "+file)
        ih, iw, ic = image.shape
        txt = "Not a face"
        retval, baseLine = cv2.getTextSize(txt, fontFace,fontScale, thickness);
        org = (int(iw/2-retval[0]/2),int(ih/2))
        cv2.putText(annotated_image, txt,org,fontFace, fontScale, fontColor,thickness)
    
    cv2.imwrite('leaf_annotated' + '.png', annotated_image)

    