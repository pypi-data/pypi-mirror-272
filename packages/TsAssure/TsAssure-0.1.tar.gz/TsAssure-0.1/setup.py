# setup.py
from setuptools import setup, find_packages

setup(
    name='TsAssure',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        # Add any additional dependencies here
    ],
    entry_points={
        'console_scripts': [
            'extract-features=TsAssure.cli:main',
        ],
    },
)