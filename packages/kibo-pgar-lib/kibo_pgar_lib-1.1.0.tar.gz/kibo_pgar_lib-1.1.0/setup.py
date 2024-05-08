"""Used for setting up the package to be published to PyPI"""

from setuptools import setup, find_packages

setup(
    name="kibo_pgar_lib",
    version="1.1.0",
    packages=find_packages(),
    description="KiboPgArpLib modified, documented and converted in python.",
    author="Alessandro Muscio",
    author_email="a.muscio001@unibs.studenti.it",
    url="https://github.com/AlessandroMuscio/kibo_pgar_lib",
)
