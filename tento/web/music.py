# -*- coding: utf-8 -*-
""" :mod:`tento.web.music` --- tento의 음악 관련 API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import Blueprint, jsonify, request, abort
from sqlalchemy.exc import IntegrityError

from ..db import session
from ..music import Artist, Album, Music, Genre

bp = Blueprint('music', __name__)

@bp.route('/', methods=['POST'])
def create():
    """ 음악 데이터를 받아서 :class:`tento.music.Artist`,
    :class:`tento.music.Album`, :class:`tento.music.Music` 을 생성합니다.

    .. sourcode:: http

       POST /musics/ HTTP/1.1
       Content-Type: application/json
       Accept: application/json
       Host: tento.com

       {
         "music_name": "유감",
         "music_track_number": 1,
         "music_disc_number": 1,
         "artist_name": "leeSA",
         "album_name": "유감",
         "album_release_year": 2010,
         "genre": "팝 > 팝, 팝 > 발라드"
       

    .. sourcode:: http

       HTTP/1.1 /musics/ 201 created
       Content-Type: application/json
    """
    if not request.json:
        abort(400)
    # json으로 데이터를 받아오는 부분
    music_name = request.json.get('music_name', None)
    music_track_number = request.json.get('music_track_number', None)
    music_disc_number = request.json.get('music_disc_number', None)
    artist_name = request.json.get('artist_name', None)
    album_name = request.json.get('album_name', None)
    album_release_year = request.json.get('album_release_year', None)
    genre = request.json.get('genre', None)
    if artist_name is None:
        abort(400)
    # artist, album, genre, music 순으로 데이터 생성
    artist = Artist(name=artist_name)
    session.add(artist)
    album = Album(artist=artist, name=album_name, year=album_release_year)
    session.add(album)
    genre = Genre(name=genre)
    session.add(genre)
    music = Music(album=album, genre=genre, name=music_name,
                  track_number=music_track_number,
                  disc_number=music_disc_number)
    session.add(music)
    # session.commit()으로 데이터를 DB에 생성하고, 예외처리 실행
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        abort(500)
    return '', 201
