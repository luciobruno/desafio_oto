import chardet
import pandas as pd
from unidecode import unidecode
import re
import os

def detect_encoding(input_file):
    with open(input_file, "rb") as f:
        result = chardet.detect(f.read(10000))
    print(f"Encoding detectado: {result['encoding']}")
    return result["encoding"]

def normalize_city(city):
    if pd.isna(city):
        return ""
    city = unidecode(city)
    city = city.upper()
    city = re.sub(r"[^A-Z0-9\s-]", "", city)
    return city.strip()

def clean_phone(phone):
    if pd.isna(phone):
        return ""
    return re.sub(r"\D", "", str(phone))

def process_csv(input_file, output_file=None, chunksize=1000):
    if not output_file:
        name, ext = os.path.splitext(input_file)
        output_file = f"{name}_clean{ext}"

    encoding = detect_encoding(input_file)

    chunks = pd.read_csv(input_file, chunksize=chunksize, encoding=encoding)
    first_chunk = True
    chunk_id = 1
    total_rows = 0

    for chunk in chunks:
        total_rows += len(chunk)

        chunk["CITY"] = chunk["CITY"].str.strip()
        chunk["CITY_ASCII"] = chunk["CITY"].apply(normalize_city)
        chunk["PHONE"] = chunk["PHONE"].apply(clean_phone)

        chunk.to_csv(
            output_file,
            mode="w" if first_chunk else "a",
            index=False,
            encoding="utf-8",
            header=first_chunk
        )
        print(f"Chunk {chunk_id} processado e salvo ({len(chunk)} linhas)")
        first_chunk = False
        chunk_id += 1

    print(f"\n{total_rows} linhas salvas em {output_file}")

if __name__ == "__main__":
    process_csv("natal2025.csv")