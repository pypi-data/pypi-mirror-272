from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='infoindia',
    version='1.1.0',
    packages=find_packages(),
    install_requires=['requests'],
    author='Vijay Chouhan',
    author_email='vijay977364@gmail.com',
    description='Wrapper for State Data APIs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/NarutoUzumvki/state_data_api',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)