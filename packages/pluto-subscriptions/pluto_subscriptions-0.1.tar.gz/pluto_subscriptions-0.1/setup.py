from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="pluto_subscriptions",
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
    author="plutoissaplanet",
    author_email=" ",
    url="https://github.com/plutoissaplanet/pythonWebProject"
)