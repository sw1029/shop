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
shop/
├── app.py
├── config.py
├── create_admin.py
├── extensions.py
├── init_db.py
├── requirements.txt
├── README.md
│
├── forms/
│   ├── login_form.py
│   └── product_form.py
│
├── instance/
│   └── db
│
├── models/
│   ├── comment.py
│   ├── post.py
│   ├── product.py
│   └── user.py
│
├── routes/
│   ├── admin.py
│   ├── auth.py
│   ├── board.py
│   ├── main.py
│   ├── product.py
│   ├── static_product.py
│   └── transfer.py
│
├── templates/
│   ├── admin/
│   │   ├── edit_post.html
│   │   ├── edit_product.html
│   │   └── product_form.html
│   ├── admin_dashboard.html
│   ├── admin_edit_balance.html
│   ├── admin_users.html
│   ├── base.html
│   ├── board_list.html
│   ├── edit_product.html
│   ├── login.html
│   ├── main.html
│   ├── post_form.html
│   ├── product_form.html
│   ├── product_list.html
│   ├── register.html
│   ├── static_product.html
│   └── transfer.html
│
├── utils/
│   └── security.py
│
└── static/
    └── (정적 파일: 이미지, CSS 등)

```
## 사용 방법
- pip install -m requirements.txt

- python init_db.py

- create_admin에서 관리자 id, pw 설정
- python create_admin.py

이후 app.py 실행 후 127.0.0.1:5000 으로 접속 시 정상적으로 실행됩니다.