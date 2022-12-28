![image](https://user-images.githubusercontent.com/70826982/209808326-0bd9add2-2a5b-41f7-8c1f-e12f7301d718.png)
---

**Raspberry Pi와 센서 및 엑츄에이터 등을 활용해 지능형 감시카메라를 제작하는 프로젝트입니다.**  
**총 두 가지 버전이 제공되며, 자세한 설명은 첨부한 발표자료를 통해 확인할 수 있습니다.**

<p align="center"><img width="461" alt="스크린샷 2022-12-29 오전 12 33 33" src="https://user-images.githubusercontent.com/70826982/209835867-e51b6dde-cf3c-4ef5-ac97-c95598f9acc2.png"></p>

> Note: Raspberry Pi OS, Python 2.7 환경에서 개발 및 테스트가 진행되었습니다.  
V2의 경우, 서보모터 성능 향상을 위해 pigpio 데몬이 별도로 사용되었습니다. LINE 메세지 전송용 Token은 [LINE Notify](https://notify-bot.line.me/en/)에서  
발급받아 사용하세요. 코드의 Token은 유효하지 않습니다. 사용한 모듈은 별도로 명세하지 않았으며,  
프로젝트 특성 상 소스코드가 다소 난해한 점 양해바랍니다.  
<br/>

# v1: 범위 내 물체를 감지하고 경고하는 감시 카메라  

<p align="center"><img width="800" alt="image" src="https://user-images.githubusercontent.com/70826982/209812402-26180b36-b917-4c96-bb02-f87593949644.png"></p>

## 개요
웹 페이지를 통해 실시간으로 현장 상황을 감시할 수 있고 일정 범위 내에 물체가 감지되면 경고음 송출과 함께 경고등이 점등되며 <br/>
LINE 메세지를 통해 관리자에게 알립니다. 카메라가 화전하므로 사각지대 없이 전 구역을 실시간으로 감시할 수 있습니다.
<p align="center"><img width="700" alt="image" src="https://user-images.githubusercontent.com/70826982/209812194-a017bdea-7a85-46bf-bf26-5ac790e0bd59.png"></p>

**사용 방법**  
필요 모듈이 설치되었고, 회로 구성이 일치해야 동작합니다.  

```bash
git clone https://github.com/Seol-JY/intelligent-CCTV.git
python v1/Project.py
```

**시연 영상**  
[유튜브 영상](https://youtu.be/JtzTJLKwXZg)

## 회로 구성
<img width="1786" alt="image" src="https://user-images.githubusercontent.com/70826982/209813468-1aad2867-49e1-4160-b171-93c8e1f13181.png">

<br/>
<br/>
<hr/>
<br/>

# v2: Tensorflow.js 기반 Human Detection 감시 카메라

<p align="center"><img width="1100" alt="image" src="https://user-images.githubusercontent.com/70826982/209839355-45dcbc6e-cde3-47be-bc4a-9569e6e2ab4a.png">
</p>
<img width="1642" alt="image" src="https://user-images.githubusercontent.com/70826982/209839903-d0317b71-3785-4049-a1c4-bcdc27814920.png">

## 개요
관제인력에 구애받지 않고 감시카메라 스스로 인원의 접근을 감지하고 관리자에 통보합니다. 웹페이지를 통해 실시간으로 현장 상황을 감시할 수 있고<br/>
감시카메라 제어를 위한 다양한 설정이 가능합니다. 메세지 수신 토글 버튼이 켜져 있다면, 인원 감지 시 사진과 함께 LINE 메세지를 전송합니다.<br/>
Raspberry Pi의 성능상의 한계를 극복하기 위해 client-side에서 Tenserflow.js를 사용해 Object-Detection을 수행합니다.
<p align="center"><img width="700" alt="스크린샷 2022-12-29 오전 1 26 28" src="https://user-images.githubusercontent.com/70826982/209842711-c0c37c45-9c40-4945-a4a6-e553961a9084.png"></p>


**사용 방법**  
필요 모듈이 설치되었고, 회로 구성이 일치해야 동작합니다.  

```bash
git clone https://github.com/Seol-JY/intelligent-CCTV.git
python v2/main.py
```

**시연 영상**  
[유튜브 영상](https://www.youtube.com/watch?v=v41BfkFqUag)

## 회로 구성
<img width="1104" alt="스크린샷 2022-12-29 오전 1 39 04" src="https://user-images.githubusercontent.com/70826982/209844223-49d2a54e-4596-470b-8e17-14a0c79ab44a.png">

