import os
import json
import re
from sklearn.model_selection import train_test_split

input_path = input('Input path of annotated JSON downloaded from LightTag: ')
output_dir = input('Output directory: ')
train, dev, test = [float(x) for x in input('Input train, dev, and test size in fraction, separated by comma: ').replace(', ', ',').split(',')]
assert sum([train, dev, test]) == 1, 'Train, dev, and test size must sum to 1.'

# Input the file
with open(input_path, 'r') as f:
    data = json.load(f)
    
def check_identical(annotations):
    # Check if any annotation is identical
    test_case = [(annotation['start'], annotation['end']) for annotation in annotations]
    return len(test_case) != len(set(test_case))

def check_partial(annotations):    
    # Check if any annotation is part of other annotations 
    other_annotations = [range(annotation['start'], annotation['end']) for annotation in annotations]
    return any([annotation['start'] in other_annotation 
                for annotation in annotations 
                for other_annotation in other_annotations if annotation['start']!=other_annotation.start])

def check_overlap(annotations):
    # Check if annotation has overlaps
    return any((check_identical(annotations), check_partial(annotations)))

def get_labels(result):
    return [re.search('\s(.+$)', line).group(1) for line in result.split('\n') if line]
    
def tag(content, annotations):
    content = list(content)
    annotations
    for annotation in annotations:
        start = annotation['start']
        end = annotation['end']
        tag = annotation['tag']
        content[start] = f'{content[start]} B-{tag}'
        for i in range(start+1, end):
            content[i] = f'{content[i]} I-{tag}'
    content = list(map(lambda x: x + ' O' if not re.search('(I|B)\-', x) else x, content))
    return '\n'.join(content)

# Split the data into train, dev, and test sets
cleaned_data = [example for example in data['data'] if check_overlap(example['annotations'])==False]
train_set, remainder = train_test_split(cleaned_data, train_size=train)
dev_set, test_set = train_test_split(remainder, test_size=dev/(dev + test))

# For each document, tag the content and write to the output file; example with overlapping annotations are omitted
label_set = []
for dataset, destination in zip([train_set, dev_set, test_set], ['train', 'dev', 'test']):
    result = '\n\n'.join([tag(example['content'], example['annotations']) for example in dataset])
    [label_set.append(label) for label in get_labels(result)]
    # Output the result
    with open(os.path.join(output_dir, f'{destination}.txt'), 'w') as f:
        f.write(result)

# Output the labels
with open(os.path.join(output_dir, f'labels.txt'), 'w') as f:
    f.write('\n'.join(sorted(list(set(label_set)), key=lambda x: x.split('-')[1] if x != 'O' else x)))