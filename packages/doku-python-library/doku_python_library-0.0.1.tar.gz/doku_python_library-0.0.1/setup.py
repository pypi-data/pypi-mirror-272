from setuptools import setup, find_packages

setup(
    name="doku_python_library",
    version="0.0.1",
    description="DOKU python library for Payment Integration",
    packages=find_packages(),
    classifiers= [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)