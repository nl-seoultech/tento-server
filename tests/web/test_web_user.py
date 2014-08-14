# -*- coding: utf-8 -*-
from flask import json

from tento.user import User
from tento.web.app import app
from tento.web.auth import generate_token

from ..util import url_for


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


def _test_find_user(url, f_user):
    with app.test_client() as c:
        r = c.get(url)
    assert 200 == r.status_code
    assert r.data
    data = json.loads(r.data)
    assert 'id' in data
    assert 'email' in data
    assert 'name' in data
    assert f_user.email == data['email']
    assert f_user.name == data['name']


def test_web_find_user(f_session, f_user):
    u = {'id': f_user.id, 'email': f_user.email, 'name': f_user.name}
    t, _ = generate_token(u)
    url = url_for('user.find_user', id_=f_user.id, token=t)
    _test_find_user(url, f_user)


def test_web_find_me(f_session, f_user):
    u = {'id': f_user.id, 'email': f_user.email, 'name': f_user.name}
    t, _ = generate_token(u)
    url = url_for('user.find_me', id_=f_user.id, token=t)
    _test_find_user(url, f_user)


def test_web_find_other_user(f_session, f_user):
    other = User(email='admire9@gmail.com', password='foo')
    f_session.add(other)
    f_session.commit()
    u = {'id': f_user.id, 'email': f_user.email, 'name': f_user.name}
    t, _ = generate_token(u)
    url = url_for('user.find_user', id_=other.id, token=t)
    with app.test_client() as c:
        r = c.get(url)
    assert 403 == r.status_code


def test_web_find_strange_user(f_session, f_user):
    u = {'id': f_user.id, 'email': f_user.email, 'name': f_user.name}
    t, _ = generate_token(u)
    url = url_for('user.find_user', id_=1231231232, token=t)
    with app.test_client() as c:
        r = c.get(url)
    assert 404 == r.status_code
