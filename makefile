all:

constitution.epub: examples/constitution.md
	python3 -m mdpub $< $@

clean:
	rm -f *.epub