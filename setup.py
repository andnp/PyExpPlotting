from setuptools import setup, find_packages

setup(
    name='PyExpPlotting',
    url='https://github.com/andnp/PyExpPlotting.git',
    author='Andy Patterson',
    author_email='andnpatterson@gmail.com',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        "scipy>=1.5.4",
        "matplotlib>=3.3.0",
        "PyExpUtils>=2.4",
    ],
    version=0.8,
    license='MIT',
    description='A few plotting utilities to go with PyExpUtils',
    long_description='todo',
)
