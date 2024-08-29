## Original code from Carlos Rojas
## Link: https://github.com/cirojas/leapfrog-benchmark/tree/gh-pages/wikidata-filter
##
##

import getopt
import sys

# Processing arguments

argv = sys.argv[1:]
try:
    options, args = getopt.getopt(argv, "i:o:",
                               ["input=",
                                "output="])
except:
    print("Usage: ", argv[0], " --input <.nt input file> --output <.nt output file>")
 
for name, value in options:
    if name in ['-i', '--input']:
        SOURCE_FILE = value
    elif name in ['-o', '--output']:
        TARGET_FILE = value
 

# Defining properties to be deleted
STRING_PATTERN = '"@'
ENGLISH_PATTERN = '"@en '
OTHER_ENGLISH_PATTERN = '"@en-'

filtered_properties = set()
filtered_properties.add('<http://www.w3.org/2000/01/rdf-schema#label>')
filtered_properties.add('<http://www.w3.org/2004/02/skos/core#altLabel>')
filtered_properties.add('<http://www.w3.org/2004/02/skos/core#prefLabel>')
filtered_properties.add('<http://schema.org/description>')


f1 = open(SOURCE_FILE, 'r', encoding='utf-8')
f2 = open(TARGET_FILE, 'w', encoding='utf-8')

n=0
while True:
    line = f1.readline()
    if not(line):
        break
    else:
        if line.split()[1] in filtered_properties:
            continue
        elif STRING_PATTERN not in line: # not a label/description and don't have a string: we write it
            f2.write(line)
        elif ENGLISH_PATTERN in line and OTHER_ENGLISH_PATTERN not in line: # line has a string, we only write if it's in english
            f2.write(line)

    if n % 1000000 == 0:
        print("Processing line", n)

    n = n + 1
            
f1.close()
f2.close()
