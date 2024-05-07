from setuptools import setup, find_packages

setup(
    name='data-quality-validation-pydeequ',
    version='0.3',
    author='Ketan Kirange',
    author_email='k.kirange@reply.com',
    description='A library for data quality validation using PyDeequ.',
    long_description='A Python library that provides classes for performing data quality validation using Pydeequ.',
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'pydeequ',
        'boto3',
        'pyyaml',  
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    keywords='data quality validation pydeequ',
)
