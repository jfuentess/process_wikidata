## Original code from Carlos Rojas
## Link: https://github.com/cirojas/leapfrog-benchmark/tree/gh-pages/wikidata-filter
##
## This code filters all the triples with property starting with "<http://www.wikidata.org/prop/"


import getopt
import sys

# Forcing to work with UTF-8 encoding
sys.stdout.reconfigure(encoding="utf-8", newline=None)
sys.stdin.reconfigure(encoding="utf-8", newline=None)
sys.stderr.reconfigure(encoding="utf-8", newline=None)

print("\n### Applying filter \"Remove properties\"", file=sys.stderr)

REMOVED_PROPERTIES_FILE = 'removed_properties.txt'

n=0
removed_properties = set()

for line in sys.stdin:
    n = n + 1

    p = line.split()[1]
    if p.startswith("<http://www.wikidata.org/prop/"):
        print(line, end="")
    else:
        removed_properties.add(p)
            
    if n % 1000000 == 0:
        print("\t[Remove properties] Processing line", n, file=sys.stderr)


f3 = open(REMOVED_PROPERTIES_FILE, 'w', encoding='utf-8')
    
for p in removed_properties:
    f3.write(p+"\n")
    
f3.close()


print("### Processed lines (filter \"Remove properties\"):", n, file=sys.stderr)
