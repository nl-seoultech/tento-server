from flask import Blueprint, jsonify, request, abort
from tento.user import User
from tento.db import session
from sqlalchemy.exc import IntegrityError, UnboundExecutionError

bp = Blueprint('user', __name__)


@bp.route('/', methods=['POST'])
def create_user():
    email = request.form.get('email', None) 
    password = request.form.get('password', None)
    user = User(email=email, password=password)
    session.add(user)
    if email is None or password is None:
        return jsonify(message='email, password must required')
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        abort(400)
    return jsonify(email=user.email)
