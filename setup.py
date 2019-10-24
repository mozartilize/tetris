import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="tetris",
    version="0.0.4",
    author="mozartilize",
    author_email="mozartilize@gmail.com",
    description=("Simple tetris game"),
    license="BSD",
    keywords="tetris pygame",
    url="https://github.com/mozartilize/tetris",
    packages=['tetris'],
    install_requires=["pygame>=2.0.0.dev4"],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Game",
        "License :: OSI Approved :: BSD License",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    entry_points={
        'console_scripts': [
            'tetris = tetris.main:main'
        ]
    },
)
