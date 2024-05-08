from setuptools import setup, find_packages

setup(
    name="ctsf",
    description="Certificate Transparency Subdomain Finder",
    long_description="Certificate Transparency Subdomain Finder",
    author="Erfan Samandarian",
    author_email="mail@erfansamandarian.com",
    url="https://erfansamandarian.com/ctsf",
    license="MIT",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["requests"],
    py_modules=["ctsf"],
    entry_points={"console_scripts": ["ctsf=ctsf:main"]},
)
