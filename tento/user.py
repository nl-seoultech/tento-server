# -*- coding: utf-8 -*-
""" :mod:`tento.user` --- 사용자 스키마를 담고있습니다.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from datetime import datetime

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Unicode, DateTime
from bcrypt import hashpw, gensalt


from .db import Base


class User(Base):
    """ 사용자 정보를 담고있는 테이블의 스키마
    """

    __tablename__ = 'users'

    #: 사용자의 고유 인덱스
    id = Column(Integer, primary_key=True)

    #: 사용자의 이메일
    email = Column(Unicode, nullable=False, unique=True)

    #: 사용자의 패스워드
    password = Column(Unicode, nullable=False)

    #: 생성일
    created_at = Column(DateTime, default=datetime.now())

    def __init__(self, email, password, created_at=None):
        """ 사용자의 비밀번호를 평문으로 저장하지않고 해시해서 저장합니다.

        :param str email: 사용자의 이메일
        :param str password: 사용자의 패스워드
        :param str created_at: 생성날짜
        """
        hashed = hashpw(password, gensalt())
        super(User, self).__init__(email=email,
                                   password=hashed,
                                   created_at=created_at)


    def confirm_password(self, password):
        """ 사용자의 비밀번호가 올바른지 확인합니다.

        :param str password: 확인할 사용자의 비밀번호
        :return: 패스워드가 맞는지 틀린지에 대한 여부
        :rtype: bool
        """
        return hashpw(password, self.password) == self.password


    @property
    def name(self):
        """ 이메일의 앞부분을 이름으로 반환합니다.

        .. sourcecode:: python

           >>> User(email='admire9@gmail.com', password='foobar')
           >>> _.name
           'admire9'

        :return: 사용자의 이름
        :rtype: str
        """
        name, domain = self.email.split('@')
        return name
