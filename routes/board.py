from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.post import Post
from app import db
from utils import security

bp = Blueprint('board', __name__)

@bp.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('board_list.html', posts=posts)

@bp.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        title = security.sanitize_input(request.form['title'])
        content = security.sanitize_input(request.form['content'])
        new_post = Post(title=title, content=content, author=current_user.username)
        db.session.add(new_post)
        db.session.commit()
        flash('게시물이 등록되었습니다.')
        return redirect(url_for('board.index'))
    return render_template('post_form.html')