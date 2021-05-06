import pyttsx3

stage = 0 # init = 0
visible = [True, True, True, True, True, True]
buttonFlag = False

engine = pyttsx3.init()

def speakDistance(text):
    print(text)
    engine.say(text)
    #engine.runAndWait()

def speakStage(text): 
    print(text)
    setVisible(False)
    setButtonFlag(True)
    engine.say(text)
    #engine.runAndWait()

def getStage():
    return stage

def setStage(num):
    global stage
    stage = num

def getButtonFlag():
    return buttonFlag

def setButtonFlag(flag):
    global buttonFlag
    buttonFlag = flag

def setVisible(flag):
    global visible
    visible[getStage()-1] = flag

def getVisible():
    return visible[getStage()-1] 

def checkSize(data):
    if len(data) > 0: return True
    else : return False

def classificationPage(page):
    if checkSize(page):
        page = page.replace(" ","")
     
        if getStage() == 6 and getButtonFlag() == False :
            setStage(7)
            setButtonFlag(True)

        if getStage() == 4 and getVisible() == False:
            page = page[0:4]    
        else:
            page = page[0:2]
       
        if page =="승차" or page == "차권" or page == "권예" or page == "예매" or page == "슴자":
            printNotice(1)

        elif page =="열차" or page =="차조" or page =="조회" or page == "열자":
            printNotice(2)

        elif page =="로그": 
            printNotice(3)

        elif page == "비회":
            printNotice(4)

        elif page =="예약취소" or page == "승차권정" or page == "차권정보"or page == "권정보확" or page == "정보확인":
            printNotice(5)

        elif page =="결제":
            printNotice(6)
        

def printNotice(pageNum):
    setStage(pageNum)
    
    if not getVisible() == True:
        return

    if getStage() == 1 :
        print("승차권 예매 page")
        speakStage("출발, 목적지 및 날짜를 선택하고 우측 하단의 열차 조회하기를 누르세요.")
        

    elif getStage() == 2:
        print("열차 조회 page")
        speakStage("예매할 열차의 우측에 일반실 금액을 선택하고 예매를 누르세요.")


    elif getStage() == 3 :
        print("로그인 page")
        speakStage("하단의 비회원을 누르세요.")


    elif getStage() == 4 :
        print("비회원 page")
        speakStage("정보를 입력하고 확인 버튼을 누르세요.")


    elif getStage() == 5:
        print("승차권정보확인 page")
        speakStage("예매 정보를 확인하고 결제하기 버튼을 누르세요.")


    elif getStage() == 6 :
        print("결제 page")
        speakStage("결제정보를 확인하고 다음 버튼을 누른 후 결제/발권을 눌러주세요.")
