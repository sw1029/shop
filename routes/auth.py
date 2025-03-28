from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user
from models.user import User
from app import db, login_manager, app
from werkzeug.security import check_password_hash
import time
import logging
from utils import security

bp = Blueprint('auth', __name__, url_prefix='/auth')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

admin_logger = logging.getLogger('admin_logger')
admin_handler = logging.FileHandler('admin_access.log')
admin_handler.setLevel(logging.INFO)
admin_logger.addHandler(admin_handler)

activity_logger = logging.getLogger('activity_logger')
activity_handler = logging.FileHandler(app.config['USER_ACTIVITY_LOG'])
activity_handler.setLevel(logging.INFO)
activity_logger.addHandler(activity_handler)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        # 로그인 시도 제한
        attempts = session.get('login_attempts', 0)
        locked_until = session.get('locked_until', 0)

        if time.time() < locked_until:
            flash('잠시 후 다시 시도해주세요.')
            return render_template('login.html')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password) and not user.is_blocked:
            login_user(user)
            session['login_attempts'] = 0
            client_ip = security.get_client_ip()
            activity_logger.info(f'사용자 로그인: {user.username} from {client_ip}')
            if user.is_admin:
                admin_logger.info(f'관리자 로그인: {user.username} from {client_ip}')
            return redirect(url_for('board.index'))
        else:
            attempts += 1
            session['login_attempts'] = attempts
            if attempts >= app.config['MAX_LOGIN_ATTEMPTS']:
                session['locked_until'] = time.time() + app.config['LOGIN_LOCKOUT_TIME']
                flash('로그인 시도 초과. 잠시 후 다시 시도해주세요.')
            else:
                flash('로그인 실패 또는 차단된 사용자입니다.')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        client_ip = security.get_client_ip()
        activity_logger.info(f'사용자 로그아웃: {current_user.username} from {client_ip}')
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        if not security.validate_username(username):
            flash('유효하지 않은 사용자 이름입니다. 영문자/숫자/언더스코어 3~20자')
        elif not security.validate_password_strength(password):
            flash('비밀번호는 최소 6자 이상이어야 합니다.')
        elif User.query.filter_by(username=username).first():
            flash('이미 존재하는 사용자입니다.')
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            client_ip = security.get_client_ip()
            activity_logger.info(f'사용자 회원가입: {user.username} from {client_ip}')
            flash('회원가입 완료. 로그인해주세요.')
            return redirect(url_for('auth.login'))
    return render_template('register.html')