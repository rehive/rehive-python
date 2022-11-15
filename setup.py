"""
Rehive SDK for rapid service development.
"""
import os
from codecs import open
# Always prefer setuptools over distutils
from setuptools import find_packages, setup


VERSION = '1.3.0'

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='rehive',
    version=VERSION,
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    include_package_data=True,
    description='Rehive SDK for Python',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/rehive/rehive-python',
    download_url='https://github.com/rehive/rehive-python/archive/{}.zip'.format(VERSION),
    author='Rehive',
    author_email='info@rehive.com',
    license='MIT',
    install_requires=['requests'],
    python_requires='>=3.4',
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
)
