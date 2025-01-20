# 🖥️ 학부 공지사항 자동 알림  

이 프로젝트는 전남대학교 공과대학 학부 페이지의 공지사항을 30분마다 크롤링하여 새롭게 추가된 공지사항을 수집하고, 이를 하루에 한 번 사용자가 지정한 시간에 카카오톡 "나에게 보내기" 기능을 통해 전달하는 파이썬 프로그램입니다.

---

## 🧑‍🤝‍🧑 팀원

- 이가영 : 화학교육과, 소프트웨어 공학과
- 김승현 : 소프트웨어 공학과
- 김지훈 : 전자컴퓨터공학부

## 📌 주요 기능
1. **공지사항 크롤링**  
   - 전남대학교 공과대학 학부 페이지의 공지사항을 30분마다 확인합니다.  
   - 새롭게 등록된 공지사항만 저장합니다.  

2. **카카오톡 알림 전송**  
   - 수집된 공지사항을 하루에 한 번, 사용자가 설정한 시간에 카카오톡 "나에게 보내기"로 전달합니다.  

3. **특정 키워드 알림** (예정)
   - 사용자가 설정한 키워드가 들어간 공지사항만을 선별하여 알림을 보냅니다.
  
4. **페이지 변경** (예정)
   - 전남대학교 공과대학 페이지가 아닌 메인 페이지, 타 학과 페이지의 알림 또한 설정할 수 있도록 확장합니다.

## ⚙️ 개발 환경 
사용 언어 : Python 3.9

**주요 라이브러리 및 프레임워크**
- `requests`: 웹 요청 처리  
- `beautifulsoup4`: HTML 파싱 및 크롤링  
- `python-dotenv`: 환경 변수 관리  
- `schedule`: 작업 스케줄링

---

#개발 현황

01.17 : Discord 미팅. 카카오톡 API 예제 공부. (완료)
01.19 : 요구사항 분석. 21일까지 웹페이지 크롤링 공부 목표. (완료)
01.21 : 타겟 사이트 HTML 분석 및 크롤링
