import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_bgpfuzz_rpc",
    version="0.2",
    author="P.Dashevskyi",
    author_email="",
    description="A bgp rpc monitor for boofuzz",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['Boofuzz>=0.4.1'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)