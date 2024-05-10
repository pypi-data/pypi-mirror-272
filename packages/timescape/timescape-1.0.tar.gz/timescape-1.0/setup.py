from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = ''.join(f.readlines())

setup(
    name='timescape',
    version='1.0',
    packages=find_packages(),
    description="Placeholder for the timescape name",
    long_description=long_description
)
