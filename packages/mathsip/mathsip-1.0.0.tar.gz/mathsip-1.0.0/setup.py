from setuptools import setup, find_packages
from mathsip_turkmenogluc import __version__

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

NAME = 'mathsip'
VERSION = __version__
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'
URL = 'https://github.com/cml/mathsip'
AUTHOR = 'Cumali Turkmenoglu'
DESCRIPTION = "A very basic Math library."
AUTHOR_EMAIL = 'turkmenogluc@gmail.com'
LICENSE = 'Apache Software License'
KEYWORDS = 'Maths,tensorflow,machine learning,deep learning'


setup(
    name=NAME,
    version=VERSION,
    description = DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    packages = find_packages(),
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    install_requires =[ "matplotlib",
                        "numpy",
                        "pandas"],
    keywords=KEYWORDS,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
