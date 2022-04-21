from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='PyExpPlotting-andnp',
    url='https://github.com/andnp/PyExpPlotting.git',
    author='Andy Patterson',
    author_email='andnpatterson@gmail.com',
    packages=find_packages(exclude=['tests*']),
    package_data={"PyExpPlotting": ["py.typed"]},
    version='0.8.0',
    license='MIT',
    description='A few plotting utilities to go with PyExpUtils',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    install_requires=[
        "scipy>=1.5.4",
        "matplotlib>=3.3.0",
        "PyExpUtils>=2.4",
    ],
    extras_require={},
)
