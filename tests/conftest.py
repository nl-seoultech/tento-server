# -*- coding: utf-8 -*-
from pytest import fixture
from flask import _request_ctx_stack, g
from sqlalchemy.orm import sessionmaker

from tento.web.app import app
from tento.db import get_session, Base, get_engine
from tento.user import User
from tento.music import Artist, Album, Genre, Music


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


@fixture
def f_genre(f_session):
    name = 'pop'
    genre = Genre(name=name)
    f_session.add(genre)
    f_session.commit()
    return genre


@fixture
def f_artist(f_session):
    name = 'Adele'
    artist = Artist(name=name)
    f_session.add(artist)
    f_session.commit()
    return artist


@fixture
def f_album(f_session, f_artist):
    name = '21'
    year = 2008
    album = Album(name=name,
                  artist=f_artist,
                  year=year)
    f_session.add(album)
    f_session.commit()
    return album


@fixture
def f_music(f_session, f_genre, f_album):
    name = 'Someone Like You'
    track_number = 1
    disc_number = 1
    music = Music(name=name,
                  album=f_album,
                  genre=f_genre,
                  track_number=track_number,
                  disc_number=disc_number)
    f_session.add(music)
    f_session.commit()
    return music
