# -*- coding: utf-8 -*-
from tento.music import Artist, Album, Genre, Music


def test_create_artist(f_session):
    name = 'Adele'
    artist = Artist(name=name)
    f_session.add(artist)
    f_session.commit()
    artist = f_session.query(Artist)\
            .filter(Artist.name == name)\
            .all()
    assert artist
    assert artist[0].created_at
    assert name == artist[0].name


def test_create_album(f_session, f_artist):
    name = '21'
    year = 2008
    album = Album(name=name,
                  artist_id=f_artist.id,
                  year=year)
    f_session.add(album)
    f_session.commit()
    album = f_session.query(Album)\
            .join(Album.artist)\
            .filter(Album.name == name)\
            .first()
    assert album
    assert album.created_at
    assert name == album.name
    assert f_artist.id == album.artist_id
    assert year == album.year
    assert f_artist.id == album.artist.id
    assert f_artist.name == album.artist.name
    assert f_artist.created_at == album.artist.created_at


def test_create_genre(f_session):
    name = 'pop'
    genre = Genre(name=name)
    f_session.add(genre)
    f_session.commit()
    genre = f_session.query(Genre)\
            .filter(Genre.name == name)\
            .all()
    assert genre
    assert genre[0].created_at
    assert name == genre[0].name


def test_create_music(f_session, f_album, f_genre):
    name = 'Someone Like You'
    track_number = 1
    disk_number = 1
    music = Music(name=name,
                  album=f_album,
                  genre=f_genre,
                  track_number=track_number,
                  disk_number=disk_number)
    f_session.add(music)
    f_session.commit()
    music = f_session.query(Music)\
            .filter(Music.name == name)\
            .first()
    assert music
    assert music.created_at
    assert name == music.name
    assert f_album.id == music.album_id
    assert track_number == music.track_number
    assert disk_number == music.disk_number
    assert f_album.id == music.album.id
    assert f_album.name == music.album.name
    assert f_genre.name == music.genre.name
