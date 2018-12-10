#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import redirect, url_for, abort, request
from flask_login import current_user
from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from ..models import User, Post, Comment

        
class BaseModelView(ModelView):
    
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == 'admin':
            return True
        
        return False
    
    def _handle_view(self, name, **kwargs):

        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('auth.login', next=request.url))



class UserModelView(BaseModelView):
    
    column_list = ('id', 'username', 'email', 'role_id', 'about_me', 'last_seen')
    column_searchable_list = (User.username, User.email, )
    
    def __init__(self, session, **kwargs):
        
        super(UserModelView, self).__init__(User, session, **kwargs)


class PostModelView(BaseModelView):
    
    column_list = ('author', 'title', 'body', 'timestamp', 'view_num')
    column_searchable_list = (Post.title, )
        
    def __init__(self, session, **kwargs):
        
        super(PostModelView, self).__init__(Post, session, **kwargs)

class CommentModelView(BaseModelView):

    column_list = ('author_id', 'author', 'post', 'body', 'timestamp', 'reply_to')
    column_searchable_list = (Comment.body, Comment.author_id, )
            
    def __init__(self, session, **kwargs):
        
        super(CommentModelView, self).__init__(Comment, session, **kwargs)


