from setuptools import setup, find_packages

from wagtail_azure_cdn import __version__


setup(
    name="wagtail-azure-cdn",
    description="Use Azure CDN with Wagtail",
    license="MIT",
    include_package_data=True,
    author="Tomasz Knapik",
    author_email="hi@tmkn.org",
    version="0.1a0",
    packages=find_packages(),
    install_requires=["azure-mgmt-cdn", "wagtail"],
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
