# python setup.py

from setuptools import setup

setup(
    name='news',
    version='0.1',
    packages=['ytprecis'],
    install_requires=[
        'dataclasses',
        'openai',
        'instructor',
        'pydantic',
        'requests',
        'youtube_transcript_api'
    ],
    entry_points={
        'console_scripts': [
            'ytprecis = ytprecis.__main__:main',
        ],
    },
)
