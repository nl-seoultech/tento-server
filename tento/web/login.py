# -*- coding: utf-8 -*-
import arrow

from flask import Blueprint, jsonify, request, abort
from sqlalchemy.exc import IntegrityError

from ..db import session
from ..user import User
from .auth import generate_token

bp = Blueprint('login', __name__)


@bp.route('/', methods=['POST'])
def login():
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if email is None or password is None:
        abort(400)
    user = session.query(User)\
           .filter(User.email == email)\
           .all()
    if not user:
        abort(404)
    if not user[0].confirm_password(password):
        abort(404)
    u = {'id': user[0].id, 'email': user[0].email, 'name': user[0].name}
    token, resp = generate_token(u)
    return jsonify(token=token, **resp)
