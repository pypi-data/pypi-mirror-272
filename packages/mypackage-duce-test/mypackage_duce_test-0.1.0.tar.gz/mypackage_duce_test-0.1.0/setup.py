from setuptools import setup, find_packages

setup(
    name='mypackage_duce_test',
    author='Laurent Wambura',
    version='0.1.0',
    description='This is test Package',
    packages=find_packages(include=['mypackage', 'mypackage.*'])
)
