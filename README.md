# PII Detection Code Developed by the AISC Community For BigScience Datasets

This repository contains the code for various hackathon efforts to detect personally identifiable information in large language datasets, and in particular BigScience's datasets.

## Quick Start
0. Clone this repo and cd into it
1. Install [conda](https://www.anaconda.com/products/individual) or [miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. Run `conda create create -f environment.yml` - this may take several minutes to install all dependencies and download models
3. Run `conda activate pii` to activate the conda environment
4. Now you can run `python3 test_regex.py -target_lang en` to test the regex for English. Other commands forthcoming!
5. You should create your own regex in your python code as follows:

```
from test_regex import apply_rules
infile = "<your infile such as en.jsonl>"
outfile = "<your outputfile>"
rulebase = [...] # see description below
target_lang = "<your lang>"
right, wrong  = apply_rules(infile, outfile, rulebase, target_lang)
```
## The regex rulebase 

A rulebase is an ordered list of rule groups and the number of times to apply the rule groups.
A rule group is on oredered list of rules of the form (new_label, regex, old_label, before text, after text)
A rule will match if all of regex, old_label, before text and after text matches. 
 - new_label is the label to tag the matching text
 - regex is the regex to use
 - old label is the label that this text was previously tagged as.  None means to ignore the test.  
 - before text is some text before the matching pattern. None means to ignore the test.
 - after text is some text after the matching pattern. None means to ignore the test.

## Docker
1. Run `docker build aisc-pii .` to build the docker image
2. Run `docker run aisc-pii` to run the container. Currently it calls `python3 test_regex.py -target_lang=en` - you will see the output after a minute or two!

## Language Groups Leads
[LEADS - BUT YOUR GITHUB HANDLES HERE]
- Hindi
- Farsi
- Mandarin: @ianyu93
- Vietnamese
- Russian
- Portugese
- English
- Swahili
- Yoruba
- Arabic
- Spanish
- French

## Module 1
[TBD: Put in the current status of the data tagging, which is partially completed. Reference LightTag and a Big THANKS to them!]

## Module 2
Please put your name by the regex you would like to work on here https://docs.google.com/spreadsheets/d/1rX_bH72CgLMwH5wxwakCAq-gbGsK4wFL4cGVqIZpvCQ/edit#gid=1934842843

## Module 3

## Module 4

## PII Library
This code is meant to be used in conjunction with the data pipeline developed under the bigscience github repository:
- https://github.com/bigscience-workshop/data_tooling

## Documentation
- [aisc site]
- https://docs.google.com/document/d/10m7v00UBiAaVbuaYz4IB-Dob8p7Bj7rjIwdxAee1zYU/edit
- 
# Acknowledgements

[TBD] Put names of all contributors here.


