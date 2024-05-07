from setuptools import setup, find_packages


with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name="visum-io-sdk",
    version="1.0.4",
    description='Python client for visum.io public API',
    long_description_content_type='text/markdown',
    long_description=long_description,
    license="MIT",
    url="https://demo.visum.io",
    packages=find_packages(),
    install_requires=[
        'requests>2.30'
    ],
)
