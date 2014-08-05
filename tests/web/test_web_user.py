# -*- coding: utf-8 -*-
from flask import json

from tento.web.app import app


def test_web_create_user(f_session):
    """ 유저를 생성하는 api를 테스트해봅니다.
    테스트 코드는 아래와 비슷한 코드구조를 가지게됩니다.

    .. sourcecode::python

       with app.test_client() as client:
           response = client.post(url_for('users.create_user'),
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
       db_user = f_session.query(User)\
                 .filter(User.email == 'admire9@gmail.com')\
                 .all()
       assert db_user
       assert json['id'] == db_user[0]['id']
    """
    pass
