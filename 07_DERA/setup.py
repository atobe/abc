from setuptools import setup

setup(
    name="dera",
    version="0.1",
    description="New!",
    url="http://github.com/atobe/dera",
    author="Toby Watson",
    author_email="toby@thetobe.com",
    license="Private",
    packages=["dera"],
    entry_points={"console_scripts": ["dera = dera.__main__:main"]},
    zip_safe=False,
)
