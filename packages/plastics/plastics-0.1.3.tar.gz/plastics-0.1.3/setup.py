# -*- coding: utf-8 -*-
# Plastics: Plastic processing models in BioSTEAM
# Copyright (C) 2024, Yoel Cortes-Pena <yoelcortes@gmail.com>
# 
# This module is under the UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
from setuptools import setup

setup(
    name='plastics',
    packages=['plastics'],
    license='MIT',
    version='0.1.3',
    description="Plastic processing models in BioSTEAM",
    long_description=open('README.rst', encoding='utf-8').read(),
    author='Yoel Cortes-Pena',
    install_requires=['biosteam>=2.44.0,<2.45.0'],
    python_requires=">=3.9",
    package_data={
        'plastics': [
            'strap/*',
        ]
    },
    platforms=['Windows', 'Mac', 'Linux'],
    author_email='yoelcortes@gmail.com',
    url='https://github.com/yoelcortes/plastics',
    download_url='https://github.com/yoelcortes/plastics',
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Console',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Scientific/Engineering :: Chemistry',
                 'Topic :: Scientific/Engineering :: Mathematics'],
    keywords='chemical process simulation plastic bioprocess engineering STRAP solvent targeted dissolution precipitation',
)
