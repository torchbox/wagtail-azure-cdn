from setuptools import setup, find_packages


setup(
    name="wagtail-azure-cdn",
    version="0.1a0",
    packages=find_packages(),
    install_requires=[
        'azure-mgmt-cdn'
    ],
)
