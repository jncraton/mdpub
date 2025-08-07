import sys
import mistletoe
from ebooklib import epub

filename = sys.argv[1]

def get_top_heading(doc):
    top_level = 6
    for node in doc.children:
        if isinstance(node, mistletoe.block_token.Heading):
            top_level = min(top_level, node.level)

    return top_level

with open(filename, 'r') as fin:
    rendered = mistletoe.markdown(fin)

book = epub.EpubBook()

# set metadata
book.set_identifier("isbn")
book.set_title("title")
book.set_language("en")

book.add_author("author")

# create chapter
c1 = epub.EpubHtml(title="title", file_name="1.xhtml", lang="en")
c1.content = rendered
book.add_item(c1)

# define Table Of Contents
book.toc = (
    epub.Link("1.xhtml", "1", "intro"),
    (epub.Section("Simple book"), (c1,)),
)

# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# basic spine
book.spine = ["nav", c1]

# write to the file
epub.write_epub(filename + ".epub", book, {})