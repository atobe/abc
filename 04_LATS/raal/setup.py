from setuptools import setup, find_packages

setup(
    name="raal",
    version="0.1",
    description="react as a library",
    url="http://github.com/atobe/abc",
    author="Toby Watson",
    author_email="toby@thetobe.com",
    license="",
    packages=['raal'],
    entry_points={"console_scripts": ["raal = raal.__main__:main"]},
    zip_safe=False,
)
