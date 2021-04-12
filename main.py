import cv2
import cvlib as cv
import copy
from cvlib.object_detection import draw_bbox
from hand_detection import *
from text_detection import *

cap = cv2.VideoCapture(1)

W_View_size = 640
H_View_size = int(W_View_size / 1.333)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, W_View_size)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H_View_size)
cap.set(cv2.CAP_PROP_FPS,10)


while cap.isOpened():
  
    _, img = cap.read()
    img2 = copy.deepcopy(img)
    bbox, label, conf = cv.detect_common_objects(img)

    
    if label.count('cell phone') > 0 or label.count('remote') > 0:
        index = -1

        if label.count('cell phone') > 0:
            index = label.index('cell phone')
        elif label.count('remote') > 0:
            index = label.index('remote')

        phone_box = bbox[index]
        phone_box = [0 if value < 0  else value for value in phone_box ] 

        img = draw_bbox(img, [ bbox[index]], [label[index]], [conf[index]]) 

        img, img2 = hand(img, img2)

        phone_img = img2[phone_box[1]:phone_box[3], phone_box[0]:phone_box[2]]

        rect = text_detect(phone_img)

        for i in rect:
            cv2.rectangle(phone_img,i[:2],i[2:],(0,0,255))

        cv2.imshow("phone", phone_img)

    
    cv2.imshow("img", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
    

