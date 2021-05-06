import cv2
from hand_detection import *
from text_detection import *
from phone_detection import *
from output import *
import numpy as np
import pytesseract
 
cap = cv2.VideoCapture(0)
W_View_size = 640
H_View_size = int(W_View_size / 1.333)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, W_View_size)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H_View_size)
cap.set(cv2.CAP_PROP_FPS,5)

distance_size = W_View_size * H_View_size / 2.5

pos_button = []


while cap.isOpened():

    _, img = cap.read()
    
    bbox, label, conf = detectPhone(img)

    if checkPhoneDetection(label):
    
        index = setPhoneLabel(label)
    
        phone_box = modifyCord(bbox[index])

        width, height, area = getInformBox(phone_box)

        if distanceRecognition(area, distance_size):
            continue
        
        phone_img = getPhoneImage(img,phone_box)

        position = handPointDetection(phone_img) 
        
        rect = textDetect(phone_img)

        if getStage() == 0 or getButtonFlag() == False:
            page = textPage(rect, phone_img,getStage())
            classificationPage(page)
       
        else:
            button = textButtonRecognition(rect, phone_img, getStage())

            if checkSize(button):
                pos_button = button

            if checkSize(pos_button):
                drawHandPoint(pos_button, phone_img)

            if checkSize(position) and checkSize(pos_button):
                if checkHandPoint(position, pos_button, phone_img):
                    setButtonFlag(False)
                    pos_button = []
                    print("Pushed button")

            if checkSize(position):
                cv2.circle(phone_img, (position[0][0], position[0][1]), 4, [0, 0, 255], -1)
                cv2.imshow("phone", phone_img)
 
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
    

