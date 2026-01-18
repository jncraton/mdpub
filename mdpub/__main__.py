import sys
import mistletoe
import re
from ebooklib import epub

epub.CHAPTER_XML = b'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"></html>'


def get_title(doc):
    """Returns title for a document

    First heading becomes title
    """
    title = ""
    for node in doc.children:
        if isinstance(node, mistletoe.block_token.Heading):
            title = "".join([c.content for c in node.children])
            break
    return title


def get_top_heading(doc):
    top_level = 6
    for node in doc.children:
        if isinstance(node, mistletoe.block_token.Heading) or isinstance(
            node, mistletoe.block_token.SetextHeading
        ):
            top_level = min(top_level, node.level)

    return top_level


def create_epub(filename, output_filename):
    with open(filename, "r") as fin:
        doc = mistletoe.Document(fin)

        top_level = get_top_heading(doc)
        title = get_title(doc)

        with mistletoe.HtmlRenderer() as renderer:
            rendered = renderer.render(doc)

    # Split by second highest heading, prepend content we split by
    wedge = f"\n<h{top_level+1}"
    chapters = rendered.split(wedge)
    chapters = [wedge + c for c in chapters]
    chapters[0] = chapters[0][len(wedge) :]

    book = epub.EpubBook()

    # Create chapters
    toc = []
    book.spine = []

    for i, chapter in enumerate(chapters):
        first_line = chapter.strip().split("\n")[0]
        chapter_title = re.sub(r"<.+?>", "", first_line)

        c = epub.EpubHtml(title=chapter_title, file_name=f"{i}.xhtml")
        c.content = chapter
        book.add_item(c)
        book.spine.append(c)
        toc.append(c)

    book.toc = tuple(toc)
    book.add_item(epub.EpubNcx())

    # write to the file
    epub.write_epub(
        output_filename,
        book,
        {
            "epub2_guide": True,
            "epub3_landmark": True,
            "epub3_pages": True,
            "landmark_title": "Guide",
            "pages_title": "Pages",
            "spine_direction": True,
            "package_direction": False,
            "play_order": {"enabled": True, "start_from": 1},
            "raise_exceptions": False,
            "compresslevel": 9,
        },
    )


if __name__ == "__main__":
    filename = sys.argv[1]
    output_filename = sys.argv[2]
    create_epub(filename, output_filename)
