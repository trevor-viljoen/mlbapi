#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

from mlbapi import __version__

requirements = [
    'requests',
    'python-dateutil',
    'inflection'
]

setup(
    name='mlbapi',
    version=__version__,
    description='A python3 API wrapper for the MLB API at statsmlb.mlb.com',
    url='https://github.com/trevor-viljoen/mlbapi',
    author='Trevor Viljoen',
    author_email='trevor.viljoen@gmail.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    keywords=[
        'MLB',
        'MLB API',
        'Major League Baseball',
        'baseball',
        'baseball API',
        'baseball data',
        'baseball scores',
        'baseball statistics',
        'baseball stats',
    ],
    platforms='ANY',
    install_requires=requirements,
    python_requires='>=3.6',
    extras_require={
        'dev': ['pytest', 'pytest-cov', 'coveralls']
    }
)
