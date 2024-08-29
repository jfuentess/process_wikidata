# Processing the Wikidata dataset
This repository is a collection of scripts to pre-process a dump Wikidata. All
the code was tested with the *latest-truthy* dump of Wikidata (June 9th, 2024).

## Filters
The first step is to apply some filters to the dump in order to reduce redundant
or unnecessary triples

### Filter 1: Remove labels and descriptions
This filter is aimed to remove descriptions of Subjects/Objects in multiple
languages, leaving only the English description

```sh
python remove_labels_and_descriptions.py --input <input .nt file> --output <output .nt file>
```


### Filter 2: Remove properties
This filter removes all the properties not starting with
"<http://www.wikidata.org/prop/". As a byproduct, this filter generates a file
named `removed_properties.txt` with all  properties removed.

```sh
python remove_properties.py --input <input .nt file> --output <output .nt file>
```


| Dataset                   | Number of triples  |
| ------------------------- | ------------------ |
| latest-truthy (original)  | 8,254,120,518      |
| After filter 1            | 2,276,362,123      |
| After filter 2            | 1,617,500,079 (26 properties deleted)      |

## Continuous identifiers 
The second step is to convert the filtered dataset into a new version using continuous identifiers for the subject/objects and predicates. The final format includes a `.nt` file and two dictionaries to convert identifiers to entries of the filtered dataset.

```sh
g++ -O3 -o ttl2dat ttl2dat.cpp
./ttl2dat <input .nt file>
```

## Query engines


