""" :mod:`tento.web.music` --- tento의 음악 관련 API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import Blueprint, request, abort
from sqlalchemy.exc import IntegrityError

from ..db import session
from ..music import Artist, Album, Music, Genre, Position
from .util import jsonable, jsonify

bp = Blueprint('music', __name__)


@jsonable.register(Position)
def _(arg):
    return {
        'x': arg.x,
        'y': arg.y,
        'music_id': arg.music_id
    }


@bp.route('/', methods=['POST'])
def create():
    """ 음악 데이터를 받아서 :class:`tento.music.Artist`,
    :class:`tento.music.Album`, :class:`tento.music.Music` 을 생성합니다.

    .. sourcecode:: http

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


    .. sourcecode:: http

       HTTP/1.1 201 created
       Content-Type: application/json

    :return: 생성된 :py:class:`tento.music.Artist` , :class:`tento.music.Album` ,
             :py:class:`tento.music.Music` 를 json으로 반환.
    :statuscode 201: 데이터가 정상적으로 생성됬음.
    :statuscode 400: 필요한 데이터가 비어있음.
    :statuscode 500: 서버 에러발생
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
    if artist_name is None or music_name is None or album_name is None:
        abort(400)
    # artist, album, genre, music 순으로 데이터 생성
    artist = Artist(name=artist_name)
    session.add(artist)
    album = Album(artist=artist, name=album_name, year=album_release_year)
    session.add(album)
    g = None
    if genre is not None:
        g = Genre(name=genre)
        session.add(g)
    music = Music(album=album, name=music_name,
                  track_number=music_track_number,
                  disc_number=music_disc_number)
    if g is not None:
        music.genre = g
    session.add(music)
    # session.commit()으로 데이터를 DB에 생성하고, 예외처리 실행
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        abort(500)
    return jsonify(), 201


@bp.route('/<int:id_>/positions/', methods=['POST'])
def position(id_):
    """ 음악 데이터를 받아서 :class:`tento.music.Position`을 생성합니다.

    .. sourcecode:: http

        POST /musics/:id/position/
        Content-Type: application/json
        Accept: application/json
        Host: tento.com

        {
            "x": 10,
            "y": 9,
            "music_id": 1
        }

    ..sourcecode:: http
        HTTP/1.1 201 created
        Content-Type: application/json

    :param id_: :class:`tento.music.Music` 의 :attr:`tento.music.Music.id`
    :return: 생성된 :py:class:`tento.music.Position`을 json으로 반환
    :statuscode 201: 데이터가 정상적으로 생성되었음.
    :statuscode 400: 필요한 데이터가 비어있음.
    :statuscode 500: 서버 에러 발생.
    """
    if not request.json:
        abort(400)
    # json으로 데이터를 받아오는 부분
    x = request.json.get('x', None)
    y = request.json.get('y', None)
    if x is None or y is None:
        abort(400)
    music = session.query(Music)\
            .filter(Music.id == id_)\
            .first()
    if not music:
        abort(404)
    # position 을 생성
    position = Position(x=x, y=y, music_id=music.id)
    session.add(position)
    # session.commit()으로 데이터를 DB에 생성하고, 예외처리 실행
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        abort(500)
    return jsonify(position), 201


@bp.route('/<int:id_>/positions/', methods=['GET'])
def find_position(id_):
    """ :param id_: 에 해당하는 :class:`tento.music.Position`을 조회합니다.

    .. sourcecode:: http

        GET /musics/:id/position/
        Accept: application/json
        Host: tento.com

    ..sourcecode:: http
        HTTP/1.1 201 created
        Content-Type: application/json

        {
            "x": 0,
            "y": 0,
            "music_id": :id
        }

    :param id_: :class:`tento.music.Music` 의 :attr:`tento.music.Music.id`
    :return: 조회한 :py:class:`tento.music.Position`을 json으로 반환
    :statuscode 200: 데이터가 정상적으로 조회되었음.
    :statuscode 404: :param id_: 에 해당하는 :class:`tento.music.Position`
                     데이터가 존재하지않음.
    :statuscode 500: 서버 에러 발생.
    """
    position = session.query(Position)\
               .join(Position.music)\
               .filter(Music.id == id_)\
               .first()
    if not position:
        abort(404)
    return jsonify(position)


@bp.route('/positions/', methods=['GET'])
def find_all_positions():
    """ 모든 :class:`tento.music.Position`을 조회합니다.

    .. sourcecode:: http

        GET /musics/positions/?music_ids=1,2,3,4
        Accept: application/json
        Host: tento.com

    ..sourcecode:: http
        HTTP/1.1 201 created
        Content-Type: application/json
        {
            "positions": [
                {
                    "x": 0,
                    "y": 0,
                    "music_id": 1
                },
                ...
            ]
        }

    :query string music_ids: :attr:`tento.music.Music.id` 를 , 로 이어 붙인것.
    :return: 조회한 :py:class:`tento.music.Position`을 json으로 반환
    :statuscode 200: 데이터가 정상적으로 조회되었음.
    :statuscode 400: 쿼리스트링에 이상한 문자열이 들어왔을때,
                     music_ids가 없을때
    :statuscode 500: 서버 에러 발생.
    """
    music_ids = request.args.get('music_ids', None)
    if music_ids is None:
        abort(400)
    music_ids = music_ids.split(',')
    try:
        music_ids = [int(x.strip()) for x in music_ids if x]
    except ValueError as e:
        abort(400)
    positions = session.query(Position)\
                .join(Position.music)\
                .filter(Music.id.in_(music_ids))\
                .all()
    return jsonify(positions=positions)
