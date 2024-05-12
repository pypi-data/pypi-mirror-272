from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Automatic setup tool for fresh Ubuntu installs'
LONG_DESCRIPTION = 'A package that automates the setup process for fresh Ubuntu installs. It can install programs, change settings, customize the Desktop Environment, install extensions, and set up those extensions'


# Setting up
setup(
    name="ubuntu-postinstall",
    version=VERSION,
    author="hagyma (Varga Dániel)",
    author_email="vargad0803@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pyside6'],
    keywords=['python', 'ubuntu', 'postinstall', 'extensions', 'dconf', 'gsettings'],
    entry_points={
        'console_scripts': [
            'ubuntu-postinstall=ubuntu_postinstall.main:main'
        ]
    }
)
