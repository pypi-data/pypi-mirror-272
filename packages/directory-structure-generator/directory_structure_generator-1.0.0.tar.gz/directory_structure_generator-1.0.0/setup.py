from setuptools import setup, find_packages

setup(
    name="directory-structure-generator",
    version="1.0.0",
    author="Ahmed Hossam",
    author_email="ahmed.7oskaa@gmail.com",
    description="This script is used to generate a list of the project structure in a markdown format. It is useful for README.md files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/7oSkaaa/Directory-Structure-Generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
