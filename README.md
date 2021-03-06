# smartglass (2021.04.03 ~ 2021.05.08)
스마트 글래스를 이용하여 예매 어플리케이션(기차, 고속버스 등)을 사용하기 힘든 디지털 소외계층(노약자)을 돕는 것에 주 목적이 있다.
현재 코레일톡을 기반으로 개발 진행중이며, 추후 TTS 기능 및 초소형컴퓨터와의 결합을 통해 이동성 있고 음성으로 설명해주는 제품을 개발할 예정이다.


Commit Message와 실제 일자는 다를 수 있습니다.

[2021.05.08]
- 학술대회 논문화
- 개발코드 및 추후 진행사항 인수인계  

[2021.05.06]
- TTS 기능을 위한 Pyttsx3 설치
- main.py 내부에 있던 출력함수와 sound를 output.py로 통합 (set, get 함수 생성)
- 결제 페이지 Stage 6~7 추가 및 버튼 인식 추가
- 버튼 인식 범위 확장 
- requirement.txt 추가
- all Stage 시나리오 테스트 완료


[2021.05.01]
- 각 Stage Page 및 버튼 타이틀의 비율 실험, 고정
- Phone_detection.py에 휴대폰 관련 기능 모듈화
- 대부분의 넘기는 버튼은 아래쪽에 위치하므로 역순으로 Search하는 것으로 변경
- OCR 실험을 통해 오인식한 결과를 정답으로 라벨링하여 성능 향상
- 불필요한 이미지 창 및 Drawing 제거 및 통합
- Pushed Button 기능 오류 수정 및 인식 영역 확장
- 손 끝 미검출 시 이전의 좌표를 사용하던 오류 수정
- 페이지 인식 후 계속 출력되던 오류 수정

[2021.04.24~2021.04.29]
- 손가락 위치에 따른 버튼의 글씨를 인식하는 방법은 페이지가 넘어가기 전에 인식 못할 경우, 다음 단계로 진행 불가능한 점을 발견
- 페이지 내의 눌러야 하는 버튼의 위치를 먼저 인식
- 손가락이 눌러야 하는 버튼 범위내에 들어갔을 경우 버튼을 누른 것으로 판정 및 페이지를 인식하는 기능으로 넘어가는 식으로 수정 및 구현

[2021.04.17~2021.04.22]
- 손가락 위치에 따른 버튼에 있는 글씨 인식 기능 추가
- 손가락이 버튼 위치에 가면 글씨 영역으로 인식하지 않아 해당 위치가 찍힌 이후 손을 땠을 때 인식 하도록 설계       
    
[2021.04.10~2021.04.15]
- 코레일 톡을 기반으로 시나리오 작성
- 휴대폰 영역만을 Detection 하는 것으로 수정
- 실험 결과 cell phone과 remote로 주로 인식하는 것을 확인
- 휴대폰 영역만을 Crop한 이미지를 대상으로 텍스트 영역 검출
- 휴대폰과의 거리를 인식하는 기능 추가
- 최상단 글씨 인식을 위해 여러 조건 적용
- OCR 기능을 추가하여 페이지 최상단 글씨 인식

[2021.04.03~2021.04.08]
- HSV영상 기반의 손 영역 마스킹
- 손 영역 및 손 끝 검출







