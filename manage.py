#!/usr/bin/env python
import os

from flask_login import current_user
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from app import create_app, db
from app.models import User, Role, Post, Comment, Follow, Permission, Noticer, Monitor, Moderator
from app.admin.views import UserModelView, PostModelView, CommentModelView


app = create_app(os.getenv('CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

    
admin = Admin(app, index_view=AdminIndexView(name='Welcome', 
                                             template='admin/index.html',
                                             url='/admin'))
admin.add_view(UserModelView(db.session, endpoint="allusers"))
admin.add_view(PostModelView(db.session, endpoint="allposts"))
admin.add_view(CommentModelView(db.session, endpoint="allcomments"))




def make_shell_context():

    return dict(app=app, db=db, User=User, Role=Role, Post=Post, \
                Follow=Follow, Permission=Permission, Moderator=Moderator,
                Monitor=Monitor, Noticer=Noticer, Admin=Admin)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.models import Role
    # Database Migration
    upgrade()
    # Build user roles
    Role.insert_roles()


if __name__ == '__main__':
    manager.run()
