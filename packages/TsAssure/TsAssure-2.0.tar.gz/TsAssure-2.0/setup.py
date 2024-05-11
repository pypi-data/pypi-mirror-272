from setuptools import setup, find_packages


setup(
    name="TsAssure",
    version="2.0",
    packages=find_packages(), 
    entry_points={
        "console_scripts": [
            "TsAssure-v1.1 = TsAssure:TsAssure",
        ],
    },
) 