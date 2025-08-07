all: constitution.epub

constitution.epub: examples/constitution.md
	python3 -m mdpub $< $@

format:
	black mdpub/*.py

clean:
	rm -f *.epub