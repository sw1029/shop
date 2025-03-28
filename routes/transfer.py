from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.user import User
from extensions import db

bp = Blueprint('transfer', __name__, url_prefix='/transfer')  # ✅ 이 줄 추가


@bp.route('/', methods=['GET', 'POST'])
@login_required
def send():
    if request.method == 'POST':
        recipient_name = request.form['recipient'].strip()

        try:
            amount = float(request.form['amount'])
            if amount <= 0:
                raise ValueError
        except ValueError:
            flash('유효한 송금 금액을 입력해주세요.')
            return redirect(url_for('transfer.send'))

        recipient = User.query.filter_by(username=recipient_name).first()
        if not recipient:
            flash('수신자 계정이 존재하지 않습니다.')
            return redirect(url_for('transfer.send'))

        if not current_user.is_admin and current_user.balance < amount:
            flash('잔액이 부족합니다.')
            return redirect(url_for('transfer.send'))

        if not current_user.is_admin:
            current_user.balance -= amount
        recipient.balance += amount
        db.session.commit()
        flash(f'{recipient.username}에게 {amount}원을 송금했습니다.')
        return redirect(url_for('main.home'))

    return render_template('transfer.html')
