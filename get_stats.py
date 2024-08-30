## This code compute several stats from the input .nt file. Some stats are
##  + Distribution of the in-degree and out-degree of the graph
##  + Number of triples with predicate belonging to different subsets of
##    predicates. The subsets are given as an input file following the format
##   #Subset1
##   <predicate 1>
##   <predicate 2>
##   ...
##   #Subset2
##   <predicate 1>
##   <predicate 2>
##   ...
##
##   For an example, check the file sets_predicates.txt


import getopt
import sys

import matplotlib.pyplot as plt


def count_dict(D, v):
    if v in D:
        D[v] += 1
    else:
        D[v] = 1
        

# Processing arguments
argv = sys.argv[1:]
try:
    options, args = getopt.getopt(argv, "i:s:",
                               ["input=",
                                "subset-preds="])
except:
    print("Usage: ", argv[0], " --input <.nt input file> --subset-preds <.txt file with predicates>")

SOURCE_FILE=""
SUBSET_FILE=""
for name, value in options:
    if name in ['-i', '--input']:
        SOURCE_FILE = value
    elif name in ['-s', '--subset-preds']:
        SUBSET_FILE = value

## Step 1: Read the list of predicate subsets        
list_subsets = list()
subset = set()
n_subsets=0

if SUBSET_FILE != "":
    f1 = open(SUBSET_FILE, 'r', encoding='utf-8')

    while True:
        line = f1.readline()
        if not(line):
            break
        else:
            if line[0] == "#":
                if len(subset) > 0:
                    ss = subset.copy()
                    list_subsets.append(ss)
                n_subsets += 1
                subset.clear()
            else:
                subset.add(line.rstrip())

    if len(subset) > 0:
        ss = subset.copy()
        list_subsets.append(ss)
    subset.clear()
            
    f1.close()


## Step 2: Get the stats
f1 = open(SOURCE_FILE, 'r', encoding='utf-8')

n=0
dict_in = dict()
dict_out = dict()
subsets_count = [0]*len(list_subsets)

while True:
    line = f1.readline()
    if not(line):
        break
    else:
        ## Assumption 1: The elements of the triple are separated by spaces
        ## Assumption 2: The subject and the predicate do not contain spaces
        triple = line.split()
        sub = triple[0]
        pred = triple[1]
        obj = triple[2:]
        obj = " ".join(obj[:-1])

        count_dict(dict_in, obj) 
        count_dict(dict_out, sub)

        for i in range(n_subsets):
            if pred in list_subsets[i]:
                subsets_count[i] += 1
            
        
    if n % 1000000 == 0:
        print("\rProcessing line", n, end="")

    n = n + 1

f1.close()

print("\n")
for i in range(n_subsets):
    print("Frecuency of predicates in subset", i,":",subsets_count[i])


print("\nThe distribution of the in-degree of the graph can be seen at in-degree.png")
print("The distribution of the out-degree of the graph can be seen at out-degree.png")
    
plt.hist(list(dict_in.values()))
plt.xlabel('in-degree')
plt.ylabel('Frecuency')
plt.title("Distribution of the in-degree")
plt.savefig("in-degree.png")

plt.hist(list(dict_out.values()))
plt.xlabel('out-degree')
plt.ylabel('Frecuency')
plt.title("Distribution of the out-degree")
plt.savefig("out-degree.png")
