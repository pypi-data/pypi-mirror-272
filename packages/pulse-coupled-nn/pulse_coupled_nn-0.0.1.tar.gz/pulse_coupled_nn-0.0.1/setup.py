from setuptools import find_packages, setup

with open("pulse_coupled_nn/README.md", "r") as f:
    long_description = f.read()

setup(
    name="pulse_coupled_nn",
    version="0.0.1",
    description="Python implementation of the Pulse Coupled Neural Network (PCNN)",
    package_dir={"": "pulse_coupled_nn"},
    packages=find_packages(where="pulse_coupled_nn"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArdeleanRichard/PCNN",
    author="Eugen-Richard Ardelean",
    author_email="ardeleaneugenrichard@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy", "scipy", "matplotlib", "astropy"],
    extras_require={
        "dev": ["twine>=4.0.2"],
    },
    python_requires=">=3.7",
)
