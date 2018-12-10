from datetime import datetime
from flask import g
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, current_app

from .. import db
from ..models import Comment, Post, Moderator, User
from . import moderator
from ..decorators import moderator_required
from ..user.forms import SearchForm
from .forms import NoticeForm


@moderator.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.add(current_user)
        db.session.commit()
    g.search_form = SearchForm()


@moderator.route('/')
@moderator_required
@login_required
def index():

    return render_template('moderator/moderator.html',
                           title='Manage')

@moderator.route('/moderatorcomment/')
@moderator_required
@login_required
def moderator_comment():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template('moderator/moderator_comment.html',
                           comments=comments,
                           pagination=pagination,
                           page=page,
                           nums=len(comments),
                           title='ManageComment')

@moderator.route('/moderatorrecover/<int:id>')
@login_required
def moderator_recover(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('moderator.moderator_comment'))

@moderator.route('/moderatordelate/<int:id>')
@login_required
def moderator_delate(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('moderator.moderator_comment'))

@moderator.route('/moderatorpost/')
@moderator_required
@login_required
def moderator_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template('moderator/moderator_post.html',
                           posts=posts,
                           pagination=pagination,
                           page=page,
                           nums = len(posts),
                           title='ManageBlog')

@moderator.route('/recoverpost/<int:id>')
@login_required
def recover_post(id):
    post = Post.query.get_or_404(id)
    post.disabled = False
    db.session.add(post)
    return redirect(url_for('moderator.moderator_post'))

@moderator.route('/delatepost/<int:id>')
@login_required
def delate_post(id):
    post = Post.query.get_or_404(id)
    post.disabled = True
    db.session.add(post)
    return redirect(url_for('moderator.moderator_post'))


@moderator.route('/notice', methods=['GET','POST'])
@login_required
@moderator_required
def add_notice():
    notice = Moderator.query.order_by(Moderator.timestamp.desc()).first()
    if notice:
        db.session.delete(notice)
    form = NoticeForm()
    if form.validate_on_submit():
        moderator = Moderator(
            notice = form.body.data
        )
        db.session.add(moderator)
        return redirect(url_for('moderator.index'))
    return render_template('moderator/moderator_notice.html',
                           title='BlogNotice',
                           form=form)

@moderator.route('/users')
@login_required
@moderator_required
def moderator_user():
    users = User.query.all()

    return render_template('moderator/moderator_user.html',
                           title='AllUsers',
                           users=users)
