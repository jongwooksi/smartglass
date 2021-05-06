import numpy as np
import cv2

def skinmask(img):
    
    hsvim = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    lower = np.array([0, 48, 80], dtype = "uint8")
    upper = np.array([20, 255, 255], dtype = "uint8")
    skinRegionHSV = cv2.inRange(hsvim, lower, upper)
    blurred = cv2.blur(skinRegionHSV, (2,2))
    ret, thresh = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY)
    
    return thresh

def getcnthull(mask_img): 
    contours, hierarchy = cv2.findContours(mask_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   
    
    if len(contours) == 0:
        return "None"

    else:
        contours = max(contours, key=lambda x: cv2.contourArea(x))
        if cv2.contourArea(contours) < 2000:
            return "None"
        
        else:
            hull = cv2.convexHull(contours)
            return hull


def getminhull(hull):
    minimum = 9999999
    cord = []
    size = len(hull)
    

    for i in range(size):
        if hull[i][0][1] < minimum:
            minimum = hull[i][0][1]
           
            cord.clear()
            cord.append(hull[i][0])

    return cord

def handPointDetection(img):
    mask_img = skinmask(img)
    
    hull = getcnthull(mask_img) 

    if hull is not "None": 
        return(getminhull(hull))
                 
    else : return []

errorAreaX = 15
errorAreaY = 40

def checkHandPoint(position, rec, phone_img):
    if rec[0]-errorAreaX < position[0][0] and rec[2]+errorAreaX > position[0][0] :
        if rec[1]-errorAreaY < position[0][1] and rec[3]+errorAreaY > position[0][1] :
            return True

    else : return False

def drawHandPoint(rec, phone_img):
    cv2.rectangle(phone_img,(rec[0]-errorAreaX,rec[1]-errorAreaY),(rec[2]+errorAreaX,rec[3]+errorAreaY),(0,255,255))
    cv2.imshow("phone", phone_img)