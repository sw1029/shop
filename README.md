# shop

# Flask 테스트 웹사이트

이 프로젝트는 Flask를 기반으로 한 테스트용 웹사이트입니다. 주요 기능으로는 게시판, 상품 등록, 악성 유저 차단 기능 등이 포함되어 있습니다.

## 주요 기능

- 사용자 인증 및 로그인
- 게시판 등록/조회
- 상품 등록/조회
- 관리자 기능 (악성 사용자 차단)

## 프로젝트 구조

```plaintext
project/
│
├── app.py                  # 앱 실행 파일 (Flask 인스턴스 실행)
├── config.py               # 환경 설정
├── requirements.txt        # 의존성 명시
│
├── models/                 # 데이터베이스 모델
│   └── user.py
│   └── post.py
│   └── product.py
│
├── routes/                 # 라우팅 핸들러
│   └── auth.py
│   └── board.py
│   └── product.py
│   └── admin.py
│
├── templates/              # HTML 템플릿
│   └── base.html
│   └── login.html
│   └── board_list.html
│   └── product_form.html
│
├── static/                 # 정적 파일 (CSS, JS, 이미지)
│
├── forms/                  # Flask-WTF 폼
│   └── login_form.py
│   └── product_form.py
│
└── utils/                  # 도우미 함수 (보안, 필터 등)
    └── security.py

