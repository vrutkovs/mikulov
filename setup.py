#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession

with open('README.md') as readme_file:
    readme = readme_file.read()

pip_session = PipSession()
parsed_reqs = parse_requirements('requirements.txt', session=pip_session)
parsed_reqs_dev = parse_requirements('requirements_dev.txt', session=pip_session)
requirements = [str(x.req) for x in parsed_reqs]
test_requirements = [str(x.req) for x in parsed_reqs_dev]

setup(
    name='mikulov',
    version='0.1.0',
    description="Mikulov is a minimalistic file-based self-hosted anonymous publishing platform",
    long_description=readme,
    author="Vadim Rutkovsky",
    author_email='vrutkovs@redhat.com',
    url='https://github.com/vrutkovs/mikulov',
    packages=['mikulov'],
    package_dir={'mikulov': 'mikulov'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='mikulov',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
