from setuptools import setup, find_packages

setup(
    name='slurpit_sdk',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas==2.2.2',
        'requests==2.31.0'
    ],
    author='PkServices',
    author_email='info@slurpit.io',
    description='A robust Python SDK for slurpit',
    keywords='sdk slurpit',
)