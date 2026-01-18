all: constitution.epub

%.epub: examples/%.md
	python3 -m mdpub $< $@
	wc $@

format:
	black mdpub/*.py

clean:
	rm -f *.epub
	rm -rf mdpub/__pycache__