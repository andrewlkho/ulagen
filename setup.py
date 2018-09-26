#!/usr/bin/python
from setuptools import setup

setup (name = 'ulagen',
	description = 'ULA prefix generator',
	packages = [
            'ulagen',
        ],
        entry_points = {
            'console_scripts': [
                'ulagen=ulagen.ulagen:main'
            ],
        })
