from setuptools import setup, find_packages

setup(
    name="GazooResearchUtils",
    version="1.3.5",
    description="Allows Analysis of GazooResearch Data",
    package_dir={"":"app"},
    packages=find_packages(where="app"),
    url="https://gazooresearch.com/",
    author='Andrew Lim MD, Megan Lim MD, Christopher Lim MD, Robert Lim MD',
    #install_requires=["numpy >= 1.26.2", "pandas >= 2.2.2", "lifelines == 0.28.0"],
    python_requires=">=3.10"
)
