from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.product import Product
from models.user import User
from extensions import db
import logging
from datetime import datetime
from utils import security

bp = Blueprint('main', __name__)

# 관리자 로그 설정
admin_log = logging.getLogger('admin_activity')
if not admin_log.handlers:
    handler = logging.FileHandler('admin_activity.log')
    formatter = logging.Formatter('[%(asctime)s] %(message)s')
    handler.setFormatter(formatter)
    admin_log.addHandler(handler)
    admin_log.setLevel(logging.INFO)

@bp.route('/', methods=['GET', 'POST'])  # ✅ POST 허용
@login_required
def home():
    keyword = request.args.get('q', '').strip()
    products = []
    users = []

    # ✅ 프로필 업데이트 처리
    if request.method == 'POST':
        new_bio = request.form.get('bio', '').strip()
        old_pw = request.form.get('old_password', '')
        new_pw = request.form.get('new_password', '')

        current_user.bio = new_bio

        if old_pw and new_pw:
            if not current_user.check_password(old_pw):
                flash('기존 비밀번호가 일치하지 않습니다.', 'error')
            elif not security.validate_password_strength(new_pw):
                flash('비밀번호는 6자 이상이어야 합니다.', 'error')
            else:
                current_user.set_password(new_pw)
                flash('비밀번호가 변경되었습니다.')

        db.session.commit()
        flash('프로필이 업데이트되었습니다.')
        return redirect(url_for('main.home'))

    # ✅ 검색 결과 처리 (GET 요청)
    if keyword:
        products = Product.query.filter(Product.name.ilike(f'%{keyword}%')).all()
        users = User.query.filter(User.username.ilike(f'%{keyword}%')).all()

    return render_template(
        'main.html',
        user=current_user,
        products=products,
        users=users,
        keyword=keyword
    )

@bp.route('/admin/balance/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_balance(user_id):
    if not current_user.is_admin:
        flash('관리자만 접근할 수 있습니다.')
        return redirect(url_for('main.home'))

    target_user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        try:
            new_balance = float(request.form['balance'])
            if new_balance < 0:
                raise ValueError
        except ValueError:
            flash('유효한 잔액을 입력해주세요.')
            return redirect(url_for('main.edit_balance', user_id=user_id))

        target_user.balance = new_balance
        db.session.commit()
        flash(f'{target_user.username}의 잔액이 {new_balance}원으로 수정되었습니다.')
        admin_log.info(f"관리자 {current_user.username} 수정: user_id={target_user.id}, balance={new_balance}")
        return redirect(url_for('main.user_admin'))

    return render_template('admin_edit_balance.html', target_user=target_user)

@bp.route('/admin/users')
@login_required
def user_admin():
    if not current_user.is_admin:
        flash('관리자만 접근할 수 있습니다.')
        return redirect(url_for('main.home'))

    users = User.query.all()
    return render_template('admin_users.html', users=users)

@bp.route('/admin/toggle_block/<int:user_id>')
@login_required
def toggle_block(user_id):
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    user = User.query.get_or_404(user_id)
    user.is_blocked = not user.is_blocked
    db.session.commit()
    flash(f'{user.username}의 차단 상태가 변경되었습니다.')
    admin_log.info(f"관리자 {current_user.username} 차단 변경: user_id={user.id}, blocked={user.is_blocked}")
    return redirect(url_for('main.user_admin'))

@bp.route('/admin/reset_password/<int:user_id>')
@login_required
def reset_password(user_id):
    if not current_user.is_admin:
        return redirect(url_for('main.home'))
    user = User.query.get_or_404(user_id)
    user.set_password("default1234")
    db.session.commit()
    flash(f'{user.username}의 비밀번호가 기본값으로 초기화되었습니다.')
    admin_log.info(f"관리자 {current_user.username} 비밀번호 초기화: user_id={user.id}")
    return redirect(url_for('main.user_admin'))
@bp.route('/products')
@login_required
def all_products():
    products = Product.query.all()
    return render_template('product_list.html', products=products)
