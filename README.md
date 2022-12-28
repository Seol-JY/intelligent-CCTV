![image](https://user-images.githubusercontent.com/70826982/209808326-0bd9add2-2a5b-41f7-8c1f-e12f7301d718.png)
---

<p align="center"><img width="410" alt="스크린샷 2022-12-29 오전 12 04 37" src="https://user-images.githubusercontent.com/70826982/209831814-f413b124-ea01-4c0c-bf79-9b418ea60010.png"></p>

**Raspberry Pi와 센서 및 엑츄에이터 등을 활용해 지능형 감시카메라를 제작하는 프로젝트입니다.**  
**총 두 가지 버전이 제공되며, 자세한 설명은 첨부한 발표자료를 통해 확인할 수 있습니다.**
> Note: Raspberry Pi OS, Python 2.7 환경에서 개발 및 테스트가 진행되었습니다.  
V2의 경우, 서보모터 성능 향상을 위해 pigpio 데몬이 별도로 사용되었습니다.  
사용한 모듈은 별도로 명세하지 않았으며, 프로젝트 특성 상 소스코드가 다소 난해한 점 양해바랍니다.  
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



## 회로 구성
<img width="1786" alt="image" src="https://user-images.githubusercontent.com/70826982/209813468-1aad2867-49e1-4160-b171-93c8e1f13181.png">

## 시연 영상
[유튜브 영상](https://www.youtube.com/watch?v=UusFe4qRObY)  
