from setuptools import setup, find_packages

setup(
    name="balokBeton",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "shapely>=2.0.4",
        "matplotlib>=3.8",
        "sympy>=1.12"
    ]

)