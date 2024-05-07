from setuptools import setup, find_packages

VERSION = '0.1.1' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'A simple Python package that provides basic math operations.'

setup(
    name="brianpackage", 
    version=VERSION,
    author="Brian",
    author_email="brian@nexa4ai.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[], 
    
    keywords=['python', 'math', 'basic operations'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)