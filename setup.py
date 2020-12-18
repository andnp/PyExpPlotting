from setuptools import setup, find_packages

setup(
    name='PyExpPlotting',
    url='https://github.com/andnp/PyExpPlotting.git',
    author='Andy Patterson',
    author_email='andnpatterson@gmail.com',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        "matplotlib>=2.2.3",
        "PyExpUtils @ git+ssh://git@github.com/andnp/PyExpUtils@2.5",
    ],
    version=.1,
    license='MIT',
    description='A few plotting utilities to go with PyExpUtils',
    long_description='todo',
)
