# -*- coding: utf-8 -*-

import sys

from setuptools import setup
from os.path import join, dirname

with open(join(dirname(__file__), 'simple_web_crawler/VERSION')) as f:
    version = f.read().strip()

setup_args = {
    'name': 'simple-web-crawler',
    'version': version,
    'url': 'https://github.com/mescanef/simple-web-crawler',
    'description': 'A simple Web Crawler',
    'author': 'Mateusz Matuszkowiak',
    'maintainer': 'Mateusz Matuszkowiak',
    'maintainer_email': 'mateusz.matuszkowiak@gmail.com',
    'license': 'MIT',
    'packages': ['simple_web_crawler'],
    'include_package_data': True,
    'classifiers': [
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Topic :: Internet :: WWW/HTTP',
    ],
    'install_requires': [
        'Scrapy==1.6',
        'pyasn1==0.4.5'
    ],
    'entry_points': {
        'console_scripts': ['simple-web-crawler=simple_web_crawler.run:main']
    },
}

setup(**setup_args)