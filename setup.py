from setuptools import setup, find_packages
from os import path

from wagtail_azure_cdn import __version__


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="wagtail-azure-cdn",
    description="Use Azure CDN with Wagtail",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license="MIT",
    include_package_data=True,
    author="Tomasz Knapik",
    author_email="hi@tmkn.org",
    version=__version__,
    packages=find_packages(),
    install_requires=["azure-mgmt-cdn", "wagtail"],
    extras_require={"testing": ["flake8", "black", "isort", "faker"]},
    python_requires=">=3.6",
    url="https://github.com/tm-kn/wagtail-azure-cdn/",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Wagtail",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
    ],
)
