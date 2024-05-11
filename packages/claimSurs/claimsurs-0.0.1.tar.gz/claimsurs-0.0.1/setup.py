from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="claimSurs",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    author="Yato_kun",
    description="package test that can print kwargs class with modul",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/user/Yato_uid/",
)
