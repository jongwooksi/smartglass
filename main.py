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

def classificationPage(page):
    if len(page) > 0:
        page = page.replace(" ","")
        page = page[0:3]

        if page =="승차권" or page == "차권예" or page == "권예매":
            print("승차권 예매 page")

        elif page =="열차조":
            print("열차 조회 page")
    
        elif page =="로그인":
            print("로그인 page")

        elif page == "비회원":
            print("비회원 page")


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

        rect = textDetect(phone_img)
        
        for i in rect:
            cv2.rectangle(phone_img,i[:2],i[2:],(0,0,255))

        page = textPage(rect, phone_img)

        classificationPage(page)
        
    
    cv2.imshow("img", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
    

