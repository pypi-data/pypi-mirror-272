from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.0.1'
DESCRIPTION = 'Convert binary <- -> decimal'
LONG_DESCRIPTION = """
Usage:
from bin2dec import Bin2Dec, Dec2Bin

print(Bin2Dec(1010)) # output is 10
print(Dec2Bin(10)) # output is 1010
"""

setup(
    name="bin2dec",
    version=VERSION,
    author="Deveclipse",
    author_email="Kokonin.1@seznam.cz",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    install_requires=[],
    packages=find_packages(),
    keywords=['binary','decimal','binary to decimal', 'bin2dec', 'dec2bin', 'decimal to binary'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)