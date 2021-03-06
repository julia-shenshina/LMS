#!/usr/bin/env python3

"""Setup script."""

from setuptools import setup, find_packages

setup(
    name="lms",
    version="1.0",
    author="Julia Shenshina",
    author_email="shenshina.ju@gmail.com",
    url="https://github.com/julia-shenshina/LMS",
    license="MIT",
    packages=find_packages(exclude=['tests']),
    setup_requires=[
        "django",
        "djangorestframework",
        "django-rest-swagger"
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        "console_scripts": ["lms=lms.manage:manage"]
    }
)