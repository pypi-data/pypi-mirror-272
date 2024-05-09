from setuptools import setup, find_packages
from setuptools.command.install import install
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'this packge will help to generate telegram api keys'
LONG_DESCRIPTION = 'A package to creates telegram api keys'



class CustomInstall(install):
    def run(self):
        print(f"Installed APi Module do visit @BeastX_Bots")
        install.run(self)

# Setting up
setup(
    name="pyBeastxAPI",
    version=VERSION,
    author="BeastX",
    author_email="atronpay7@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["lxml","requests","fake_useragent","tqdm"],
    cmdclass={"install": CustomInstall},
    keywords=['tgapihash', 'tgapi', 'telegram api', 'api hash', 'pybeastx'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)