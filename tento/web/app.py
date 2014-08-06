# -*- coding: utf-8 -*-
from flask import Flask

from . import user


app =  Flask(__name__)
app.register_blueprint(user.bp, url_prefix='/users/')


if __name__ == '__main__':
    app.run(port=5000)
