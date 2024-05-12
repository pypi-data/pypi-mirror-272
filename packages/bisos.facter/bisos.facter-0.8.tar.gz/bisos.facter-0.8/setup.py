#!/usr/bin/env python

import setuptools
# import sys

import pypandoc


def readme():
    with open('TITLE.txt') as f:
        return f.readline().rstrip('\n')


def longDescriptionOld():
    with open('README.rst') as f:
        return f.read()

def longDescription():
    return pypandoc.convert_file('README.org', 'rst')



# from setuphelpers import get_version, require_python
# from setuptools import setup

# __version__ = get_version('unisos/icm/__init__.py')
__version__ = '0.8'


requires = [
    "bisos",
    "blee",
    "blee.csPlayer",
    "bisos.transit",   # is used in bisos.b
    "bisos.b",
    "bisos.banna",
    "bisos.common",
]


# print('Setting up under python version %s' % sys.version)
# print('Requirements: %s' % ','.join(requires))

scripts = [
    "./bin/facter.cs",
    "./bin/roInv-facter.cs",
    "./bin/roPerf-facter.cs",
]


setuptools.setup(
    name='bisos.facter',
    version=__version__,
    # namespace_packages=['bisos'],
    packages=setuptools.find_packages(),
    scripts=scripts,
    requires=requires,
    include_package_data=True,
    zip_safe=False,
    author='Mohsen Banan',
    author_email='libre@mohsen.1.banan.byname.net',
    maintainer='Mohsen Banan',
    maintainer_email='libre@mohsen.1.banan.byname.net',
    url='http://www.by-star.net/PLPC/180047',
    license='AGPL',
    description=readme(),
    long_description=longDescription(),
    download_url='http://www.by-star.net/PLPC/180047',
    install_requires=requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
