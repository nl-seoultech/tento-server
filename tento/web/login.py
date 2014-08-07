# -*- coding: utf-8 -*-
import arrow

from flask import Blueprint, jsonify, request, abort
from itsdangerous import JSONWebSignatureSerializer
from sqlalchemy.exc import IntegrityError

from tento.db import session
from tento.user import User

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
    resp = {
        'user': {'id': user[0].id,
                 'email': user[0].email,
                 'name': user[0].name},
        'expired_at': arrow.utcnow().replace(hours=+2).timestamp
    }
    secret_key = 'secret_key'
    s = JSONWebSignatureSerializer(secret_key)
    return jsonify(token=s.dumps(resp).decode('utf-8'), **resp)
