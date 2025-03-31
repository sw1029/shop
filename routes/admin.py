from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models.user import User
from models.post import Post
from models.product import Product
from extensions import db
from utils import security
import os
import logging
from werkzeug.utils import secure_filename

bp = Blueprint('admin', __name__, url_prefix='/admin')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_IMAGE_SIZE_MB = 5

admin_logger = logging.getLogger('admin_logger')
admin_handler = logging.FileHandler('admin_ui.log',encoding='utf-8')
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

@bp.route('/')
@login_required
def dashboard():
    if not current_user.is_admin:
        return redirect(url_for('board.index'))
    users = User.query.all()
    posts = Post.query.all()
    products = Product.query.all()
    return render_template('admin_dashboard.html', users=users, posts=posts, products=products)

@bp.route('/block/<int:user_id>')
@login_required
def block_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('board.index'))
    user = User.query.get(user_id)
    user.is_blocked = True
    db.session.commit()
    flash('사용자가 차단되었습니다.')
    admin_logger.info(f'[차단] 관리자 {current_user.username} - 사용자 ID: {user_id}')
    return redirect(url_for('admin.dashboard'))

@bp.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    if not current_user.is_admin:
        return redirect(url_for('board.index'))
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('게시글이 삭제되었습니다.')
    admin_logger.info(f'[삭제] 관리자 {current_user.username} - 게시글 ID: {post_id}')
    return redirect(url_for('admin.dashboard'))

@bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    if not current_user.is_admin:
        return redirect(url_for('board.index'))
    post = Post.query.get(post_id)
    if request.method == 'POST':
        post.title = security.sanitize_input(request.form['title'])
        post.content = security.sanitize_input(request.form['content'])
        db.session.commit()
        flash('게시글이 수정되었습니다.')
        admin_logger.info(f'[수정] 관리자 {current_user.username} - 게시글 ID: {post_id}')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_post.html', post=post)

@bp.route('/delete_product/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not current_user.is_admin and current_user.username != product.author:
        return redirect(url_for('board.index'))
    if product.image_path and os.path.exists(product.image_path):
        os.remove(product.image_path)
    db.session.delete(product)
    db.session.commit()
    flash('상품이 삭제되었습니다.')
    admin_logger.info(f'[삭제] 관리자 {current_user.username} - 상품 ID: {product_id}')
    return redirect(url_for('admin.dashboard'))

@bp.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    if not current_user.is_admin and current_user.username != product.author:
        return redirect(url_for('board.index'))

    if request.method == 'POST':
        product.name = security.sanitize_input(request.form['name'])
        product.price = request.form['price']
        product.description = security.sanitize_input(request.form['description'])

        file = request.files.get('image')
        if file and file.filename:
            valid, message = validate_image(file)
            if not valid:
                flash(message)
                return render_template('admin/edit_product.html', product=product)
            filename = secure_filename(file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            if product.image_path and os.path.exists(product.image_path):
                os.remove(product.image_path)
            product.image_path = file_path

        db.session.commit()
        flash('상품이 수정되었습니다.')
        admin_logger.info(f'[수정] 관리자 {current_user.username} - 상품 ID: {product_id}')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_product.html', product=product)
