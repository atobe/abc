from setuptools import setup, find_packages

setup(
    name="lats",
    version="0.1",
    description="language agent tree search",
    url="http://github.com/atobe/abc",
    author="Toby Watson",
    author_email="toby@thetobe.com",
    license="",
    packages=["lats"],
    entry_points={"console_scripts": ["lats = lats.__main__:main"]},
    zip_safe=False,
)
