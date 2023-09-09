# -*- coding: utf-8 -*-
"""Installer for the collective.opentelemetry package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="collective.opentelemetry",
    version="1.0a1",
    description="OpenTelemetry instrumentation for Plone",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="David Glick",
    author_email="david@glicksoftware.com",
    url="https://github.com/collective/collective.opentelemetry",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/collective.opentelemetry",
        "Source": "https://github.com/collective/collective.opentelemetry",
        "Tracker": "https://github.com/collective/collective.opentelemetry/issues",
        # 'Documentation': 'https://collective.opentelemetry.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        "opentelemetry-distro",
        "opentelemetry-exporter-otlp",
        "opentelemetry-instrumentation-wsgi",
        "Plone>=6.0.0",
    ],
    extras_require={
        "profiler": ["pyinstrument"],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [paste.filter_factory]
    wsgi = collective.opentelemetry.middleware:wsgi_middleware_factory
    """,
)
