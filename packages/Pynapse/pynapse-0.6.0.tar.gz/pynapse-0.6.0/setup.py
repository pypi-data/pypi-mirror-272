from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='Pynapse',
    version='0.6.0',
    packages=find_packages(),
    install_requires=['numpy'],
    long_description= description,
    long_description_content_type="text/markdown",
)