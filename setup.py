#!/usr/bin/env python
"""
sentry-opsgenie
============

An extension for `OpsGenie <https://www.opsgenie.com>`_ which creates OpsGenie alerts.

:copyright: (c) 2015 by Sentry Team, see AUTHORS for more details.
:license: Apache 2.0, see LICENSE for more details.
"""
from setuptools import setup, find_packages


install_requires = [
    'sentry>=5.0.0',
]

setup(
    name='sentry-opsgenie',
    version='0.1.0',
    author='David Cramer',
    author_email='dcramer@gmail.com',
    url='https://github.com/getsentry/sentry-opsgenie',
    description='A Sentry extension which posts notifications to OpsGenie (https://www.opsgenie.com/).',
    long_description=open('README.rst').read(),
    license='Apache 2.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'sentry_opsgenie = sentry_opsgenie',
        ],
        'sentry.plugins': [
            'sentry_opsgenie = sentry_opsgenie.plugin:OpsGeniePlugin',
        ]
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
