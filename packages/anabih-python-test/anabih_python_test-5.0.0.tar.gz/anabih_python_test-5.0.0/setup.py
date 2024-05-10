import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anabih_python_test",
    version="5.0.0",
    author="Ahmed Nabih",
    author_email="anabih2000@yahoo.com",
    description="Python test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anabih/python-test",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
