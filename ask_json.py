import requests

owner = "lan-ensad"
repo = "Environmental_Product_Declarations"
path = "labelingsustainability/output_json" #labelingsustainability | holcimus | environdec
base_raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{path}/"

api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
response = requests.get(api_url)
files = response.json()

for file in files:
    if file["name"].endswith(".json"):
        raw_url = base_raw_url + file["name"]
        json_data = requests.get(raw_url).json()
        # print(f"{file['name']} loaded, keys: {list(json_data.keys())}")
        try:
            print(f"{json_data['epd_metadata']['period_of_validity']}")
        except:
            print(f"{file['name']} no key found")
