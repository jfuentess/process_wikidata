## This code deletes invalid edges in the graph represented by a .nt file. The deleted
## edges/predicates are limited to predicates related to the containment
## relation, given in an input file following the format 
##   <predicate 1>
##   <predicate 2>
##   ...
##
##   For an example, check the file containment_predicates.txt


import getopt
import sys
from collections import defaultdict

## The code to store and traverse the graph was adapted from the code at https://www.geeksforgeeks.org/python-program-for-depth-first-search-or-dfs-for-a-graph/


# This class represents a directed graph using adjacency list representation
class Graph:

    # Constructor
    def __init__(self):
        # Default dictionary to store graph
        self.graph = defaultdict(list)
    
    # Function to add an weighted edge to graph
    def addEdge(self, u, v, w):
        self.graph[u].append((v, w))
    
    # A function used by DFS
    def DFSUtil(self, v, visited, cycles):

        # Mark the current node as visited
        visited.add(v)

        # Recur for all the vertices adjacent to this vertex
        for neighbour in self.graph[v]:
            target = neighbour[0] 
            label = neighbour[1] 
            if target not in visited:
                self.DFSUtil(target, visited, cycles)
            else:
                ## We found a cycle
                cycles.add(label)

    
    # The function to do DFS traversal. It uses recursive DFSUtil()
    # Assumption: The graph can be non-connected
    def DFS(self, cycles, init_vertices, visited = set()):
        n_components = 0

        # All the vertices to start a traversal (vertices with in-degree 0) 
#        init_vertices = get_starting_vertices(self)
        
        for init_v in init_vertices:
            if init_v not in visited:
                init_size = len(visited)
        
                v = init_v
                self.DFSUtil(v, visited, cycles)

                end_size = len(visited)

                # print("Component ", n_components, ": ", end_size - init_size, "vertices")            

                n_components += 1

        print("# Number of components:", n_components)
        print("# Number of visited vertices:", len(visited))
        print("# Number of edges to be deleted:", len(cycles))
        
# Processing arguments
argv = sys.argv[1:]
try:
    options, args = getopt.getopt(argv, "i:o:s:",
                               ["input=",
                                "output=",
                                "subset-preds="])
except:
    print("Usage: ", argv[0], " --input <.nt input file> --output <.nt output file> --subset-preds <.txt file with predicates>")

SOURCE_FILE=""
TARGET_FILE=""
SUBSET_FILE=""
REMOVED_EDGES_FILE = 'removed_triples_cycle.txt'
for name, value in options:
    if name in ['-i', '--input']:
        SOURCE_FILE = value
    elif name in ['-o', '--output']:
        TARGET_FILE = value
    elif name in ['-s', '--subset-preds']:
        SUBSET_FILE = value


## Step 1: Read the list of predicate subsets        
print("\n### Reading the list of predicate subsets")
subset_preds_direct = set()
subset_preds_reverse = set()

if SUBSET_FILE != "":
    f1 = open(SUBSET_FILE, 'r', encoding='utf-8')

    while True:
        line = f1.readline()
        if not(line):
            break
        else:
            pred = line.split()[0]
            direction = line.split()[1]
            if direction == "0":
                subset_preds_direct.add(pred)
            elif direction == "1":
                subset_preds_reverse.add(pred)

    f1.close()


## Step 2: Get the graph
print("\n### Reading the input graph")
f1 = open(SOURCE_FILE, 'r', encoding='utf-8')
n=0
g = Graph()

# Sets of vertices that are sources and targets of edges. It will be used to
# compute vertices with in-degree 0
sources = set()
targets = set()
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
        
        if pred in subset_preds_direct:
            g.addEdge(sub, obj, n)
            sources.add(sub) 
            targets.add(obj)
        elif pred in subset_preds_reverse:
            g.addEdge(obj, sub, n)
            sources.add(obj) 
            targets.add(sub)
           
    if n % 1000000 == 0:
        print("\rProcessing line", n, end="")
    
    n = n + 1
    
f1.close()


## Step 3: Get the set of edges to be deleted
print("\n### Computing invalid edges (first pass)")
cycles = set()
visited = set()
init_vertices = sources.difference(targets)
all_vertices = sources.union(targets)

print("\tinit_vertices:", len(init_vertices))
print("\tnum vertices(union):", len(all_vertices))
g.DFS(cycles, init_vertices, visited)

print("\n### Computing invalid edges (second pass)")
init_vertices = all_vertices.difference(visited)
print("\tinit_vertices:", len(init_vertices))
g.DFS(cycles, init_vertices, visited)


## Step 4: Get the new graph without invalid edges
print("\n### Writing the graph without invalid edges")
f1 = open(SOURCE_FILE, 'r', encoding='utf-8')
f2 = open(TARGET_FILE, 'w', encoding='utf-8')
f3 = open(REMOVED_EDGES_FILE, 'w', encoding='utf-8')

n=0

while True:
    line = f1.readline()
    if not(line):
        break
    else:
        if n not in cycles:
            f2.write(line)
        else:
            f3.write(line)

    if n % 1000000 == 0:
        print("\rProcessing line", n, end="")

    n = n + 1
    
f1.close()
f2.close()
f3.close()
