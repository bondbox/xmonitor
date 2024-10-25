# coding=utf-8

from setuptools import find_packages
from setuptools import setup

from xmonitor.utils import __author__
from xmonitor.utils import __author_email__
from xmonitor.utils import __description__
from xmonitor.utils import __project__
from xmonitor.utils import __urlbugs__
from xmonitor.utils import __urlcode__
from xmonitor.utils import __urldocs__
from xmonitor.utils import __urlhome__
from xmonitor.utils import __version__


def all_requirements():
    def read_requirements(path: str):
        with open(path, "r", encoding="utf-8") as rhdl:
            return rhdl.read().splitlines()

    requirements = read_requirements("requirements.txt")
    return requirements


setup(
    name=__project__,
    version=__version__,
    description=__description__,
    url=__urlhome__,
    author=__author__,
    author_email=__author_email__,
    project_urls={"Source Code": __urlcode__,
                  "Bug Tracker": __urlbugs__,
                  "Documentation": __urldocs__},
    packages=find_packages(include=["xmonitor*"], exclude=["tests"]),
    install_requires=all_requirements())
