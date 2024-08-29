## Original code from Carlos Rojas
## Link: https://github.com/cirojas/leapfrog-benchmark/tree/gh-pages/wikidata-filter
##
## This code filters all the triples with property starting with "<http://www.wikidata.org/prop/"


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
 
REMOVED_PROPERTIES_FILE = 'removed_properties.txt'

f1 = open(SOURCE_FILE, 'r', encoding='utf-8')
f2 = open(TARGET_FILE, 'w', encoding='utf-8')

n=0
removed_properties = set()

while True:
    line = f1.readline()
    if not(line):
        break
    else:
        p = line.split()[1]
        if p.startswith("<http://www.wikidata.org/prop/"):
            f2.write(line)
        else:
            removed_properties.add(p)
            
    if n % 1000000 == 0:
        print("Processing line", n)

    n = n + 1

f1.close()
f2.close()


f3 = open(REMOVED_PROPERTIES_FILE, 'w', encoding='utf-8')
    
for p in removed_properties:
    f3.write(p+"\n")
    
f3.close()
