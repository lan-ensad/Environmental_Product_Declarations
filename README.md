This repo contains an easy tool to scrap edp file from three sources.

## Dependencies

`pip install -r requirements.txt`

Be sure to `playwright install` before launch scraping script.

## Downloding PDF

- `environdec/` https://environdec.com/library

    - first `scrap_urls.py` to refresh the `urls.json`
    - then you can run `download_pdf.py` wich referes to the `urls.json`. It will refresh the pdf files in `docs/`.

- `holciumus/` https://www.holcim.us/technical-specifications

    just run `download_pdf.py` to refresh the pdf files in `docs/`

- `labelingsustainability/` https://www.labelingsustainability.com/holcim-epds

    just run `download_pdf.py` to refresh the pdf files in `docs/`

Download files about Holcim but can be modified with any.

## OCR sources

`ocrisation.py` will check the folder `docs/` and generate raw text in `ocr_output`. You can adjust all parameters try to have the best raw file.

## Resume with LLM

Use `txt_to_json.py` with an API key (Open AI in this exemple). It will generate a resume for each file in `ocr_output` folder. If the resume is not accurate, you can juste delete it, change some parameters (temperature or prompt for exemple) and relaunch the script. It will first check is the file in `ocr_output` already exist, if not it will send the API request.

## Cleaning

It could be some unicode caracter artefact. Launch `clean_unicode.py` it will all json files in the folder_path to clean it. 

## Warning

Be sure to evaluate the cost of the API request before to proceed.