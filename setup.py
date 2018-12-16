#!/usr/bin/env python3

"""Setup script."""

from setuptools import setup

setup(
    name="lms",
    version="0.0.1",
    author="Julia Shenshina",
    author_email="shenshina.ju@gmail.com",
    url="https://github.com/julia-shenshina/LMS",
    license="MIT",
    packages=[
        "lms",
    ],
    setup_requires=[
        "pytest-runner",
        "pytest-pylint",
        "pytest-pycodestyle",
        "pytest-pep257",
        "pytest-cov",
    ],
    tests_require=[
        "pytest",
        "pylint",
        "pycodestyle",
        "pep257",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    # entry_points={
    #     "console_scripts": ["lms=lms.lms:main"]
    # }
)