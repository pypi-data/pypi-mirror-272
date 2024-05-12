from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A CG generator for C/C++ project'
LONG_DESCRIPTION = 'A package that allows you to generate CG for C/C++ project'

setup(
    name='CGenr',
    version=VERSION,
    author='Jiang Yuxuan',
    author_email='1594935046@qq.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'tree-sitter>=0.20.2',
        'graphviz',
        'setuptools',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)