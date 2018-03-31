# setuptools installation of GromacsWrapper
# Copyright (c) 2008-2011 Oliver Beckstein <orbeckst@gmail.com>
# Released under the GNU Public License 3 (or higher, your choice)
#
# See the files INSTALL and README for details or visit
# http://sbcb.bioch.ox.ac.uk/oliver/software/GromacsWrapper/
from __future__ import with_statement

from setuptools import setup, find_packages

with open("README.md") as readme:
    long_description = readme.read()

setup(name="PlumedWrapper",
      version="0.1",
      description="A python wrapper around the gromacs tools.",
      long_description=long_description,
      author="Jan Domanski",
      author_email="jandom@gmail.com",
      license="GPLv3",
      url="://github.com/orbeckst/PlumedWrapper",
      download_url="https://github.com/jandom/PlumedWrapper/downloads",
      keywords="science Gromacs Plumed analysis 'molecular dynamics'",
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Operating System :: POSIX',
                   'Operating System :: MacOS :: MacOS X',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering :: Bio-Informatics',
                   'Topic :: Scientific/Engineering :: Chemistry',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                  ],
      packages=find_packages(),
      zip_safe=True,
     )
