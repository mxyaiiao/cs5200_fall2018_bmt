from datetime import datetime
from flask import g
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, current_app

from .. import db
from ..models import Comment, Post, Noticer, User, Permission
from . import noticer
from ..decorators import noticer_required
from ..user.forms import SearchForm
from .forms import NoticeForm


@noticer.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.add(current_user)
        db.session.commit()
    g.search_form = SearchForm()


@noticer.route('/')
@noticer_required
@login_required
def index():

    return render_template('noticer/noticer.html',
                           title='Manage')

@noticer.route('/noticercomment/')
@noticer_required
@login_required
def noticer_comment():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template('noticer/noticer_comment.html',
                           comments=comments,
                           pagination=pagination,
                           page=page,
                           nums=len(comments),
                           title='ManageComment')

@noticer.route('/noticerrecover/<int:id>')
@login_required
def noticer_recover(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('noticer.noticer_comment'))

@noticer.route('/noticerdelate/<int:id>')
@login_required
def noticer_delate(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('noticer.noticer_comment'))

@noticer.route('/noticerpost/')
@noticer_required
@login_required
def noticer_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template('noticer/noticer_post.html',
                           posts=posts,
                           pagination=pagination,
                           page=page,
                           nums = len(posts),
                           title='ManageBlog')

@noticer.route('/recoverpost/<int:id>')
@login_required
def recover_post(id):
    post = Post.query.get_or_404(id)
    post.disabled = False
    db.session.add(post)
    return redirect(url_for('noticer.noticer_post'))

@noticer.route('/delatepost/<int:id>')
@login_required
def delate_post(id):
    post = Post.query.get_or_404(id)
    post.disabled = True
    db.session.add(post)
    return redirect(url_for('noticer.noticer_post'))


@noticer.route('/notice', methods=['GET','POST'])
@login_required
@noticer_required
def add_notice():
    notice = Noticer.query.order_by(Noticer.timestamp.desc()).first()
    if notice:
        db.session.delete(notice)
    form = NoticeForm()
    if form.validate_on_submit():
        noticer = Noticer(
            notice = form.body.data
        )
        db.session.add(noticer)
        return redirect(url_for('noticer.index'))
    return render_template('noticer/noticer_notice.html',
                           title='BlogNotice',
                           form=form)

@noticer.route('/users')
@login_required
@noticer_required
def noticer_user():
    users = User.query.all()

    return render_template('noticer/noticer_user.html',
                           title='AllUsers',
                           users=users)
