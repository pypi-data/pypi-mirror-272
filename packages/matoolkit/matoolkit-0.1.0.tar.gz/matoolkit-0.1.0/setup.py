from setuptools import setup, find_packages

setup(
    name="matoolkit",
    version="0.1.0",
    packages=find_packages(),
    description="A toolkit for chart creation in matplotlib",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Joseph Barbier",
    author_email="joseph.barbierdarnal@gmail.com",
    url="http://www.barberjoseph.com",
    install_requires=[
        "pandas",
        "highlight_text",
        "matplotlib",
        "pytest",
    ],
)
