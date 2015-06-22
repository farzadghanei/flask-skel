from flask import current_app, request, jsonify, session
from flask.ext.login import login_user, current_user, logout_user

from ..services.user import UserService
from . import api_v1

@api_v1.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated():
        return jsonify(success=True)
    data = request.get_json()
    if not data:
        return jsonify(success=False, message='Please provide token or email and password in valid JSON format')
    session['credentials_used'] = False
    service = UserService(current_app.logger)
    token = data.get('token')
    if token:
        user = service.authenticate(current_app.config['SECRET_KEY'], token)
    else:
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify(success=False, message='Please provide a token or email and password in valid JSON format')
        user = service.authenticate(current_app.config['SECRET_KEY'], email, password)
        session['credentials_used'] = True
    if user and login_user(user, remember='y'):
        current_app.logger.debug("API user '{}' logged in".format(email))
        return jsonify(success=True)

    current_app.logger.debug("API user login failed")
    return jsonify(success=False, message='Login failed')

@api_v1.route('/logout')
def logout():
    if current_user.is_authenticated():
        logout_user()
    current_app.logger.debug("API user '{}' logged out".format(current_user))
    return jsonify(success=True, message='Logged Out')
