# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup

setup_args = {
    'name': 'simple-web-crawler',
    'version': '0.1.0',
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
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Topic :: Internet :: WWW/HTTP',
    ],
    'install_requires': [
        'Scrapy==1.6',
        'scrapy-splash==0.7.2',
        'pyasn1==0.4.5'
    ],
    'entry_points': {
        'console_scripts': ['simple-web-crawler=simple_web_crawler.run:main']
    },
}

setup(**setup_args)
