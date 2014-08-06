# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Unicode, DateTime
from bcrypt import hashpw, gensalt


from .db import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    email = Column(Unicode, nullable=False, unique=True)

    password = Column(Unicode, nullable=False)

    created_at = Column(DateTime, default=datetime.now())

    def __init__(self, email, password, created_at=None):
        hashed = hashpw(password, gensalt())
        super(User, self).__init__(email=email, password=hashed, created_at=created_at)


    def confirm_password(self, password):
        return hashpw(password, self.password) == self.password