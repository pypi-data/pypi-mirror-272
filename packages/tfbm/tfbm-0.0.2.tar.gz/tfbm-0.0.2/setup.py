from setuptools import find_packages, setup

with open("tfbm/README.md", "r", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="tfbm",
    version="0.0.2",
    description="The Time-Frequency Breakdown Method (TFBM) was developed for the detection of brain oscillations in time-frequency representations (such as spectrograms obtained from the Fourier Transform).",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/ArdeleanRichard/Time-Frequency-Breakdown-Method",
    author="Eugen-Richard Ardelean",
    author_email="ardeleaneugenrichard@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy", "scikit-learn"],
    extras_require={
        "dev": ["twine>=4.0.2"],
    },
    python_requires=">=3.7",
)
