# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='mydatepackage',
    version='0.1.0',
    packages=find_packages(),
    description='A simple date utility package',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    license='MIT',
    install_requires=[
        'python-dateutil>=2.8.1'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)