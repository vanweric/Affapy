uml:
	pyreverse -o dot -p AffApy -A -S -f OTHER ../../AffApy

png: uml
	dot -Tpng classes_AffApy.dot -o uml.png
	@make clear

pdf: uml
	dot -Tpdf classes_AffApy.dot -o uml.pdf
	@make clear

clear:
	rm classes_AffApy.dot packages_AffApy.dot
