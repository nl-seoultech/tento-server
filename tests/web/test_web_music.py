# -*- coding: utf-8 -*-
from random import randint

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


def test_web_create_chunk_music(f_session):
    payload = {
        'musics': [
            {
                'music_name': '유감',
                'music_track_number': 1,
                'music_disc_number': 1,
                'artist_name': 'leeSA',
                'album_name': '유감',
                'album_release_year': 2010,
                'genre': '팝 > 팝, 팝 > 발라드'
            },
            {
                'music_name': '유감',
                'music_track_number': 1,
                'music_disc_number': 1,
                'artist_name': 'leeSA',
                'album_name': '유감',
                'album_release_year': 2010,
                'genre': '팝 > 팝, 팝 > 발라드'
            },
            {
                'music_name': 'Could you stop that smile ?',
                'music_track_number': 1,
                'music_disc_number': 1,
                'artist_name': 'leeSA',
                'album_name': '유감',
                'album_release_year': 2010,
                'genre': '팝 > 팝, 팝 > 발라드'
            },
        ]
    }
    with app.test_client() as client:
        response = client.post(url_for('music.create_chunks'),
                               data=json.dumps(payload),
                               content_type='application/json')
    # response 상태
    assert 201 == response.status_code
    # artist 데이터 생성 확인
    artist = f_session.query(Artist)\
             .filter(Artist.name == payload['musics'][0]['artist_name'])\
             .first()
    assert artist
    assert artist.name
    assert artist.created_at
    assert payload['musics'][0]['artist_name'] == artist.name
    print([x.name for x in f_session.query(Artist).all()])
    assert 1 == f_session.query(Artist).count()
    # album 데이터 생성 확인
    album = f_session.query(Album)\
            .filter(Album.name == payload['musics'][0]['album_name'])\
            .first()
    assert album
    assert album.name
    assert album.created_at
    assert album.year
    assert album.artist_id
    assert artist.id == album.artist.id
    assert 1 == f_session.query(Album).count()
    # genre 데이터 생성 확인
    genre = f_session.query(Genre)\
            .filter(Genre.name == payload['musics'][0]['genre'])\
            .first()
    assert genre
    assert genre.name
    assert genre.created_at
    assert 1 == f_session.query(Genre).count()
    # music 데이터 생성 확인
    for v in payload['musics']:
        music = f_session.query(Music)\
                .filter(Music.name == v['music_name'])\
                .first()
        assert music
        assert music.name == v['music_name']
        assert music.created_at
        assert music.album_id
        assert album.id == music.album.id
        assert music.genre_id
        assert genre.id == music.genre.id
    assert 2 == f_session.query(Music).count()
    assert response.data
    data = json.loads(response.data)
    assert 'musics' in data
    assert data['musics']
    exp = [{'id': x.id, 'name': x.name} for x in f_session.query(Music).all()]
    assert exp == data['musics']


def test_web_no_json_create_position(f_session, f_music):
    """ json으로 position(음악의 좌표 데이터)를 생성
    """
    with app.test_client() as client:
        response = client.post(url_for('music.position', id_=f_music.id),
                               content_type='application/json')
    assert 400 == response.status_code


def test_web_notfound_create_position(f_session, f_music):
    payload = {'x': 10, 'y': 9}
    with app.test_client() as client:
        response = client.post(url_for('music.position', id_=f_music.id + 1),
                               data=json.dumps(payload),
                               content_type='application/json')
    assert 404 == response.status_code


def test_web_create_position(f_session, f_music):
    payload = {'x': 10, 'y': 9}
    # position 데이터 생성
    with app.test_client() as client:
        response = client.post(url_for('music.position', id_=f_music.id),
                               data=json.dumps(payload),
                               content_type='application/json')
    #response 상태
    assert 201 == response.status_code
    # position 생성 확인
    position = f_session.query(Position)\
               .filter(Position.music_id == f_music.id)\
               .first()
    assert position
    assert payload['x'] == position.x
    assert payload['y'] == position.y
    assert f_music.id == position.music_id


def test_web_notfound_find_position(f_session, f_music):
    url = url_for('music.find_position', id_=f_music.id + 1)
    with app.test_client() as client:
        response = client.get(url)
    assert 404 == response.status_code


def test_web_find_position(f_session, f_position):
    url = url_for('music.find_position', id_=f_position.music.id)
    with app.test_client() as client:
        response = client.get(url)
    assert 200 == response.status_code
    assert response.data
    data = json.loads(response.data)
    assert data
    assert 'x' in data
    assert 'y' in data
    assert 'music_id' in data
    assert f_position.x == data['x']
    assert f_position.y == data['y']
    assert f_position.music_id == data['music_id']


def test_web_noquery_all_pos(f_session, f_position):
    url = url_for('music.find_all_positions')
    with app.test_client() as c:
        r = c.get(url)
    assert 400 == r.status_code


def test_web_weired_query_all_pos(f_session, f_position):
    url = url_for('music.find_all_positions', music_ids='hehe,weired')
    with app.test_client() as c:
        r = c.get(url)
    assert 400 == r.status_code


def test_web_find_all_pos(f_session, f_position, f_album):
    musics = []
    for x in range(1, 10):
        music = Music(name='music {}'.format(x),
                      album=f_album,
                      track_number=x,
                      disc_number=1)
        f_session.add(music)
        f_session.add(Position(x=randint(1, 100),
                               y=randint(1, 100),
                               music=music))
        musics.append(music)
    f_session.commit()
    url = url_for('music.find_all_positions',
                  music_ids=','.join([str(x.id) for x in musics]))
    with app.test_client() as c:
        r = c.get(url)
    assert 200 == r.status_code
    assert r.data
    data = json.loads(r.data)
    assert data
    assert 'positions' in data
    assert data['positions']
    expect_ids = [x.id for x in musics]
    result_ids = [x['music_id'] for x in data['positions']]
    assert not (set(result_ids) - set(expect_ids))
    for d in data['positions']:
        p = f_session.query(Position)\
            .filter(Position.music_id == d['music_id'])\
            .first()
        assert p
        assert p.x == d['x']
        assert p.y == d['y']
