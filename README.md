# Processing the Wikidata dataset
This repositorio is a collection of scripts to process the Wikidata dataset.

**Note:** The committed code was tested with *latest-truthy-09jun2024* dump of Wikidata.

## Filters
The first step is to apply some filters to the dump in order to reduce redundant information

## Continuous identifiers 
The second step is to convert the filtered dataset to a new version using continuous identifiers for the subject/objects and predicates. The final format includes a `.nt` file and two dictionaries to convert identifiers to entries in the filtered dataset.

## Query engines
