import os
import json
import re
import importlib
import spacy
from sklearn.model_selection import train_test_split

answer = input('Tokenization through an existing pakcage? [y/n] ')
assert answer in ['y', 'n'], 'Must be y or n'

# Define language model
if answer == 'y':
    package = input('Input package name (e.g. en_core_web_sm) ')
    nlp = spacy.load(package)
elif answer == 'n':
    code, language = input('Input code and language name, '
                           'separated by comma (e.g. en, English): ').replace(' ', '').split(',')
    tokenizer = getattr(importlib.import_module(
        f'spacy.lang.{code}'), language)
    nlp = tokenizer()

# Define input file paths, output, directory, and trian/dev/test split size
input_path = input('Input path of annotated JSON downloaded from LightTag: ')
output_dir = input('Output directory: ')
train, dev, test = [float(x) for x in input(
    'Input train, dev, and test size in fraction, separated by comma: ').replace(', ', ',').split(',')]
assert sum([train, dev, test]) == 1, 'Train, dev, and test size must sum to 1.'

# Input the file
with open(input_path, 'r') as f:
    data = json.load(f)


def check_identical(annotations):
    # Check if any annotation is identical
    test_case = [(annotation['start'], annotation['end'])
                 for annotation in annotations]
    return len(test_case) != len(set(test_case))


def check_partial(annotations):
    # Check if any annotation is part of other annotations
    other_annotations = [range(annotation['start'], annotation['end'])
                         for annotation in annotations]
    return any([annotation['start'] in other_annotation
                for annotation in annotations
                for other_annotation in other_annotations if annotation['start'] != other_annotation.start])


def check_overlap(annotations):
    # Check if annotation has overlaps
    return any((check_identical(annotations), check_partial(annotations)))


def get_labels(result):
    # Get labels for each line
    return [re.search('\s(.+$)', line).group(1) for line in result.split('\n') if line]


def indexing(annotation):
    # Return annotated index and values
    return annotation['start'], annotation['end'], annotation['tag']


def flatten(list_):
    # Flatten a nested list
    return [item for sublist in list_ for item in sublist]


def tagging(subdoc, annotated_values):

    # Find matching tag given index

    start = subdoc[0]
    end = subdoc[1]
    tag = [x[2] for x in annotated_values if x[0] == start if x[1] == end]
    tokenized = tokenize(subdoc[2])
    first_token = tokenized[0]
    for token in tokenized:
        if len(tag) == 0:
            yield token+' O'
        else:
            yield token+f' B-{tag[0]}' if token == first_token else token+f' I-{tag[0]}'


def tokenize(text):
    # Tokenize a string
    return [token.text for token in nlp(text)]


def convert(content, annotations):
    # Convert each content to IOB format with annotations
    if len(annotations) == 0:
        return '\n'.join([token+' O' for token in tokenize(content)])
    indices = sorted(flatten(
        [[annotation['start'], annotation['end']] for annotation in annotations]))
    splitted_content = [(i, j, content[i:j])
                        for i, j in zip(indices, indices[1:]+[None])]
    splitted_content = [x for x in splitted_content if x[2] != '']
    annotated_values = [indexing(x) for x in annotations]
    return '\n'.join(flatten([list(tagging(subdoc, annotated_values)) for subdoc in splitted_content]))


# Split the data into train, dev, and test sets
cleaned_data = [example for example in data['data']
                if check_overlap(example['annotations']) == False]
train_set, remainder = train_test_split(cleaned_data, train_size=train)
dev_set, test_set = train_test_split(remainder, test_size=dev/(dev + test))

# For each document, tag the content and write to the output file; example with overlapping annotations are omitted
label_set = []
for dataset, destination in zip([train_set, dev_set, test_set], ['train', 'dev', 'test']):
    result = '\n\n'.join(
        [convert(example['content'], example['annotations']) for example in dataset])
    [label_set.append(label) for label in get_labels(result)]
    # Output the result
    with open(os.path.join(output_dir, f'{destination}.txt'), 'w') as f:
        f.write(result)

# Output the labels
with open(os.path.join(output_dir, f'labels.txt'), 'w') as f:
    f.write('\n'.join(sorted(list(set([label.replace(
        ' ', '') for label in label_set])), key=lambda x: x.split('-')[1] if x != 'O' else x)))
