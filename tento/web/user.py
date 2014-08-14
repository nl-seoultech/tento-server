# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, abort, g
from sqlalchemy.exc import IntegrityError

from ..db import session
from ..user import User
from .auth import auth_required

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


@bp.route('/<int:id_>/', methods=['GET'])
@auth_required
def find_user(id_):
    user = session.query(User)\
           .filter(User.id == id_)\
           .first()
    if user is None:
        abort(404)
    if g.current_user and g.current_user.id != user.id:
        abort(403)
    return jsonify(id=g.current_user.id,
                   email=g.current_user.email,
                   name=g.current_user.name)


@bp.route('/me/', methods=['GET'])
@auth_required
def find_me():
    return jsonify(id=g.current_user.id,
                   email=g.current_user.email,
                   name=g.current_user.name)
