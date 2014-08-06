# -*- coding: utf-8 -*-
from flask import json
from ..util import url_for
from tento.web.app import app


def test_web_create_user(f_session):
    """ 유저를 생성하는 api를 테스트해봅니다.
    테스트 코드는 아래와 비슷한 코드구조를 가지게됩니다.

    .. sourcecode::python

    """

    with app.test_client() as client:
        response = client.post(url_for('user.create_user'),
                           data={'email': 'admire9@gmail.com',
                                 'password': 'foobar'})


    assert 201 == response.status_code
    assert response.data
    json = json.loads(response.data)
    assert 'id' in json
    assert 'email' in json
    assert 'name' in json
    assert 'admire9@gmail.com' == json['email']
    assert 'admire9' == json['name']
    user = f_session.query(User)\
              .all()
    assert user
    assert 'admire9@gmail.com' == db_user[0].mail
