B2B-Subscription-Email-RPA

B2B Subscription Email RPA는 고객사가 통신사로 전송한 청약 메일을 자동으로 분석하고 처리하는 AI + RPA 기반 엔드투엔드 자동화 프로젝트입니다.
메일 수신부터 GPT 기반 정보 추출, Excel 파일 생성, UiPath를 통한 웹 입력까지 전체 자동화 파이프라인을 구현했습니다.

📒 프로젝트 개요

기간: 2025.07.22 ~ 2025.08.02 (약 2주)

개발 인원: 개인 프로젝트

역할: 기획 · 설계 · 개발 전 과정 담당

기여도: 100%

기술 스택:

백엔드: Python, FastAPI

AI: OpenAI GPT API

RPA: UiPath

DB: MySQL (SQLAlchemy ORM)

주요 목표:

반복적 이메일 청약 처리 자동화

자유 양식 이메일에서 GPT를 통한 데이터 구조화

엑셀 생성 후 UiPath 자동 입력

🛠 문제 상황 해결

과거 U+ 프로젝트 경험에서 발생한 문제

고객사 메일 본문 형식이 제각각 → 데이터 추출 불가

다양한 고객사 메일 주소로 인해 필터링 어려움

본문 전체를 그대로 입력해야 했고 HTML 태그로 가독성 저하

당시(2023년 11월)는 AI 도입 부족 → GPT 활용 불가

이번 프로젝트를 통해 GPT 기반 구조화 + RPA 자동화로 문제 극복

🙍‍♀️ 역할 및 성과
DB 및 아키텍처 설계

3개 테이블(mails_info, gpt_subscriptions, rpa_results) 기반 ERD 설계

메일 원본 → GPT 분석 결과 → UiPath 실행 결과 추적 가능

uid와 pk로 메일 처리 이력과 GPT/RPA 결과 연결

메일 추출 로직

Gmail IMAP API를 활용하여 마지막 처리 UID 이후 메일만 수집

멀티파트(텍스트/HTML) 메일도 정규화된 텍스트만 추출

mails_info 테이블에 저장 후 GPT 요청용 JSON 변환

GPT 기반 청약 데이터 추출

자유 양식 메일에서 청약 여부 및 필드 추출 (JSON 스키마)

추출 필드: 회사명, 담당자, 연락처, 서비스명, 회선 수, 주소, 설치일, 계약 유형, 추가 요청 사항

is_subscription 플래그로 청약 메일 구분

RPA 자동화 연계

Python에서 UiPath 실행 명령 호출 → 엑셀 기반 웹 입력 자동화

성공/실패 및 에러 메시지 rpa_results에 기록

재시도 가능 구조 설계

🔔 자동화 데이터 흐름

Email 수신: IMAP으로 DB에 저장된 마지막 처리 UID 이후 미처리 메일 수집

GPT 데이터 추출: 자유 양식 메일 → GPT → JSON 필드 추출

엑셀 파일 생성: 청약 메일 필터링 후 엑셀 작성

UiPath 자동화 수행: Python에서 UiPath 호출 → 웹 입력 자동화

💡 성장 포인트

규칙 기반 RPA 한계 극복

HTML/비정형 데이터 문제 → GPT로 자유 양식 JSON 변환

메일 처리 성능 최적화

UID 기준 처리 범위 지정 → 성능과 신뢰성 확보

RPA와 AI 실무적 연계 경험

GPT 결과 → 엑셀 → UiPath 입력 흐름 구현

실제 업무 환경과 유사한 엔드투엔드 파이프라인 경험
