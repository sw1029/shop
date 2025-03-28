from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.post import Post
from models.comment import Comment
from extensions import db
from utils import security

bp = Blueprint('board', __name__)

@bp.route('/board')
@login_required
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('board_list.html', posts=posts)

@bp.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        title = security.sanitize_input(request.form['title']).strip()
        content = security.sanitize_input(request.form['content']).strip()

        if not title or len(title) > 100:
            flash('제목은 1~100자 사이여야 합니다.')
            return redirect(url_for('board.post'))

        if not content or len(content) > 1000:
            flash('내용은 1~1000자 사이여야 합니다.')
            return redirect(url_for('board.post'))

        new_post = Post(title=title, content=content, author=current_user.username)
        db.session.add(new_post)
        db.session.commit()
        flash('게시물이 등록되었습니다.')
        return redirect(url_for('board.index'))
    return render_template('post_form.html')

@bp.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment(post_id):
    content = security.sanitize_input(request.form['content']).strip()

    if not content or len(content) > 300:
        flash('댓글은 1~300자 사이여야 합니다.')
        return redirect(url_for('board.index'))

    comment = Comment(content=content, author=current_user.username, post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    flash('댓글이 등록되었습니다.')
    return redirect(url_for('board.index'))