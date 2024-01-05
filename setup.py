# coding=utf-8

from setuptools import find_packages
from setuptools import setup

from xmonitor.utils import __author__
from xmonitor.utils import __author_email__
from xmonitor.utils import __description__
from xmonitor.utils import __name__
from xmonitor.utils import __url_bugs__
from xmonitor.utils import __url_code__
from xmonitor.utils import __url_docs__
from xmonitor.utils import __url_home__
from xmonitor.utils import __version__

setup(
    name=__name__,
    version=__version__,
    description=__description__,
    url=__url_home__,
    author=__author__,
    author_email=__author_email__,
    project_urls={"Source Code": __url_code__,
                  "Bug Tracker": __url_bugs__,
                  "Documentation": __url_docs__},
    packages=find_packages(include=["xmanual*"], exclude=["tests"]))
