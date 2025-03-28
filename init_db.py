# init_db.py
from app import app
from extensions import db

with app.app_context():
    db.create_all()
    print("DB 테이블 생성 완료")
