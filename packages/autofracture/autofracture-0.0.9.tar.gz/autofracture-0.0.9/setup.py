#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree
from distutils.core import setup
from setuptools import find_packages

  
NAME = 'autofracture'
DESCRIPTION = 'Support the intelligent fracturing process.'
URL = 'https://github.com/MoonCapture/AutoFracture'
EMAIL = 'mzc1226@126.com'
AUTHOR = 'mzc'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.0.9'

# What packages are required for this module to be executed? # 执行这个模块需要什么包?
REQUIRED = [
    'numpy', 'pandas', 'scikit-learn', 'matplotlib', 'seaborn', 'scipy','autogluon'
]
# What packages are optional? # 什么包是可选的?
EXTRAS = {
    # 'fancy feature': ['django'],
}


# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
here = os.path.abspath(os.path.dirname(__file__))
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


setup(
      name=NAME,  
      version=VERSION,  # 版本号
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type='text/markdown',
      author=AUTHOR,
      author_email=EMAIL,
      python_requires=REQUIRES_PYTHON,
      url=URL,
      install_requires=REQUIRED,
      extras_require=EXTRAS,
      include_package_data=True,
      packages=find_packages(),
      platforms=["all"],
      license='MIT License',
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Software Development :: Libraries'
      ],
      )
