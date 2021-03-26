from setuptools import setup

VERSION = '0.0.11' 
DESCRIPTION = 'ictools is designed to be the swiss army knife of programming methods.'
LONG_DESCRIPTION = 'Each method is broken down into a specific type of use case. The methods are currently broad and cover several types of areas.'

# Setting up
setup(

        name="ictools", 
        version=VERSION,
        author="ictools",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=['ictools/directors'],
        url='https://github.com/IncognitoCoding/ictools.git',
        license='GPL',
        install_requires=[
            'cryptography>=3.4.6'
        ], 
        keywords=['python'],
        classifiers= [
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],
        zip_safe=False

)