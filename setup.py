import os
from io import open

import setuptools

with open("README.md") as fh:
    long_description = fh.read()


here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)

version_contents = {}
with open(os.path.join(here, "truework", "version.py"), encoding="utf-8") as f:
    exec(f.read(), version_contents)

setuptools.setup(
    name="truework",
    version=version_contents["VERSION"],
    author="Truework",
    author_email="python-sdk@truework.com",
    description="An SDK to use the Truework API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/truework/truework-sdk-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7, <4",
    install_requires=["requests>=2.20.0", "attrs==19.3.0", "cattrs==1.0.0"],
)
