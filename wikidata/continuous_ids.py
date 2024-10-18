import getopt
import sys

# Processing arguments
argv = sys.argv[1:]
try:
    options, args = getopt.getopt(argv, "i:",
                               ["input="])
except:
    print("Usage: ", argv[0], " --input <.nt input file>")
 
for name, value in options:
    if name in ['-i', '--input']:
        SOURCE_FILE = value
 
f1 = open(SOURCE_FILE, 'r', encoding='utf-8')

n=0
set_SO = set()
set_P = set()

## 1. Create the dictionaries of sujects/objects and predicates
print("STEP 1: Creating the dictionaries")

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

        set_SO.add(sub)
        set_SO.add(obj)
        set_P.add(pred)
        
    if n % 1000000 == 0:
        print("\rProcessing line", n, end="")

    n = n + 1

f1.close()

dict_SO = {so: i for i, so in enumerate(set_SO, start=1)}
dict_P = {p: i for i, p in enumerate(set_P, start=1)}


## 2. Write the dictionaries into files with extensions ".dat.SO" and ".dat.P"
print("\n")
print("STEP 2: Writing the dictionaries to disk")

OUTPUT_FILE_DAT = SOURCE_FILE+".dat"
OUTPUT_FILE_SO = SOURCE_FILE+".dat.SO"
OUTPUT_FILE_P = SOURCE_FILE+".dat.P"

f1 = open(OUTPUT_FILE_SO, 'w', encoding='utf-8')
f2 = open(OUTPUT_FILE_P, 'w', encoding='utf-8')
    
for k,v in dict_SO.items():
    f1.write(str(v) + " " + k + "\n")

for k,v in dict_P.items():
    f2.write(str(v) + " " + k + "\n")

f1.close()
f2.close()


## 3. Write the final dataset into a file with extension ".dat"
print()
print("STEP 3: Writing the output dataset to disk")

f1 = open(SOURCE_FILE, 'r', encoding='utf-8')
f2 = open(OUTPUT_FILE_DAT, 'w', encoding='utf-8')

n=0
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
    
        sub = str(dict_SO[sub])
        pred = str(dict_P[pred])
        obj = str(dict_SO[obj])
        
        f2.write(sub + " " + pred + " " + obj + "\n")
        
    if n % 1000000 == 0:
        print("\rWriting line", n, end="")

    n = n + 1

f1.close()
f2.close()

print("\n")
print("The output dataset is stored at", OUTPUT_FILE_DAT)
print("The dictionaries are stored at", OUTPUT_FILE_SO, "and", OUTPUT_FILE_P)

