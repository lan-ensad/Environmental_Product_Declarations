import tiktoken
from pathlib import Path 

THRESHOLD = 70000
MODEL = "gpt-4o"

def count_tokens_in_file(file_path, model="gpt-4o"):
    enc = tiktoken.encoding_for_model(model)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    num_tokens = len(enc.encode(content))
    print(f"{file_path} contient environ {num_tokens} tokens.")
    return num_tokens

def scan_directory_for_tokens(directory_path, threshold=THRESHOLD, model=MODEL):
    directory = Path(directory_path)
    for file_path in directory.glob("*.txt"):
        num_tokens = count_tokens_in_file(file_path, model)
        if num_tokens > threshold:
            print(f"{file_path.name} : {num_tokens} tokens (Over {threshold})")
        else:
            print(f"{file_path.name} : {num_tokens} tokens")

scan_directory_for_tokens("labelingsustainability/ocr_output")
