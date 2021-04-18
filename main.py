import cv2
import cvlib as cv
import copy
from cvlib.object_detection import draw_bbox
from hand_detection import *
from text_detection import *
import numpy as np
import pytesseract

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

        width = phone_box[2]-phone_box[0]
        height = phone_box[3]-phone_box[1]
        area = width * height

        if area < W_View_size * H_View_size / 2.5:
            print("가까이 더 가까이 ~")
            cv2.imshow("img", img)
            continue

        
        #print(phone_box)

        img, img2 = hand(img, img2)

        
        phone_img = img2[phone_box[1]:phone_box[3], phone_box[0]:phone_box[2]]

        rect = text_detect(phone_img)
        
        for i in rect:
            cv2.rectangle(phone_img,i[:2],i[2:],(0,0,255))

        if len(rect) > 0:
            up_rect = rect[len(rect)-1]
            up_rect = [0 if value < 0  else value for value in up_rect ] 
           
            cv2.rectangle(phone_img,(up_rect[0],up_rect[1]),(up_rect[2],up_rect[3]),(255,0,0))

            menuimage = phone_img[up_rect[1]:up_rect[3], up_rect[0]:up_rect[2]]
            cv2.imshow("menuimage",menuimage )


            text = pytesseract.image_to_string(menuimage, lang='kor') 
            
            if text[0] == "승":
                print("main page")
                print(up_rect)
                print(text)

            elif text[0] == "열":
                print("second page")
                print(text)

            elif text[0] == "로":
                print("third page")
                print(text)


        cv2.imshow("menu", phone_img)

    
    cv2.imshow("img", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
    

