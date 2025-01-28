from setuptools import setup, find_packages

setup(
    name='apollo-cli',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'apollo=apollo.main:cli',
        ],
    },
)