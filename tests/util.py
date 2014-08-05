# -*- coding: utf-8 -*-
from flask import url_for as flask_url_for

from tento.web.app import app


def url_for(*args, **kwargs):
    """ `flask.url_for`는 flask 앱의 context가 필요합니다. 따라서 context안에서
    생성한 url을 가져와서 사용하면됩니다. 테스트 코드 내부에서 그냥
    `flask.url_for`를 사용하면 에러가 나게됩니다.
    """
    with app.test_request_context() as ctx_:
        return flask_url_for(*args, **kwargs)
