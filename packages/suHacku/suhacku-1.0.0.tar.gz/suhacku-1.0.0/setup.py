from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="suHacku",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    author="Yato_kun",
    description="a little package that can print diferent curses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io/",
)

