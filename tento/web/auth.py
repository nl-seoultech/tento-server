# -*- coding: utf-8 -*-
from functools import wraps

from arrow import utcnow, Arrow
from flask import g, request, abort
from itsdangerous import JSONWebSignatureSerializer, BadSignature

from ..db import session
from ..user import User


def get_secret_key():
    from tento.web.app import app
    k = app.config.get('SECRET_KEY', None)
    if k is None:
        raise Exception('`SECRET_KEY`는 반드시 필요합니다.')
    return k


def generate_token(user):
    secret_key = get_secret_key()
    s = JSONWebSignatureSerializer(secret_key)
    expired_at = utcnow().replace(hours=+2).timestamp
    d = {'user': user, 'expired_at': expired_at}
    token = s.dumps(d).decode('utf-8')
    return token, d


def validate_token(token):
    if not isinstance(token, str):
        raise TypeError('token은 반드시 `str` 이여야합니다.')
    secret_key = get_secret_key()
    s = JSONWebSignatureSerializer(secret_key)
    try:
        data = s.loads(token.encode('utf-8'))
    except BadSignature as e:
        raise InvalidTokenError('잘못된 token입니다.')
    expired_at = Arrow.fromtimestamp(data['expired_at'])
    now = utcnow()
    if expired_at < now:
        raise ExpiredTokenError('만료된 token입니다.')
    return data


def authorized_user(token):
    d = validate_token(token)
    user_id = d['user']['id']
    u = session.query(User)\
        .filter(User.id == user_id)\
        .all()
    if not u:
        return None
    return u[0]


def auth_required(f):
    @wraps(f)
    def deco(*args, **kwargs):
        token = request.args.get('token', None) or request.headers.get('Authorization')
        try:
            u = authorized_user(token)
        except TypeError as e:
            abort(400)
        except InvalidTokenError as e:
            abort(400)
        except ExpiredTokenError as e:
            abort(400)
        if u is None:
            abort(403)
        g.current_user = u
        return f(*args, **kwargs)
    return deco


class InvalidTokenError(Exception):
    pass


class ExpiredTokenError(Exception):
    pass
