# -*- coding: utf-8 -*-
from tento.music import Artist, Album, Genre, Music


def test_create_artist(f_session):
    name = 'adele'
    artist = Artist(name=name)
    f_session.add(artist)
    f_session.commit()
    artist = f_session.query(Artist)\
            .filter(Artist.name == name)\
            .all()
    assert artist
    assert name == artist[0].name


def test_create_album(f_session):
    name = '21'
    artist_id = 1
    genre_id = 1
    year = 2008
    album = Album(name=name,
                  artist_id=artist_id,
                  genre_id=genre_id,
                  year=year)
    f_session.add(album)
    f_session.commit()
    album = f_session.query(Album)\
            .filter(Album.name == name)\
            .all()
    assert album
    assert name == album[0].name
    assert artist_id == album[0].artist_id
    assert genre_id == album[0].genre_id
    assert year == album[0].year


def test_create_genre(f_session):
    name = 'pop'
    genre = Genre(name=name)
    f_session.add(genre)
    f_session.commit()
    genre = f_session.query(Genre)\
            .filter(Genre.name == name)\
            .all()
    assert genre
    assert name == genre[0].name


def test_create_music(f_session):
    name = 'Someone Like You'
    album_id = 1
    track_number = 1
    disk_number = 1
    music = Music(name=name,
                  album_id=album_id,
                  track_number=track_number,
                  disk_number=disk_number)
    f_session.add(music)
    f_session.commit()
    music = f_session.query(Music)\
            .filter(Music.name == name)\
            .all()
    assert music
    assert name == music[0].name
    assert album_id == music[0].album_id
    assert track_number == music[0].track_number
    assert disk_number == music[0].disk_number
