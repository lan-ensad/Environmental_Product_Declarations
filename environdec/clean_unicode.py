import json
import os

def decode_unicode_in_json(input_path, output_path=None):
    if output_path is None:
        output_path = input_path

    with open(input_path, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)

    print(f"Done : {input_path}")

folder_path = 'output_json'

for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        full_path = os.path.join(folder_path, filename)
        decode_unicode_in_json(full_path)
