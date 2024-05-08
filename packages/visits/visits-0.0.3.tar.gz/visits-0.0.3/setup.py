#!/usr/bin/env python3

from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='visits',
    version='0.0.3',
    license='MIT',
    author='nggit',
    author_email='contact@anggit.com',
    description=(
        'visits is just an example of a web page to display hits.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/nggit/visits',
    packages=['visits'],
    install_requires=['terbilang', 'tremolo', 'tremolo_session'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
