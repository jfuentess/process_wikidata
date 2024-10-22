# - *- coding: utf-8 - *-
# Dependencies
#      pip install pyshp
#
# Description: This script gets all the adjacency relations (neighboring) stored in
#              the Edges ShapeFile of Tiger Dataset. Each edge in the ShapeFile
#              has two face identifiers: one for the left face (TFIDL) and one
#              for the right face (TFIDR). We use the face identifiers to
#              construct the relations
#

import sys
import os
import shapefile
import getopt

def process_edges_shp(directory):
    vertices = {}
    num_files = 0
    
    # Extracting vertices from each ShapeFile in the folder
    for filename in os.listdir(directory):

        # Only process files with extension .shp
        if filename.endswith(".shp"):
            num_files += 1

            if num_files%100 == 0:
                print("Processed files:", num_files, file=sys.stderr)

            # Read the ShapeFile
            sf = shapefile.Reader(directory + filename)

            # List of shapes in the ShapeFile
            shapes=sf.shapes()
            num_shapes=len(shapes)

            for i in range(0, num_shapes):
                rec=sf.record(i)

                # Avoid self-loops
                if rec["TFIDL"] == rec["TFIDR"]:
                    continue
                else:
                    if rec["TFIDR"] not in vertices:
                        vertices[rec["TFIDR"]] = []
                    if rec["TFIDL"] not in vertices:
                        vertices[rec["TFIDL"]] = []

                    # Inserting nodes in the adyacency lists of the vertices
                    # TFIDL stands for "Permanent face ID on the left of the edge"
                    # TFIDR stands for "Permanent face ID on the right of the
                    # edge"

                    # Note: The relation is symmetric (no need to store the
                    # complement)
                    vertices[rec["TFIDR"]].append(rec["TFIDL"])
        else:
            continue

    print("Total number of processed files: ", num_files, file=sys.stderr)
        
    total_relations = 0
    for vtx in vertices.values():
        total_relations += len(vtx)

    print("total relations (unique)   :", total_relations, file=sys.stderr)
    print("total elements:", len(vertices), file=sys.stderr)

    # Write the adjacency relations in .nt format
    for src in vertices:
        for tgt in vertices[src]:
            print(src, "shares_boundary_with", tgt, ".")



# Processing arguments
argv = sys.argv[1:]
try:
    options, args = getopt.getopt(argv, "i:", ["input="])

except:
    print("Usage: ", sys.argv[0], " --input <Path to .shp edges files>", file=sys.stderr)

SOURCE_PATH=""
for name, value in options:
    if name in ['-i', '--input']:
        SOURCE_PATH = value
            
process_edges_shp(SOURCE_PATH)
