#!/usr/bin/env python

import os

from setuptools import setup

title = "byted-jarvis"
version = os.getenv("VERSION")

setup(
    name=title,
    version=version,
    long_description_content_type="text/markdown",
    author='test',
    # packages=["requests"],
    package_data={"": ["LICENSE", "NOTICE"]},
    package_dir={"byted-jarvis": "byted-jarvis"},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=["requests"],
    setup_requires=["requests"],
    license="MIT",
    zip_safe=False,
    classifiers=[
    ],
)