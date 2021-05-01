import cv2
from hand_detection import *
from text_detection import *
from phone_detection import *
import numpy as np
import pytesseract
 
cap = cv2.VideoCapture(0)
W_View_size = 640
H_View_size = int(W_View_size / 1.333)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, W_View_size)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H_View_size)
cap.set(cv2.CAP_PROP_FPS,5)

distance_size = W_View_size * H_View_size / 2.5
stage = 0 # init = 0
visible = [True, True, True, True, True]
pos_button = []
buttonFlag = False

def checkSize(data):
    if len(data) > 0: return True
    else : return False


def drawRectangle(rect, phone_img):
    for i in rect:
        cv2.rectangle(phone_img,i[:2],i[2:],(0,0,255))


def classificationPage(page):
    if checkSize(page):
        global stage
        page = page.replace(" ","")

        if stage == 4 and visible[stage-1] == False:
            page = page[0:4]    
        else:
            page = page[0:2]
          
        if page =="승차" or page == "차권" or page == "권예" or page == "예매" or page == "슴자":
            stage = 1
            printNotice()

        elif page =="열차" or page =="차조" or page =="조회" or page == "열자":
            stage = 2
            printNotice()

        elif page =="로그": 
            stage = 3
            printNotice()

        elif page == "비회":
            stage = 4
            printNotice()

        elif page =="예약취소" or page == "승차권정" or page == "차권정보"or page == "권정보확" or page == "정보확인":
            stage = 5
            printNotice()
  
    
def printNotice():
    global stage
    global buttonFlag

    if stage == 1 and visible[stage-1] == True:
        print("승차권 예매 page")
        print("출발, 목적지 및 날짜를 선택하고 우측 하단의 열차 조회하기를 누르세요.")
        visible[stage-1] = False
        buttonFlag = True

    elif stage == 2 and visible[stage-1] == True:
        print("열차 조회 page")
        print("예매할 열차의 우측에 일반실 금액을 선택하고 예매를 누르세요.")
        visible[stage-1] = False
        buttonFlag = True

    elif stage == 3 and visible[stage-1] == True:
        print("로그인 page")
        print("하단의 비회원을 누르세요.")
        visible[stage-1] = False
        buttonFlag = True

    elif stage == 4 and visible[stage-1] == True:
        print("비회원 page")
        print("정보를 입력하고 완료 버튼을 누르세요.")
        visible[stage-1] = False
        buttonFlag = True

    elif stage == 5 and visible[stage-1] == True:
        print("승차권정보확인 page")
        print("예매 정보를 확인하고 결제하기 버튼을 누르세요.")
        visible[stage-1] = False
        buttonFlag = True



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

        if stage == 0 or buttonFlag == False:
            page = textPage(rect, phone_img,stage)
            classificationPage(page)

        else:
            button = textButtonRecognition(rect, phone_img, stage)

            if checkSize(button):
                pos_button = button

            if checkSize(pos_button):
                drawHandPoint(pos_button, phone_img)

            if checkSize(position) and checkSize(pos_button):
                if checkHandPoint(position, pos_button, phone_img):
                    buttonFlag = False
                    pos_button = []
                    print("Pushed button")

            if checkSize(position):
                cv2.circle(phone_img, (position[0][0], position[0][1]), 4, [0, 0, 255], -1)
                cv2.imshow("phone", phone_img)
 
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
    

