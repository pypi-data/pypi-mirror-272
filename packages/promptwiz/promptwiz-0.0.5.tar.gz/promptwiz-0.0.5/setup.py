# coding: utf-8


from setuptools import setup  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "promptwiz"
VERSION = "0.0.5"
PYTHON_REQUIRES = ">=3.7"
REQUIRES = [
    "requests",
    "httpx",
]

setup(
    name=NAME,
    version=VERSION,
    description="PromptWiz API",
    author="PromptWiz",
    author_email="contact@promptwiz.co.uk",
    url="",
    keywords=["PromptWiz", "PromptWiz API"],
    install_requires=REQUIRES,
    license="Apache 2.0",
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
)
