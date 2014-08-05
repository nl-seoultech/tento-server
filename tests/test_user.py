# -*- coding: utf-8 -*-
from tento.user import User


def test_create_user(f_session):
    """ `tento.db.Base`를 상속받은 `tento.user.User`가 실제로 생성되는지
    확인합니다.
    """
    email = 'admire9@gmail.com'
    password = 'helloworld'
    user = User(email=email, password=password)
    f_session.add(user)
    f_session.commit()
    user = f_session.query(User)\
           .filter(User.email == email)\
           .all()
    assert user
    assert email == user[0].email
    # password는 해쉬해서 저장해야하므로 같으면안됩니다
    assert password != user[0].password


def test_cannot_create_duplicate_user(f_user, f_session):
    """ `tento.user.User`는 `email`이 같은 사용자가 추가되면안됩니다.
    `f_user`는 `tests.conftest` 에 정의되어있습니다.
    """
    pass


def test_confirm_user_password(f_user, f_session):
    """ `tento.user.User`는 패스워드를 확인할수있는 메소드를 구현해야합니다.
    """
    pass


def test_get_user_name(f_user):
    """ `tento.user.User`는 사용자의 이메일로부터 이름을 가져오는 프로퍼티를
    구현해야합니다.

    property는 이런식으로 사용할수있습니다.

    .. sourcecode::python

       class User(Base):

           ...

           @property
           def name(self):
               ...
    """
    pass
