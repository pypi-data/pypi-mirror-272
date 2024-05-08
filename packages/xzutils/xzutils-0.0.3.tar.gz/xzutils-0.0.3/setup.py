from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Sean Python package'
LONG_DESCRIPTION = 'Sean Python package'

# Setting up
# packages=find_packages(),
setup(
       # the name must match the folder name 'verysimplemodule'
        name="xzutils", 
        version=VERSION,
        author="Sean",
        author_email="<xz.sean.g@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=['utils'],
        
)