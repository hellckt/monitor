# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

VERSION = (0, 0, 1)

__version__ = ".".join(map(str, VERSION))
__status__ = "Alpha"
__description__ = "Simple web visit monitor system powered by mitmptoxy"
__author__ = "hellckt"
__email__ = "scottzkt@gmail.com"
__license__ = "MIT License"

try:
    long_description = open('README.md').read()
except:
    long_description = __description__

# TODO: 了解setup的进阶用法
setup(
    name='monitor',
    version=__version__,
    url='https://github.com/hellckt/mitmproxy',
    author=__author__,
    author_email=__email__,
    description=__description__,
    long_description=long_description,
    license=__license__,
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'monitor.app': [
            'templates/*.jinja',
            'templates/auth/*.jinja',
            'templates/ban/*.jinja',
            'templates/flow/*.jinja',
            'static/favicon.ico'
        ],
    },
    zip_safe=False,
    platforms='any',
    entry_points={
        'console_scripts': [
            "mitmmonitor = monitor.main:mitmmonitor"
        ]
    },
    install_requires=[
        'Flask>=0.12',
        'Flask-Bootstrap>=3.3.7.1',
        'Flask-Login>=0.4.0',
        'Flask-SQLAlchemy>=2.2',
        'Flask-WTF>=0.14.2',
        'mitmproxy>=2.0.0'
    ]
)
