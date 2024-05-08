from setuptools import find_packages, setup

with open("spike_cluster_score/README.md", "r", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="spike_cluster_score",
    version="0.0.1",
    description="Spike Cluster Score (SCS) is a clustering performance metric designed with the purpose of spike sorting in mind",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArdeleanRichard/Spike-Cluster-Score",
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
