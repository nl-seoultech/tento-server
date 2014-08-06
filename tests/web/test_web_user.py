# -*- coding: utf-8 -*-
from flask import json
from ..util import url_for

from tento.web.app import app
from tento.user import User


def _test_create_user(response, f_session):
    mail = 'admire9@gmail.com'
    assert 201 == response.status_code
    assert response.data
    data = json.loads(response.data)
    assert 'id' in data
    assert 'email' in data
    assert 'name' in data
    assert mail == data['email']
    assert 'admire9' == data['name']
    db_user = f_session.query(User)\
              .all()
    assert db_user
    assert mail == db_user[0].email


def test_web_create_user(f_session):
    """ 폼데이터로 유저생성
    """
    mail = 'admire9@gmail.com'
    with app.test_client() as client:
        response = client.post(url_for('user.create_user'),
                               data={'email': mail,
                                     'password': 'foobar'})
    _test_create_user(response, f_session)


def test_web_create_user_by_json(f_session):
    """ json으로 유저생성
    """
    mail = 'admire9@gmail.com'
    with app.test_client() as client:
        response = client.post(url_for('user.create_user'),
                               data=json.dumps({'email': mail,
                                                'password': 'foobar'}),
                               content_type='application/json')
    _test_create_user(response, f_session)
