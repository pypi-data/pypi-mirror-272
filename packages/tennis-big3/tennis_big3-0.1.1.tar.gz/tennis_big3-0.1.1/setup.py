from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup (
	name="tennis_big3",
	version="0.1.1",
	packages=find_packages(),
	install_requires=[],
	author="Javier Gutiérrez",
	description="Library which shows stats about the Big Three era in Tennis (2000's, 2010's)",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://es.wikipedia.org/wiki/Big_Three_(tenis)"
	)
