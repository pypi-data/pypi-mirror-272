# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
from DrissionPage import __version__

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="DrissionPagePlus",
    version=__version__,
    author="xx299x",
    author_email="xx299x@gmail.com",
    description="Add some functions to DrissionPage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD",
    keywords="DrissionPage",
    url="https://gitee.com/xx299x/DrissionPagePlus",
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'lxml',
        'requests',
        'cssselect',
        'DownloadKit>=2.0.0',
        'websocket-client',
        'click',
        'tldextract',
        'psutil'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'dp = DrissionPage._functions.cli:main',
        ],
    },
)
