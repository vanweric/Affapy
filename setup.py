"""Fichier set up"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='affapy',
    version='0.1',
    author=[
        "Quentin DESCHAMPS",
        "Florian GUILY",
        "Tristan MICHEL",
        "Ruxue ZENG"
    ],
    author_email=[
        "quentin.deschamps@etu.sorbonne-universite.fr",
        "florian.guily@etu.sorbonne-universite.fr",
        "tristan.michel1@etu.sorbonne-universite.fr",
        "ruxue.zeng@etu.sorbonne-universite.fr"
    ],
    description="A Python library for multiprecision Affine Arithmetic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.lip6.fr/hilaire/affapy",
    packages=["affapy"],
    install_requires=["mpmath"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPLv3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
