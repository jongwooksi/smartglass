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

stage = -1
visible = [True, True, True, True, True]

def classificationPage(page):
    if len(page) > 0:
        global stage
        page = page.replace(" ","")

        if stage == 4 and visible[stage-1] == False:
            page = page[0:4]    
        else:
            page = page[0:3]
          
        print(page)
        if page =="승차권" or page == "차권예" or page == "권예매":
            stage = 1
            print("승차권 예매 page")
            printNotice()

        elif page =="열차조":
            print("열차 조회 page")
            stage = 2
            printNotice()

        elif page =="로그인":
            print("로그인 page")
            stage = 3
            printNotice()

        elif page == "비회원":
            print("비회원 page")
            stage = 4
            printNotice()

        elif page =="예약취소" or page == "승차권정" or page == "차권정보"or page == "권정보확" or page == "정보확인":
            print("승차권정보확인 page")
            stage = 5
            printNotice()
  
    

def printNotice():
    global stage
    if stage == 1 and visible[stage-1] == True:
        print("출발, 목적지 및 날짜를 선택하고 우측 하단의 열차 조회하기를 누르세요.")
        visible[stage-1] = False

    elif stage == 2 and visible[stage-1] == True:
        print("예매할 열차의 우측에 일반실 금액을 선택하하고 예매를 누르세요.")
        visible[stage-1] = False

    elif stage == 3 and visible[stage-1] == True:
        print("하단의 비회원을 누르세요.")
        visible[stage-1] = False

    elif stage == 4 and visible[stage-1] == True:
        print("정보를 입력하고 완료 버튼을 누르세요.")
        visible[stage-1] = False

    elif stage == 5 and visible[stage-1] == True:
        print("예매 정보를 확인하고 결제하기 버튼을 누르세요.")
        visible[stage-1] = False


def drawRectangle(rect, phone_img):
    for i in rect:
        cv2.rectangle(phone_img,i[:2],i[2:],(0,0,255))

    return phone_img

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

        if area < (W_View_size * H_View_size / 2.5):
            print("가까이 더 가까이 ~")
            cv2.imshow("img", img)
            continue


        img, img2 = hand(img, img2)

        phone_img = img2[phone_box[1]:phone_box[3], phone_box[0]:phone_box[2]]

        rect = textDetect(phone_img)
        
        phone_img = drawRectangle(rect, phone_img)

        page = textPage(rect, phone_img)

        classificationPage(page)
        
    
    cv2.imshow("img", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
    

