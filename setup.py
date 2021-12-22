from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in customapi/__init__.py
from customapi import __version__ as version

setup(
	name="customapi",
	version=version,
	description="Custom API",
	author="Nirali Satapara",
	author_email="nirali@ascratech.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
