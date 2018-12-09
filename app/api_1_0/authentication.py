from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth

from . import api
from .errors import unauthorized, forbidden
from ..models import AnonymousUser, User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = User.verify_auth_token(username)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(username=username).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_authenticated:
        return forbidden('Unconfirmed account')


@api.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})
