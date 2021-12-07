import argparse
import json
import os
from hanziconv import HanziConv

"""
Creates traditional and simplified Chinese lexicons from lexicons/zh.json
Usage:
	python -m ontology.mandarin.convert_zh_unicode (change --export-path flag if necessary)
"""

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'--lexicon-path', 
		default='./lexicons/zh.json'
	)
	parser.add_argument(
		'--export-path',
		default='./language/zh'
	)
	args = parser.parse_args()
	zh_simplified_dict = {}
	zh_traditional_dict = {}

	with open(args.lexicon_path) as json_file:
		data = json.load(json_file)

		for key in data.keys():
			zh_simplified_entities = []
			zh_traditional_entities = []
			for item in data[key]:
				if isinstance(item, str):
					zh_simplified_entities.append(HanziConv.toSimplified(item))
					zh_traditional_entities.append(HanziConv.toTraditional(item))
					assert HanziConv.same(zh_simplified_entities[-1], zh_traditional_entities[-1])

			if len(zh_simplified_entities) > 0:	
				zh_simplified_dict[key] = zh_simplified_entities
			else:
				zh_simplified_dict[key] = data[key] 
			
			if len(zh_traditional_entities) > 0:
				zh_traditional_dict[key] = zh_traditional_entities
			else:
				zh_traditional_dict[key] = data[key]
		
		assert zh_traditional_dict.keys() == data.keys()
		assert zh_simplified_dict.keys() == data.keys()
	
	with open(os.path.join(args.export_path, 'zh_simplified.json'), 'w', encoding='utf-8') as output:
		json.dump(zh_simplified_dict, output)

	with open(os.path.join(args.export_path, 'zh_traditional.json'), 'w', encoding='utf-8') as output:
		json.dump(zh_traditional_dict, output)

if __name__ == "__main__":
	main()

