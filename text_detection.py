import cv2

ratio_x = 0.08
ratio_y = 1.1

def text_detect(img,ele_size=(23,15)): 
   
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.Sobel(img,cv2.CV_8U,1,0)
    img = cv2.threshold(img,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY)

    element = cv2.getStructuringElement(cv2.MORPH_RECT,ele_size)
    img = cv2.morphologyEx(img[1],cv2.MORPH_CLOSE,element)

    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    Rectangle = [cv2.boundingRect(i) for i in contours if i.shape[0]>80 and i.shape[0] < 500 and (i.shape[1] / i.shape[0]) <2]
    rect = [(int(i[0]-i[2]*ratio_x),int(i[1]-i[3]*ratio_x),int(i[0]+i[2]*ratio_y),int(i[1]+i[3]*ratio_y)) for i in Rectangle]
    
    return rect


