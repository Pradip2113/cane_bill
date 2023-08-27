from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in cane_bill/__init__.py
from cane_bill import __version__ as version

setup(
	name="cane_bill",
	version=version,
	description="cane_bill",
	author="quantbit",
	author_email="21pradipjadhav@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
