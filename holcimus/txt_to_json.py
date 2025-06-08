import os
import json
from pathlib import Path
from openai import OpenAI
import time

client = OpenAI(api_key="API_KEY")

txt_folder = Path("ocr_output")
output_folder = Path("output_json")
output_folder.mkdir(exist_ok=True)

instruction_system = """You are a highly skilled assistant specializing in the analysis of Environmental Product Declarations (EPDs). 
Your task is to extract structured, relevant data from the raw content of a text file and organize it into the following JSON schema:

{
  "epd_metadata": {...},
  "product_description": {...},
  "lca_information": {...},
  "transport_and_installation": {...},
  "end_of_life": {...},
  "carbon_emission_context": {...},
  "recycled_materials_handling": {...},
  "additional_info": {...}
}

Guidelines:
- Do not infer or fabricate any data.
- If a section is missing, incomplete, or not explicitly stated, use `null` or `{}` as appropriate.
- Preserve the original structure and factual integrity of the source content.
- Output a **single, valid JSON object** only — without comments, explanation, or extra text.
"""

def extract_json_from_txt(txt_path):
    with open(txt_path, "r", encoding="utf-8") as file:
        content = file.read()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": instruction_system},
            {"role": "user", "content": content}
        ],
        temperature=0, # try to avoid hallucinations
    )

    output = response.choices[0].message.content

    try:
        json_obj = json.loads(output)
    except json.JSONDecodeError:
        import re
        match = re.search(r'\{[\s\S]*\}', output)
        if match:
            json_obj = json.loads(match.group(0))
        else:
            raise ValueError(f"json error : {txt_path.name}")

    return json_obj

for txt_file in txt_folder.glob("*.txt"):
    output_path = output_folder / f"{txt_file.stem}.json"
    if output_path.exists():
        print(f"Already existing : {txt_file.name} -> ignore")
        continue

    try:
        print(f"prompting : {txt_file.name}")
        data = extract_json_from_txt(txt_file)
        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(data, out, indent=2)
        print(f"json generated : {output_path.name}\nWaiting before next API request...")
        time.sleep(45) # avoid limit TPM for chat-gpt API
    except Exception as e:
        print(f"error {txt_file.name} : {e}")

