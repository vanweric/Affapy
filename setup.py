"""Fichier set up"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='affapy',
    version='0.1',
    author=[
        "Ruxue ZENG",
        "Quentin DESCHAMPS",
        "Florian GUILY",
        "Tristan MICHEL"
    ],
    author_email=[
        "quentin.deschamps@etu.sorbonne-universite.fr",
        "florian.guily@etu.sorbonne-universite.fr",
        "tristan.michel1@etu.sorbonne-universite.fr",
        "ruxue.zeng@etu.sorbonne-universite.fr"
    ],
    description="A python library for multiprecision Affine Arithmetic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.lip6.fr/hilaire/affapy",
    packages=["AffApy"],
    install_requires=['Sphinx', 'mpmath', 'sphinx-rtd-theme'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # to complete
        "Operating System :: OS Independent",  # to complete
    ],
    python_requires='>=3.5',
)
