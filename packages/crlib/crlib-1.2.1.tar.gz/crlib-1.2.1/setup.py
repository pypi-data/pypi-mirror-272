from setuptools import setup

mdata = {}
with open("crlib/metadata.py", "r") as f:
    for line in f.read().split("\n")[:~0]:
        linedata = [i.strip(" \"") for i in line.split("=")]
        mdata[linedata[0]] = linedata[1]

with open("README.rst", "r") as f:
    readme = f.read()

# set-oop
setup(
    name="crlib",
    version=mdata["__version__"],
    description="Cuboid Raptor's Lib Rary, A Garbage Collection Of Garbage For Your Garbage Needs™",
    url=mdata["__url__"],
    author=mdata["__author__"],
    author_email=mdata["__authoremail__"],
    license="GNU GPLv3",
    packages=["crlib"],
    install_requires=[
        "dill>=0.3.0",
        "lazy_import>=0.2.0"
    ],
    python_requires=">=3.6",
    long_description=readme,
    long_description_content_type="text/x-rst",
)
