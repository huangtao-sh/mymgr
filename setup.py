#!/usr/bin/python3
from distutils.core import setup
setup(
        name='mymgr',
        version='0.0.1',
        author='Huang tao',
        author_email='huangtao.jh@gmail.com',
        platforms='any',
        description='mysql connection lib',
        long_description='mysql connection lib',
        packages=['mymgr'],
        license='GPL',
        requires=['mysql_connector_python']
        )
