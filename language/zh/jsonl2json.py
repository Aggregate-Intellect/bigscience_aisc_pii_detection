import os
import json

print(
    """
    =========================================================
    This script is used to convert jsonl file to json file.
    Please ensure that the jsonl file has the follwoing keys:
    - id: the id of the example
    - text: the text of the example
    - lang: language of the example
    - domain: domain (e.g., news, movie, oscar, etc.) of the example
    - ner: a list of named entities with the ner of the example, 
    e.g. [['John Smith', 'PERSON'], ['American', 'NORP']]
    
    The script outputs two json files:
    - file_name_text.json: to be used with upload_dataset.py
    - file_name_tags.json: to be used with upload_suggestions_model.py
    
    ** Note **
    The final output will not include where tagged substrings are not found in the example text. 
    """)

def text_index(string, substring):
    # Return the start and end indices of substring in string
    return string.index(substring), string.index(substring) + len(substring)

# Define input file paths, output directory, and output file name
input_file = input('Input file_path: ')
output_dir = input('Output directory: ')
output_file_name = os.path.splitext(os.path.basename(input_file))[0]
output_file_path = os.path.join(output_dir, output_file_name)

# Open the jsonl file
with open(input_file, 'r') as json_file:
    json_list = list(json_file)

# Convert to a list of dictionaries
data = [json.loads(json_str) for json_str in json_list]

# Create a list of dictionaries for text.json
pii_text = [
    {
        'id': example['id'], 
        'text': example['text'], 
        'lang': example['lang'], 
        'domain': example['domain']
    } for example in data
]

# Create a list of dictionaries for tags.json
pii_suggestion_list = []
total_examples = len(data)
errors = 0
for example in data:
    for example_text, example_tag in example['ner']:
        try:
            start, end = text_index(example['text'], example_text)
            pii_suggestion_list.append(
                {
                    "example_id": example['id'], 
                    "tag": example_tag, 
                    "start": start,
                    "end": end,
                    "text": example_text
                }
            )
        except Exception as e: 
            print(f"ID: {example['id']}")
            print(f"Text: {example['text']}")
            print(f"Example Text: {example_text}")
            print(e)
            errors+=1            
print(f"{errors} errors out of {total_examples} total examples")

# Output converted files
with open(f'{output_file_path}_text.json', 'w') as f:
    json.dump(pii_text, f)
    
with open(f'{output_file_path}_tags.json', 'w') as f:
    json.dump(pii_suggestion_list, f)