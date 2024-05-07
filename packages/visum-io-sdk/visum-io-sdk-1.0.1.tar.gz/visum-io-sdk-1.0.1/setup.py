from setuptools import setup, find_packages


setup(
    name="visum-io-sdk",
    version="1.0.1",
    description='Python client for visum.io public API',
    license="MIT",
    url="https://demo.visum.io",
    packages=find_packages(),
    install_requires=[
        'requests>2.30'
    ],
)
