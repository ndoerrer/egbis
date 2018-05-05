#!/usr/bin/python

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "egbis",
    version = "1.0",
    author = "Nils Doerrer",
    author_email = "nils.doerrer@stud.uni-goettingen.de",
    description = ("A library for efficient graph based data segmentation"+
					"using the Felzenzwalb-Huttenlocher algorithm"),
    license = "BSD",		#??
    keywords = "segmentation, graph-based, ",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['egbislib'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2.7",
    ],
)


