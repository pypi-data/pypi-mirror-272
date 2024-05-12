#!/usr/bin/env python3

import re
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

try:
    long_description = (here / "docs/README.md").read_text(encoding="utf-8")
except FileNotFoundError:
    long_description = (here / "README.md").read_text(encoding="utf-8")

with open('sherlock/sherlock.py', 'r') as file:
    sherlockpy = file.read()
version = str(re.findall('__version__ = "(.*)"', sherlockpy)[0])

setup(
    name="sherlock",
    version=version,
    description="Hunt down social media accounts by username",
    long_description=long_description,
    long_description_content_type="test/markdown",
    url="http://sherlock-project.github.io/",
    author="Sherlock Project",
    package_dir={"": "sherlock"},
    package_data={
        "*": ["*.json"]
    },
    project_urls={
        "Homepage": "http://sherlock-project.github.io/",
        "Repository": "https://github.com/sherlock-project/sherlock.git",
        "Issues": "https://github.com/sherlock-project/sherlock/issues"
    }
)