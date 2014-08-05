# -*- coding: utf-8 -*-
from pytest import fixture
from flask import _request_ctx_stack, g
from sqlalchemy.orm import sessionmaker

from tento.web.app import app
from tento.db import get_session, Base, get_engine
from tento.user import User


@fixture
def f_session(request):
    with app.test_request_context() as _ctx:
        Session = sessionmaker(autocommit=False, autoflush=False)
        app.config['DATABASE_URL'] = 'sqlite:///test.db'
        engine = get_engine(app)
        Base.metadata.create_all(engine)
        _ctx.push()
        session = Session(bind=engine)
        setattr(g, 'sess', session)
        def finish():
            session.close()
            Base.metadata.drop_all(engine)
            engine.dispose()

        request.addfinalizer(finish)
        return session


@fixture
def f_user(f_session):
    email = 'mytest@test.com'
    password = 'mytest:password'
    u = User(email=email, password=password)
    f_session.add(u)
    f_session.commit()
    return u
