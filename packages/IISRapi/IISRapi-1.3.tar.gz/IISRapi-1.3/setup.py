from setuptools import setup, find_packages
from pathlib import Path

def readmd():
    with open(Path("readme.md"), "r", encoding="utf-8") as f:
        return f.read()
    
with open("requirement.txt", "r") as f:
    requirements = f.read().splitlines()
    
setup(
    name='IISRapi',
    version='1.3',
    packages=find_packages(),
    license='MIT',
    long_description=readmd(),
    long_description_content_type='text/markdown',
    install_requires=requirements,
)