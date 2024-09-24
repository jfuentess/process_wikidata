## This code computes several stats from the input .nt file. Some stats are
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
import numpy as np

def count_dict(D, v):
    if v in D:
        D[v] += 1
    else:
        D[v] = 1
        

# Processing arguments
argv = sys.argv[1:]
try:
    options, args = getopt.getopt(argv, "i:s:d",
                               ["input=",
                                "subset-preds=",
                                "max-deg="])
except:
    print("Usage: ", argv[0], " --input <.nt input file> --subset-preds <.txt file with predicates> --max-deg <maximum degree to plot>")

SOURCE_FILE=""
SUBSET_FILE=""
max_deg = None
for name, value in options:
    if name in ['-i', '--input']:
        SOURCE_FILE = value
    elif name in ['-s', '--subset-preds']:
        SUBSET_FILE = value
    elif name in ['-d', '--max-deg']:
        max_deg = int(value)

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

## Step 3: Report results

print("\n")
for i in range(n_subsets):
    print("Frecuency of predicates in subset", i,":",subsets_count[i])


## Sort the in/out degree
sorted_in_degree = sorted(dict_in.items(), key=lambda x:x[1])
sorted_out_degree = sorted(dict_out.items(), key=lambda x:x[1])

n_in = len(dict_in)
n_out = len(dict_out)

## Report the top 10 subjects/predicates with higher degree
print("Top 10 nodes (in-degree): ")
for i in range(10):
    print("\t", sorted_in_degree[n_in - i - 1][0], ": ", sorted_in_degree[n_in - i - 1][1])

print("\nTop 10 nodes (out-degree): ")
for i in range(10):
    print("\t", sorted_out_degree[n_out - i - 1][0], ": ", sorted_out_degree[n_out - i - 1][1])

## if max_deg is define (option --max_deg), generate a histogram up to a maximum
## degree. If not, generate a histogram considering all values
values_in = list(zip(*sorted_in_degree))[1]
values_out = list(zip(*sorted_out_degree))[1]

if max_deg != None:
    limit_in = 0
    # This could be a binary search, but currently is fast enough
    for i in range(n_in):
        if values_in[i] > max_deg:
            break
        limit_in = i

    limit_out = 0
    for i in range(n_out):
        if values_out[i] > max_deg:
            break
        limit_out = i
    
    values_in = values_in[:limit_in]
    values_out = values_out[:limit_out]

## Report the histogram (in console)
hist, bins = np.histogram(values_in)
print("Values in-degree: ", end="")
print(hist)
print("Bins limit in-degree: ", end="")
print(bins)

hist, bins = np.histogram(values_out)
print("Values out-degree: ", end="")
print(hist)
print("Bins limit out-degree: ", end="")
print(bins)

## Report the histogram (in PNG format)
fig, ax = plt.subplots(2,1)
fig.tight_layout(pad=3.0)

values_in = np.log(values_in)
values_out = np.log(values_out)
ax[0].hist(values_in)
ax[1].hist(values_out)

ax[0].title.set_text('Distribution of the in-degree')
ax[0].set_xlabel('in-degree')
ax[0].set_ylabel('Frequency (log scale)')

ax[1].title.set_text('Distribution of the out-degree')
ax[1].set_xlabel('out-degree')
ax[1].set_ylabel('Frequency (log scale)')

plt.savefig("in-out-degree.png")
