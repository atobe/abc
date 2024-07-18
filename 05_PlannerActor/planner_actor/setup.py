from setuptools import setup

setup(
    name="planner_actor",
    version="0.1",
    description="planner actor",
    url="http://github.com/atobe/abc",
    author="Toby Watson",
    author_email="toby@thetobe.com",
    license="",
    packages=["planner_actor"],
    entry_points={"console_scripts": ["planner_actor = planner_actor.__main__:main"]},
    zip_safe=False,
)
