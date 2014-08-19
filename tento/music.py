# -*- coding: utf-8 -*-
""" :mod:`tento.music` --- 스키마를 담고있습니다.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Unicode, DateTime

from .db import Base


class Artist(Base):
    """ 가수 정보를 저장하는 스키마
    """
    __tablename__ = 'artists'
    # sphinx domain

    #: :py:class:`Artist` 의 고유키
    id = Column(Integer, primary_key=True)

    #: 가수 이름 정보
    name = Column(Unicode, nullable=False)

    #: 가수에 관한 데이터가 생성된 시각
    created_at = Column(DateTime, default=datetime.now())

    #: relationship 설정
    album_rel = relationship('Album')


class Album(Base):
    """ 앨범 정보를 저장하는 스키마
    """
    __tablename__ = 'albums'

    #: :py:class:'Album' 의 고유키
    id = Column(Integer, primary_key=True)

    #: 앨범 이름
    name = Column(Unicode, nullable=False)

    #: 가수 이름 정보
    artist_id = Column(Integer, ForeignKey('artists.id'), nullable=False)

    #: 앨범 장르 정보(생략 가능)
    genre_id = Column(Integer, ForeignKey('genres.id'))

    #: 앨범이 출시된 연도
    year = Column(Integer)

    #: 생성일
    created_at = Column(DateTime, default=datetime.now())

    #: relationship 설정
    music_rel = relationship('Music')


class Genre(Base):
    """ 음악의 장르 정보를 저장하는 스키마
    """
    __tablename__ = 'genres'

    #: :py:class:'Genre' 의 고유키
    id = Column(Integer, primary_key=True)

    #: 장르 이름
    name = Column(Unicode, nullable=False)

    #: 생성일
    created_at = Column(DateTime, default=datetime.now())

    #: relationship 설정
    album_rel = relationship('Album')


class Music(Base):
    """ 음악의 제목과 가수등의 정보를 저장하는 스키마
    """
    __tablename__ = 'musics'

    #: py:class:'Music' 의 고유키
    id = Column(Integer, primary_key=True)

    #: 음악의 이름
    name = Column(Unicode, nullable=False)

    #: 해당 음악이 수록된 앨범의 고유 아이디(번호, 생략가능)
    album_id = Column(Integer, ForeignKey('albums.id'), nullable=False)

    #: 앨범 트랙 번호(생략가능)
    track_number = Column(Integer)

    #: 앨범 디스크 번호(생략가능)
    disk_number = Column(Integer)

    #: 생성일
    created_at = Column(DateTime, default=datetime.now())
