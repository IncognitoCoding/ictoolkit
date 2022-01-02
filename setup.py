from setuptools import setup

VERSION = '0.0.10.20'
DESCRIPTION = 'ictoolkit is designed to be the swiss army knife of programming methods.'
LONG_DESCRIPTION = 'Each method is broken down into a specific type of use case. The methods are currently broad and cover several types of areas.'

# Setting up
setup(
    name="ictoolkit",
    version=VERSION,
    author="ictoolkit",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=[
        'ictoolkit/directors',
        'ictoolkit/helpers'
    ],
    url='https://github.com/IncognitoCoding/ictoolkit.git',
    license='GPL',
    install_requires=[
    ],
    keywords=['python'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    zip_safe=False
)
