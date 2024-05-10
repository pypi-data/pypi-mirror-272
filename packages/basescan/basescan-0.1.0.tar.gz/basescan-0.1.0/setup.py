from setuptools import setup

setup(
    name='basescan',
    version='0.1.0',
    packages=["basescan"],
    long_description="""BaseScan API Wrapper for Python.
    BaseScan is a block explorer of the Base Chain. This API Wrapper is a Python implementation of the BaseScan API.
    """,
    long_description_content_type='text/markdown',
    author='fswair',
    author_email="kodlarintercumani@gmail.com",
    maintainer='basefly',
    maintainer_email="baseflyfinance@gmail.com",
    install_requires=[
        'requests'
    ],
    zip_safe=False,
    python_requires='>=3.9',
    url="https://github.com/Basefly/BaseScan"

)

