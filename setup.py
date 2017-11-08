# Project installation

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "description": "ALL Project, BSc Business Information Technology",
    "author": "Group 7",
    "url": "https://github.com/leoslf/FSBA",
    "download_url": "__DOWNLOAD_URL__",
    "author_email": "lfsin3-c@my.cityu.edu.hk",
    "version": "0.1",
    "install_requires": ["nose"],
    "packages": ["all_proj2"],
    "scripts": [],
    "name": "FSBA2"
}

setup(**config)
