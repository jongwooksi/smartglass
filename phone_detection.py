import cvlib as cv
from cvlib.object_detection import draw_bbox

def detectPhone(img):
    return cv.detect_common_objects(img)

def checkPhoneDetection(label):
    if label.count('cell phone') > 0 or label.count('remote') > 0 :
        return True

    else: return False

def setPhoneLabel(label):
    if label.count('cell phone') > 0:
        index = label.index('cell phone')
    elif label.count('remote') > 0:
        index = label.index('remote')

    return index


def distanceRecognition(area, distance_size):
    if area < distance_size:
        print("Put your cell phone a little closer")
        return True

    else: return False    


def getInformBox(box):
    width = box[2]-box[0]
    height = box[3]-box[1]
    area = width * height

    return width, height, area

def getPhoneImage(img, box):
    return img[box[1]:box[3], box[0]:box[2]]
