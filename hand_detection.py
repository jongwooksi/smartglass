import numpy as np
import cv2

minhull = []

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

def getdefects(contours):
    hull = cv2.convexHull(contours, returnPoints=False)
    defects = cv2.convexityDefects(contours, hull)
    return defects

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

def hand(img,img2):
    mask_img = skinmask(img2)
    
    hull = getcnthull(mask_img) 

    if hull is not "None": 
        global minhull
        minhull = getminhull(hull)
        
        #cv2.drawContours(img, [contours], -1, (255,255,0), 2)
        cv2.drawContours(img, [hull], -1, (0, 255, 255), 2)
        
        #defects = getdefects(contours)
        img = cv2.circle(img, (minhull[0][0], minhull[0][1]), 4, [0, 0, 255], -1)
            
    return img, img2, minhull