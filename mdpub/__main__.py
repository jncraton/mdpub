import mistletoe
import sys

filename = sys.argv[1]

with open(filename, 'r') as fin:
    rendered = mistletoe.markdown(fin)

print(rendered)