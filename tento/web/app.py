# -*- coding: utf-8 -*-
from flask import Flask

from . import user, login, music


app = Flask(__name__)
app.register_blueprint(user.bp, url_prefix='/users')
app.register_blueprint(login.bp, url_prefix='/login')
app.register_blueprint(music.bp, url_prefix='/musics')
