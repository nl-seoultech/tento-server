# -*- coding: utf-8 -*-
import arrow

from flask import json
from itsdangerous import JSONWebSignatureSerializer
from ..util import url_for

from tento.web.app import app
from tento.user import User

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
    """ checking [token] validity """
    assert 'token' in data
    s = JSONWebSignatureSerializer('secret_data')
    s.loads(data['token']).encode('utf-8')
