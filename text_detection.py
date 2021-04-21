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


def textPage(rect, phone_img):
    if len(rect) > 0:
        text = ""

        for i in range(len(rect)-1, 0,-1):
            up_rect = rect[i]
            up_rect = [0 if value < 0  else value for value in up_rect ] 
        
            width_up = up_rect[2] - up_rect[0]
            height_up = up_rect[3] - up_rect[1]
            
            area_up = width_up * height_up
            ratio_up = width_up / height_up
            
            if (ratio_up > 4.5) or (ratio_up < 2) or area_up < 500 or height_up < 10:
                continue

            cv2.rectangle(phone_img,(up_rect[0],up_rect[1]),(up_rect[2],up_rect[3]),(255,0,0))

            menuimage = phone_img[up_rect[1]:up_rect[3], up_rect[0]:up_rect[2]]

            text = pytesseract.image_to_string(menuimage, lang='kor') 

            cv2.imshow("menu", menuimage)
            break

        cv2.imshow("phone", phone_img)
        return text

        
