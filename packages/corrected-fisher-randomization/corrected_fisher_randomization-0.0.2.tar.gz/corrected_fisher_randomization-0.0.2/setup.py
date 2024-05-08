from setuptools import find_packages, setup

with open("corrected_fisher_randomization/README.md", "r") as f:
    long_description = f.read()

setup(
    name="corrected_fisher_randomization",
    version="0.0.2",
    description="Python implementation of the Corrected Fisher Randomization (CFR)",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArdeleanRichard/CFR",
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
