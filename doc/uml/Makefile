uml:
	pyreverse -o dot -p affapy -A -S -f OTHER ../../affapy

png: uml
	dot -Tpng classes_affapy.dot -o uml.png
	@make clear

pdf: uml
	dot -Tpdf classes_affapy.dot -o uml.pdf
	@make clear

clear:
	rm classes_affapy.dot packages_affapy.dot
