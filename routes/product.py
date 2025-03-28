from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from models.product import Product
from app import db
from utils import security
import os
import logging
from werkzeug.utils import secure_filename

bp = Blueprint('product', __name__, url_prefix='/product')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_IMAGE_SIZE_MB = 5

# 관리자 로그 추적
admin_logger = logging.getLogger('admin_logger')
admin_handler = logging.FileHandler('admin_ui.log')
admin_handler.setLevel(logging.INFO)
admin_logger.addHandler(admin_handler)
admin_logger.propagate = False


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file):
    if not allowed_file(file.filename):
        return False, '허용되지 않는 이미지 형식입니다.'
    file.seek(0, os.SEEK_END)
    size_mb = file.tell() / (1024 * 1024)
    file.seek(0)
    if size_mb > MAX_IMAGE_SIZE_MB:
        return False, '이미지 크기는 최대 5MB를 초과할 수 없습니다.'
    return True, ''

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_product():
    if request.method == 'POST':
        name = security.sanitize_input(request.form['name'])
        price = request.form['price']
        description = security.sanitize_input(request.form['description'])

        file = request.files.get('image')
        image_path = None

        if file and file.filename:
            valid, message = validate_image(file)
            if not valid:
                flash(message)
                return render_template('product_form.html')
            filename = secure_filename(file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            image_path = file_path

        product = Product(
            name=name,
            price=price,
            description=description,
            image_path=image_path,
            author=current_user.username
        )
        db.session.add(product)
        db.session.commit()
        flash('상품이 등록되었습니다.')
        if current_user.is_admin:
            admin_logger.info(f'[등록] 관리자 {current_user.username} - 상품명: {name}')
        return redirect(url_for('board.index'))
    return render_template('admin/product_form.html' if current_user.is_admin else 'product_form.html')

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
