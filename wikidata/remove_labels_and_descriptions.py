## Original code from Carlos Rojas
## Link: https://github.com/cirojas/leapfrog-benchmark/tree/gh-pages/wikidata-filter
##
##

import getopt
import sys

# Forcing to work with UTF-8 encoding
sys.stdout.reconfigure(encoding="utf-8", newline=None)
sys.stdin.reconfigure(encoding="utf-8", newline=None)
sys.stderr.reconfigure(encoding="utf-8", newline=None)

print("\n### Applying filter \"Remove labels and descriptions\"", file=sys.stderr)

# Defining properties to be deleted
STRING_PATTERN = '"@'
ENGLISH_PATTERN = '"@en '
OTHER_ENGLISH_PATTERN = '"@en-'

filtered_properties = set()
filtered_properties.add('<http://www.w3.org/2000/01/rdf-schema#label>')
filtered_properties.add('<http://www.w3.org/2004/02/skos/core#altLabel>')
filtered_properties.add('<http://www.w3.org/2004/02/skos/core#prefLabel>')
filtered_properties.add('<http://schema.org/description>')

n=0
for line in sys.stdin:
    n = n + 1

    if line.split()[1] in filtered_properties:
        continue
    elif STRING_PATTERN not in line: # not a label/description and don't have a string: we write it
        print(line, end="")
    elif ENGLISH_PATTERN in line and OTHER_ENGLISH_PATTERN not in line: # line has a string, we only write if it's in english
        print(line, end="")

    if n % 10000000 == 0:
        print("\t[Remove labels and descriptions] Processing line", n, file=sys.stderr)


print("### Processed lines (filter \"Remove labels and descriptions\"):", n, file=sys.stderr)
    
