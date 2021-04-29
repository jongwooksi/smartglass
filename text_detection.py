import cv2
import pytesseract

ratio_x = 0.08
ratio_y = 1.1

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
    up_rect = rect
    up_rect = [0 if value < 0  else value for value in up_rect ] 

    width_up = up_rect[2] - up_rect[0]
    height_up = up_rect[3] - up_rect[1]
    
    area_up = width_up * height_up
    ratio_up = width_up / height_up

    return up_rect, width_up, height_up, area_up, ratio_up


def textPage(rect, phone_img):
    if not rect == None:
        text = ""

        for i in range(len(rect)-1, 0,-1):
            
            up_rect, width_up, height_up, area_up, ratio_up = checkBox(rect[i])

            if (ratio_up > 4.5) or (ratio_up < 2) or area_up < 500 or height_up < 10:
                continue

            cv2.rectangle(phone_img,(up_rect[0],up_rect[1]),(up_rect[2],up_rect[3]),(255,0,0))

            text = textButton(up_rect, phone_img)

            break

        cv2.imshow("phone", phone_img)
        return text
    
    else: return ""
        
def textButton(rect, phone_img):
    
    buttonimage = phone_img[rect[1]:rect[3], rect[0]:rect[2]]
  
    return pytesseract.image_to_string(buttonimage, lang='kor') 

def textButtonRecognition(position, rect, phone_img):
    if not rect == None:
        p_button = []
        flag = False
        
        for i in range(len(rect)-1, 0,-1):
            button, width_up, height_up, area_up, ratio_up = checkBox(rect[i])
            
            if (ratio_up < 4) or (ratio_up> 6) or area_up < 1000 or height_up < 20:
                continue

            cv2.rectangle(phone_img,(button[0],button[1]),(button[2],button[3]),(255,0,0))

            if not len(button) == 0:
                cv2.rectangle(phone_img,(button[0],button[1]),(button[2],button[3]),(255,0,255))
                buttonText = textButton(button, phone_img)
                
            if checkButtonText(buttonText):
                p_button = button
                print(buttonText)
                break

        cv2.imshow("button", phone_img)
        return p_button
    
    else: return []


def checkButtonText(button):
    button = button.replace(" ","")

    button = button[0:2]

    if button == "열차" or button == "조회"or button == "하기":
        return True

    else:
        return False


def checkHandPoint(position, rec):
    errorArea = 20


    if rec[0] < position[0][0]+errorArea and rec[2] > position[0][0]-errorArea :
        if rec[1] < position[0][1]+errorArea and rec[3] > position[0][1]-errorArea :
            return True

    else : return False


'''
def textButtonRecognition(position, rect, phone_img):
    if not len(position) == 0 :
        if not position[0][1] == 0 : 
            print("End of Hand {}".format(position)) 

            
            button = []
            rect.sort()

            for rec in rect:
                if rec[0] < position[0][0] and rec[2] > position[0][0] :
                    if rec[1] < position[0][1] and rec[3] > position[0][1] :
                        button = rec 

            button = [0 if value < 0  else value for value in button ] 

            print(button)            
            if not len(button) == 0:
                cv2.rectangle(phone_img,(button[0],button[1]),(button[2],button[3]),(255,0,255))
                buttonText = textButton(button, phone_img)
                print(buttonText)

            cv2.imshow("button", phone_img)    
            return phone_img
'''



     