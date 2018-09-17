import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mensa",
    version = "0.4.1",
    author = "Antonia Pérez-Cerezo",
    author_email = "antonia@antonia.is",
    description = ("A program that fetches menus from various restaurants. Pre-installed by default are various cafeterias around TU Berlin."),
    license = "MIT",
    keywords = "food",
    url = "https://git.bananach.space/mensa.git",
    packages=['mensa'],
    scripts=['bin/mensa'],
    long_description=read('README'),
    include_package_data=True,
    install_requires=['yapsy','lxml', 'cssselect'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
