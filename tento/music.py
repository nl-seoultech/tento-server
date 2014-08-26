# -*- coding: utf-8 -*-
""" :mod:`tento.music` --- 스키마를 담고있습니다.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Unicode, DateTime, Float

from .db import Base


class Artist(Base):
    """ 가수 정보를 저장하는 스키마
    """
    __tablename__ = 'artists'

    #: :py:class:`Artist` 의 고유키
    id = Column(Integer, primary_key=True)

    #: 가수 이름 정보
    name = Column(Unicode, nullable=False)

    #: 가수에 관한 데이터가 생성된 시각
    created_at = Column(DateTime, default=datetime.now())

    #: 이 가수에 속한 :py:class:`Album` 들
    albums = relationship('Album', backref='artist')


class Album(Base):
    """ 앨범 정보를 저장하는 스키마
    """
    __tablename__ = 'albums'

    #: :py:class:`Album` 의 고유키
    id = Column(Integer, primary_key=True)

    #: 앨범 이름
    name = Column(Unicode, nullable=False)

    #: 가수 이름 정보
    artist_id = Column(Integer, ForeignKey('artists.id'), nullable=False)

    #: 앨범이 출시된 연도
    year = Column(Integer)

    #: 생성일
    created_at = Column(DateTime, default=datetime.now())

    #: 이 앨범에 속한 :py:class:`Music` 들
    musics = relationship('Music', backref='album')


class Genre(Base):
    """ 음악의 장르 정보를 저장하는 스키마
    """
    __tablename__ = 'genres'

    #: :py:class:`Genre` 의 고유키
    id = Column(Integer, primary_key=True)

    #: 장르 이름
    name = Column(Unicode, nullable=False)

    #: 생성일
    created_at = Column(DateTime, default=datetime.now())


class Music(Base):
    """ 음악의 제목과 가수등의 정보를 저장하는 스키마
    """
    __tablename__ = 'musics'

    #: :py:class:`Music` 의 고유키
    id = Column(Integer, primary_key=True)

    #: 음악의 이름
    name = Column(Unicode, nullable=False)

    #: 해당 음악이 수록된 앨범의 고유 아이디(번호, 생략가능)
    album_id = Column(Integer, ForeignKey('albums.id'), nullable=False)

    #: 앨범 트랙 번호(생략가능)
    track_number = Column(Integer)

    #: 앨범 디스크 번호(생략가능)
    disc_number = Column(Integer)

    #: 장르 정보(생략 가능)
    genre_id = Column(Integer, ForeignKey('genres.id'))

    #: 노래의 장르
    genre = relationship('Genre')

    position = relationship('Position')

    #: 생성일
    created_at = Column(DateTime, default=datetime.now())

class Position(Base):
    """ 음악 분위기 데이터의 :attr:`x`, `y`, `music_id` 정보를 저장하는 스키마
    """
    __tablename__ = 'positions'

    #: :py:class:`Position` 의 고유키
    id = Column(Integer, primary_key=True)

    #: 분위기의 x 좌표(가사에 의한 분위기)
    x = Column(Float, nullable=False, default=0)

    #: 분위기의 y 좌표(BPM에 의한 분위기)
    y = Column(Float, nullable=False, default=0)

    #: :class:`tento.Music.music_id` 를 가리키는 외래키
    music_id = Column(Integer, ForeignKey('musics.id'), nullable=False)
