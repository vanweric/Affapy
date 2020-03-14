import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name='AffApy',
	version='0.1',  #to complete
	scripts=['AffA'],  #to complete
	author=[
		"Ruxue ZENG",
		"Quentin DESCHAMPS",
		"Florian GUILY",
		"Tristan MICHEL"
	],
	author_email=[
		"roxue.zeng@etu.sorbonne-universite.fr",
		"quentin.deschamps1@etu.sorbonne-universite.fr",
		"florian.guily@etu.sorbonne-universite.fr",
		"tristan.michel1@etu.sorbonne-universite.fr"
	],
	description="A package using affine and interval arithmetic to predict variables content.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/.../AffApy", #to complete
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License", #to complete
		"Operating System :: OS Independent", #to complete
	],
 )