import cv2
import pytesseract
from output import *

ratio_x = 0.08
ratio_y = 1.1

def modifyCord(cord):
    return [0 if value < 0  else value for value in cord ]


def textDetect(img,ele_size=(23,15)): 
   
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.Sobel(img,cv2.CV_8U,1,0)
    img = cv2.threshold(img,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY)

    element = cv2.getStructuringElement(cv2.MORPH_RECT,ele_size)
    img = cv2.morphologyEx(img[1],cv2.MORPH_CLOSE,element)

    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    Rectangle = [cv2.boundingRect(i) for i in contours if i.shape[0]>80 and i.shape[0] < 500 and (i.shape[1] / i.shape[0]) <2]
    rect = [(int(i[0]-i[2]*ratio_x),int(i[1]-i[3]*ratio_x),int(i[0]+i[2]*ratio_y),int(i[1]+i[3]*ratio_y)) for i in Rectangle]
    
    return rect


def checkBox(rect):
    up_rect = modifyCord(rect)

    width_up = up_rect[2] - up_rect[0]
    height_up = up_rect[3] - up_rect[1]
    
    area_up = width_up * height_up
    ratio_up = width_up / height_up

    return up_rect, width_up, height_up, area_up, ratio_up


def textPage(rect, phone_img,stage):
    if not rect == None:
        text = ""

        for i in range(len(rect)-1, 0,-1):
            
            up_rect, width_up, height_up, area_up, ratio_up = checkBox(rect[i])

            if pageButtonArea(width_up, height_up, area_up, ratio_up, stage) :
                continue

            cv2.rectangle(phone_img,(up_rect[0],up_rect[1]),(up_rect[2],up_rect[3]),(255,0,0))

            text = textButton(up_rect, phone_img)
            break

        cv2.imshow("phone", phone_img)
        return text
    
    else: return ""
        

def textButton(rect, phone_img):
    buttonimage = phone_img[rect[1]:rect[3], rect[0]:rect[2]]
    text = pytesseract.image_to_string(buttonimage, lang='kor')

    return text.replace(" ","")


def textButtonRecognition(rect, phone_img, stage):
    if not rect == None:
        p_button = []
        
        for i in range(len(rect)):
            button, width_up, height_up, area_up, ratio_up = checkBox(rect[i])
            
            if buttonArea(width_up, height_up, area_up, ratio_up, stage):
                continue

            if not len(button) == 0:
                cv2.rectangle(phone_img,(button[0],button[1]),(button[2],button[3]),(255,0,255))
                buttonText = textButton(button, phone_img)

            if checkButtonText(buttonText,stage):
                p_button = button
                break

        cv2.imshow("phone", phone_img)
        return p_button
    
    else: return []


def checkButtonText(button,stage):
    button = button[0:2]

    if stage == 1:     
        if button == "열차" or button == "조회" or button == "별차" or button == "열자": return True
    elif stage == 2:
        if button == "예매": return True
    elif stage == 3:
        if button == "비회" or button == "비희" or button == "회원" : return True
    elif stage == 4: 
        if button == "확인": return True
    elif stage == 5: 
        if button == "결제": return True
    elif stage == 6: 
        if button == "다음": return True
    elif stage == 7: 
        if button == "결제" or button == "발권" : 
            Speak("결제 완료")
            return True

    else : return False


def buttonArea(width_up, height_up, area_up, ratio, stage):
    if stage == 1: 
        if ratio < 4.5 or ratio > 5.5: return True   
    elif stage == 2: 
        if ratio < 1.2 or ratio > 2.2 : return True
    elif stage == 3: 
        if ratio < 2 or ratio > 4: return True  
    elif stage == 4: 
        if ratio < 1.5 or ratio > 3: return True 
    elif stage == 5: 
        if ratio < 3 or ratio > 4: return True
    elif stage == 6: 
        if ratio < 1 or ratio > 2: return True 
    elif stage == 7: 
        if ratio < 3 or ratio > 4: return True 
           
    else : False


def pageButtonArea(width_up, height_up, area_up, ratio, stage):
    if stage == 0:
        if ratio < 3.2 or ratio > 4 or area_up < 500 or height_up < 10 : return True
    elif stage == 1:
        if ratio < 2.3 or ratio > 3.2 or area_up < 500 or height_up < 10 : return True
    elif stage == 2:
        if ratio < 1 or ratio > 3 or area_up < 500 or height_up < 10 : return True
    elif stage == 3: 
        if ratio < 1 or ratio > 3 or area_up < 500 or height_up < 10 : return True
    elif stage == 4: 
        if ratio < 5 or ratio > 7 or area_up < 500 or height_up < 10 : return True
    elif stage == 5: 
        if ratio < 1 or ratio > 2 or area_up < 500 or height_up < 10 : return True

    else : False