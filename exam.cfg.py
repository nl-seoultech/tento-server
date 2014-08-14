"""
설정 예시파일입니다. 가급적이면 직접사용하시지마시고 복사하시고 각자 설정해서 사용해주세요. *.cfg.py는 버전관리에서 제외됩니다.
"""

DEBUG = True

DATABASE_URL = "sqlite:///tento_test.db"

# 각자의 migrations 디렉토리의 경로를 넣어주세요.
ALEMBIC_SCRIPT_LOCATION = '/Users/admire/src/tento-server/tento/migrations/'


"""
쉘에 다음과같이 실행해서 충분히 복잡한 비밀키를 얻을수있습니다.

    $ python -c "import os;print(os.urandom(32).encode('base64'))"
    Fd+zVocBpai7+EunMzSdPU7zxNToE0zIySWWYhN5vZ8=

복사해서 사용하시면됩니다.
""""
SECRET_KEY = 'your secret key'
