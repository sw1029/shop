# create_admin.py
from app import app
from extensions import db
from models.user import User

with app.app_context():
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', is_admin=True)
        admin.set_password('1234')  # 원하는 비밀번호 입력
        db.session.add(admin)
        db.session.commit()
        print("관리자 계정이 생성되었습니다.")
    else:
        print("'admin' 계정이 이미 존재합니다.")
