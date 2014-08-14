#! -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(name='tento',
      version='0.0.1',
      author='Kang Hyojun',
      author_email='admire9@gmail.com',
      packages=find_packages(),
      install_requires=[
          'flask==0.10.1', 'flask-script==2.0.5', 'sqlalchemy==0.9.7',
          'pytest==2.6.0', 'alembic', 'py-bcrypt==0.4', 'arrow',
          'itsdangerous', 'sphinx==1.2.2', 'sphinx_rtd_theme'
      ],
      scripts=['manager.py'])
