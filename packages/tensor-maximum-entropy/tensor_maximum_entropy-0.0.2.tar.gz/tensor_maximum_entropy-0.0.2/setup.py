from setuptools import find_packages, setup

with open("tensor_maximum_entropy/README.md", "r") as f:
    long_description = f.read()

setup(
    name="tensor_maximum_entropy",
    version="0.0.2",
    description="Python implementation of the Tensor Maximum Entropy (TME)",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArdeleanRichard/TME",
    author="Eugen-Richard Ardelean",
    author_email="ardeleaneugenrichard@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy", "scipy", "matplotlib", "scikit-learn"],
    extras_require={
        "dev": ["twine>=4.0.2"],
    },
    python_requires=">=3.7",
)
