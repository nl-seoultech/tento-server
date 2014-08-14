# -*- coding: utf-8 -*-
from tento.web.app import app


app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'testing secret_key'
