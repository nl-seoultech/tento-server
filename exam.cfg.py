"""
설정 예시파일입니다. 가급적이면 직접사용하시지마시고 복사하시고 각자 설정해서 사용해주세요. *.cfg.py는 버전관리에서 제외됩니다. 
"""

DEBUG = True

DATABASE_URL = "sqlite:///tento_test.db"

# 각자의 migrations 디렉토리의 경로를 넣어주세요.
ALEMBIC_SCRIPT_LOCATION = '/Users/admire/src/tento-server/tento/migrations/'
