from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="crawler",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,

    install_requires=['httplib2', 'bs4'],

    author="renchen@",
    author_email="cookum0420@gmail.com",
    license="MIT",
)