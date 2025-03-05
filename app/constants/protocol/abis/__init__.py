from pathlib import Path
import json


def read(contract):
    file_path = Path(__file__).parent / f"{contract}.json"

    with file_path.open("r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data
