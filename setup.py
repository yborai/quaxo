#!/usr/bin/env python

"""
quaxo
"""

import os

import quaxo


def relative_path(path):
    """
    Return the given path relative to this file.
    """
    return os.path.join(os.path.dirname(__file__), path)


def autosetup():
    from setuptools import setup, find_packages

    with open(relative_path('requirements.txt'), 'rU') as f:
        requirements_txt = f.read().split("\n")

    return setup(
        name="quaxo",
        version="0.0.1",
        include_package_data=True,
        zip_safe=False,
        packages=find_packages(exclude=[]),
        install_requires=requirements_txt,
        entry_points = {
            'console_scripts': [
                'quaxo = quaxo.__main__:main',
            ]
        }
    )

if(__name__ == '__main__'):
    dist = autosetup()
