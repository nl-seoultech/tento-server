# -*- coding: utf-8 -*-
""" :mod:`tento.db` --- tento의 DB의 설정과 관련된 모듈
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import current_app, g
from alembic.config import Config
from alembic.script import ScriptDirectory
from werkzeug.local import LocalProxy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


__all__ = ('Base', 'ensure_shutdown_session', 'get_engine', 'get_session',
           'get_alembic_config')


def get_alembic_config(engine):
    """ :py:mod:`alembic` 에필요한 설정을 가져옵니다.

    :param engine: db에 연결할 :py:class:`sqlalchemy.engine.Engine` 인스턴스
    :return: alembic 사용할때 필요한 설정이 담긴 
             :py:class:`alembic.config.Config`
    :rtype: :py:class:`alembic.config.Config`

    :param flask.Flask app: :py:class:`flask.Flask` 로 생성한 앱
    """
    if engine is not None:
        url = str(engine.url)
        config = Config()
        config.set_main_option('script_location',
                               current_app.config['ALEMBIC_SCRIPT_LOCATION'])
        config.set_main_option('sqlalchemy.url', url)
        config.set_main_option('url', url)
        return config
    else:
        raise 'no engine founded. DATABASE_URL can be misconfigured.'


def ensure_shutdown_session(app):
    """ :py:attr:`tento.web.app.app` 의 문맥이 종료될때,
    :py:attr:`tento.db.session` 이 반드시 닫히도록 합니다.
    """
    def remove_or_rollback(exc=None):
        if hasattr(g, 'sess'):
            if exc:
                g.sess.rollback()
            g.sess.close()

    app.teardown_appcontext(remove_or_rollback)


def get_engine(app=None):
    """ DB 연결에 필요한 엔진을 생성합니다.

    :param flask.Flask app: :py:class:`flask.Flask` 로 생성한 앱
    :return: :py:mod:`sqlalchemy` 의 엔진
    :rtype: :py:class:`sqlalchemy.engine.Engine`
    """
    app = app if app else current_app
    if app.config.get('DATABASE_URL', None) is not None:
        return create_engine(app.config.get('DATABASE_URL', None))


def get_session(engine=None):
    """ :py:mod:`sqlalchemy` 의 쿼리를 날릴때 사용하는 세션을 가지고옵니다.

    :param sqlalchemy.engine.Engine engine: :py:mod:`sqlalchemy` 엔진
    :return: DB에 쿼리를 날리때 사용하는 세션
    :rtype: :py:class:`sqlalchemy.orm.session.Session`
    """
    if engine is None:
        engine = get_engine()
    if not hasattr(g, 'sess'):
        setattr(g, 'sess', Session(bind=engine))
    return getattr(g, 'sess')


Base = declarative_base()
Session = sessionmaker()
session = LocalProxy(get_session)
