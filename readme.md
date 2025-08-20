mdpub
=====

An ebook format with a plaintext featureset

mdpub is:

- [EPUB](https://en.wikipedia.org/wiki/EPUB) compatible
- Smaller than a native markdown document

mdpub is a subset of epub2 with the following features explicity disallowed:

- Stylesheets
- Scripts
- Fonts
- Nav pages

An mdpub document is essentially a markdown document that has been split into chapters, converted to html, mapped to a table of contents, and compressed into the standard epub package.
