# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, abort
from sqlalchemy.exc import IntegrityError

from tento.db import session
from tento.user import User

bp = Blueprint('user', __name__)


@bp.route('/', methods=['POST'])
def create_user():
    if request.content_type == 'application/x-www-form-urlencoded':
        email = request.form.get('email', None)
        password = request.form.get('password', None)
    elif request.content_type == 'application/json':
        payload = request.json
        email = payload.get('email', None)
        password = payload.get('password', None)
    user = User(email=email, password=password)
    session.add(user)
    if email is None or password is None:
        abort(400)
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        abort(500)
    return jsonify(email=user.email, id=user.id, name=user.name), 201
