#!/usr/bin/env python

import os
from setuptools import setup


with open('requirements.txt') as f:
    required = f.read().splitlines()
print required

setup(name='hmas',
      version='1.0',
      description='Scrapes proxies on hidemyass.com',
      author='Ali Bozorgkhan',
      author_email='alibozorgkhan@gmail.com',
      url='https://github.com/alibozorgkhan/hidemyass-scraper',
      install_requires=required,
      license='The MIT License (MIT)'
     )
