import json
import re

input_path = input('Input path of annotated JSON downloaded from LightTag: ')
output_path = input('Output path of IOB-formatted text (with .txt extension): ') # e.g. exmaple.text

# Input the file
with open(input_path, 'r') as f:
    data = json.load(f)
    
def check_overlap(annotations):    
    # Check if there are annotations with overlapping indices
    other_annotations = [range(annotation['start'], annotation['end']) for annotation in annotations]
    return any([annotation['start'] in other_annotation for annotation in annotations for other_annotation in other_annotations if annotation['start']!=other_annotation.start])

def tag(content, annotations):
    
    # Split the content into a list of characters
    content = list(content)
    # For each annotation, add annotated tag to the character
    for annotation in annotations:
        start = annotation['start']
        end = annotation['end']
        tag = annotation['tag']
        content[start] = f'{content[start]} B-{tag}'
        for i in range(start+1, end):
            content[i] = f'{content[i]} I-{tag}'
    # For each character, add O tag if it is not annotated
    content = list(map(lambda x: x + ' O' if not re.search('(I|B)\-', x) else x, content))
    
    return '\n'.join(content)

# For each document, tag the content and write to the output file; example with overlapping annotations are omitted
result = '\n\n'.join([tag(example['content'], example['annotations']) for example in data['data'] if check_overlap(example['annotations'])==False])

# Output the result
with open(output_path, 'w') as f:
    f.write(result)