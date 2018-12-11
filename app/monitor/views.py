from datetime import datetime
from flask import g
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, current_app

from .. import db
from ..models import Comment, Post, Monitor, User, Permission
from . import monitor
from ..decorators import monitor_required, moderator_required
from ..user.forms import SearchForm
#from .forms import NoticeForm


@monitor.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.add(current_user)
        db.session.commit()
    g.search_form = SearchForm()


@monitor.route('/')
@monitor_required
#@moderator_required(Permission.MONITOR)
@login_required
def index():

    return render_template('monitor/monitor.html',
                           title='Monitor')

@monitor.route('/monitorcomment/')
@monitor_required
@login_required
def monitor_comment():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template('monitor/monitor_comment.html',
                           comments=comments,
                           pagination=pagination,
                           page=page,
                           nums=len(comments),
                           title='ManageComment')

@monitor.route('/monitorrecover/<int:id>')
@login_required
def monitor_recover(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('monitor.monitor_comment'))

@monitor.route('/monitordelate/<int:id>')
@login_required
def monitor_delate(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('monitor.monitor_comment'))

@monitor.route('/monitorpost/')
@monitor_required
@login_required
def monitor_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template('monitor/monitor_post.html',
                           posts=posts,
                           pagination=pagination,
                           page=page,
                           nums = len(posts),
                           title='ManageBlog')

@monitor.route('/recoverpost/<int:id>')
@login_required
def recover_post(id):
    post = Post.query.get_or_404(id)
    post.disabled = False
    db.session.add(post)
    return redirect(url_for('monitor.monitor_post'))

@monitor.route('/delatepost/<int:id>')
@login_required
def delate_post(id):
    post = Post.query.get_or_404(id)
    post.disabled = True
    db.session.add(post)
    return redirect(url_for('monitor.monitor_post'))


@monitor.route('/notice', methods=['GET','POST'])
@login_required
@monitor_required
def add_notice():
    notice = Monitor.query.order_by(Monitor.timestamp.desc()).first()
    if notice:
        db.session.delete(notice)
    form = NoticeForm()
    if form.validate_on_submit():
        monitor = Monitor(
            notice = form.body.data
        )
        db.session.add(monitor)
        return redirect(url_for('monitor.index'))
    return render_template('monitor/monitor_notice.html',
                           title='BlogNotice',
                           form=form)

@monitor.route('/users')
@login_required
@monitor_required
def monitor_user():
    users = User.query.all()

    return render_template('monitor/monitor_user.html',
                           title='AllUsers',
                           users=users)
