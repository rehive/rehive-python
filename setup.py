"""
Rehive SDK for rapid service development
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rehive',
    version=open('VERSION').read().strip(),
    description='Rehive SDK for Python',
    long_description=long_description,
    url='https://github.com/rehive/rehive-python',
    author='Rehive',
    author_email='info@rehive.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='rehive api sdk development',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['requests']
)
