# -*- coding: utf-8 -*-
import arrow

from flask import json
from itsdangerous import JSONWebSignatureSerializer
from pytest import raises

from tento.user import User
from tento.web.app import app
from tento.web.auth import validate_token, get_secret_key, InvalidTokenError, ExpiredTokenError

from ..util import url_for


def test_web_login(f_session, f_user):
    email = 'mytest@test.com'
    password = 'mytest:password'
    with app.test_client() as client:
        response = client.post(url_for('login.login'),
                               data={'email': email, 'password': password})
    assert 200 == response.status_code
    assert response.data
    data = json.loads(response.data)
    assert 'user' in data
    assert 'id' in data['user']
    assert 'email' in data['user']
    assert 'name' in data['user']
    assert 'token' in data
    assert f_user.id == data['user']['id']
    assert f_user.email == data['user']['email']
    assert f_user.name == data['user']['name']
    assert 'token' in data
    user_data = validate_token(data['token'])
    assert f_user.id == user_data['user']['id']
    assert f_user.email == user_data['user']['email']
    assert f_user.name == user_data['user']['name']


def test_invalid_token(f_session, f_user):
    secret_key = get_secret_key()
    s = JSONWebSignatureSerializer(secret_key)
    expired_at = arrow.utcnow().replace(hours=-2).timestamp
    d = {
        'user': {'id': f_user.id, 'email': f_user.email, 'name': f_user.name},
        'expired_at': expired_at
    }
    token = s.dumps(d).decode('utf-8')
    with raises(InvalidTokenError):
        t = validate_token('dadfa.asdf')
    with raises(ExpiredTokenError):
        t = validate_token(token)
