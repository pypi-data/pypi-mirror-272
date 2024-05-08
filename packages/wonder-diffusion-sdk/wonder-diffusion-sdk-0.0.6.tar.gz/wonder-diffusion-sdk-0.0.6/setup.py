from setuptools import setup, find_packages

setup(
    name='wonder-diffusion-sdk',
    version='0.0.6',
    description='Python SDK for common Wonder diffusion models',
    long_description='Version 0.0.6 requires a crucial update in WonderModelConfig initialization',
    author='basri',
    author_email='basri@wonder.co',
    packages=find_packages(),
    install_requires=[
      'diffusers==0.26.3'
    ],
)