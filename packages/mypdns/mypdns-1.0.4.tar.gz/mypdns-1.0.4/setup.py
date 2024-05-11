"""
A default setup template which will import version and requirement directly
from source files within a project.

Author:
    Spirillen

License:
    https://github.com/mypdns/mypdns/blob/master/LICENSE
"""
from re import compile as comp

import setuptools

from setuptools import find_packages, setup


def _get_requirements():
    """
    This function extract all requirements from requirements.txt.
    """

    with open("requirements.txt") as file:
        requirements = file.read().splitlines()

    return requirements


def get_long_description():  # pragma: no cover
    """
    This function return the long description.
    """

    return open("README.md", encoding="utf-8").read()


if __name__ == "__main__":
    # setuptools.
    setup(
        name="mypdns",
        version="1.0.4",
        author="spirillen",
        author_email="pdns@protonmail.com",
        description="My Privacy DNS's Name space reservation",
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        url="https://mypdns.org/",
        project_urls={
            'Tracker': 'https://github.com/mypdns/mypdns/issues',
            'Source': 'https://github.com/mypdns/mypdns',
        },
        packages=find_packages(
            exclude=("*.tests", "*.tests.*", "tests.*", "tests")),
        include_package_data=True,
        classifiers=[
            "Environment :: Console",
            "Development Status :: 7 - Inactive",
            "Intended Audience :: Developers",
            "Intended Audience :: End Users/Desktop",
            "Intended Audience :: Information Technology",
            "Intended Audience :: System Administrators",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3.13",
            "License :: OSI Approved",
            "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3.11",
        ],
        keywords=[
            "dns",
            "domain",
            "Blacklists",
            "Blocklists",
        ],
        python_requires='>=3.10.0, <4',
    )
