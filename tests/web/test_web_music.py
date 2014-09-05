# -*- coding: utf-8 -*-
from flask import json

from tento.web.app import app
from tento.music import Artist, Album, Music, Genre, Position

from ..util import url_for


def test_web_no_json_create_music(f_session):
    """ json으로 음악생성
    """
    with app.test_client() as client:
        response = client.post(url_for('music.create'),
                               content_type='application/json')
    assert 400 == response.status_code


def test_web_create_music(f_session):
    payload = {
        'music_name': '유감',
        'music_track_number': 1,
        'music_disc_number': 1,
        'artist_name': 'leeSA',
        'album_name': '유감',
        'album_release_year': 2010,
        'genre': '팝 > 팝, 팝 > 발라드'
    }
    with app.test_client() as client:
        response = client.post(url_for('music.create'),
                               data=json.dumps(payload),
                               content_type='application/json')
    # response 상태
    assert 201 == response.status_code
    # artist 데이터 생성 확인
    artist = f_session.query(Artist)\
             .filter(Artist.name == payload['artist_name'])\
             .first()
    assert artist
    assert artist.name
    assert artist.created_at
    assert payload['artist_name'] == artist.name
    # album 데이터 생성 확인
    album = f_session.query(Album)\
            .filter(Album.name == payload['album_name'])\
            .first()
    assert album
    assert album.name
    assert album.created_at
    assert album.year
    assert album.artist_id
    assert artist.id == album.artist.id
    # genre 데이터 생성 확인
    genre = f_session.query(Genre)\
            .filter(Genre.name == payload['genre'])\
            .first()
    assert genre
    assert genre.name
    assert genre.created_at
    # music 데이터 생성 확인
    music = f_session.query(Music)\
            .filter(Music.name == payload['music_name'])\
            .first()
    assert music
    assert music.name == payload['music_name']
    assert music.created_at
    assert music.album_id
    assert album.id == music.album.id
    assert music.genre_id
    assert genre.id == music.genre.id


def test_web_no_json_create_position(f_session):
    """ json으로 position(음악의 좌표 데이터)를 생성
    """
    with app.test_client() as client:
        response = client.post(url_for('music.position'),
                               content_type='application/json')
    assert 400 == response.status_code


def test_web_create_position(f_session):
    payload = {
            'music_name': 'Someone Like You',
            'music_track_number': 1,
            'music_disc_number': 1,
            'artist_name': 'Adele',
            'album_name': '21',
            'album_release_year': 2011,
            'genre': '팝',
    }
    # music 데이터 생성
    with app.test_client() as client:
        response = client.post(url_for('music.create'),
                               data=json.dumps(payload),
                               content_type='application/json')
    #response 상태
    assert 201 == response.status_code
    music = f_session.query(Music)\
            .filter(Music.name == payload['music_name'])\
            .first()
    assert music
    assert 1 == music.id

    payload2 = {
            'x': 10,
            'y': 9,
            'music_id': 1
    }
    # position 데이터 생성
    with app.test_client() as client:
        response = client.post(url_for('music.position'),
                               data=json.dumps(payload2),
                               content_type='application/json')
    #response 상태
    assert 201 == response.status_code
    # position 생성 확인
    position = f_session.query(Position)\
               .filter(Position.music_id == payload2['music_id'])\
               .first()
