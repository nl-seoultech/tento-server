#! -*- coding: utf-8 -*-
from setuptools import setup, find_packages


docs_require = [
    'sphinx>=1.2', 'sphinxcontrib-httpdomain', 'sphinx_rtd_theme'
]

test_require = [
    'pytest==2.6.0',
]

setup(name='tento',
      version='0.0.1',
      author='Kang Hyojun',
      author_email='admire9@gmail.com',
      packages=find_packages(),
      install_requires=[
          'flask==0.10.1', 'flask-script==2.0.5', 'sqlalchemy==0.9.7',
          'alembic', 'py-bcrypt==0.4', 'arrow',
          'itsdangerous'
      ] + docs_require,
      tests_require=test_require,
      extras_require={
          'docs': docs_require,
          'tests': test_require
      },
      scripts=['manager.py'])
