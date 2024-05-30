# python setup.py

from setuptools import setup

setup(
    name='news',
    version='0.1',
    packages=['news'],
    install_requires=[
        'dataclasses',
        'openai',
        'instructor',
        'pydantic'
    ],
    entry_points={
        'console_scripts': [
            'agent_news = news.__main__:main',
        ],
    },
)
