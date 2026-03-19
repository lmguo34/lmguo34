from setuptools import setup, find_packages

setup(
    name="freeride",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["freeride"],
    entry_points={
        "console_scripts": [
            "freeride=freeride:cli",
        ],
    },
    install_requires=[
        "requests",
    ],
)
