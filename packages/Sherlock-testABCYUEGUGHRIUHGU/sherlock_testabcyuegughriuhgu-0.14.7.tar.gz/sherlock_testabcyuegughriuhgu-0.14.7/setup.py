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

setup()