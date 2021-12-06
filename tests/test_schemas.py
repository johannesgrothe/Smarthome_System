import os
import json
import jsonschema
import urllib.request
import logging


def load_schema(url: str) -> dict:
    print(f"Loading schema from '{url}'")
    logging.info(f"Loading schema from '{url}'")
    data = []
    for line in urllib.request.urlopen(url):
        data.append(line.decode('utf-8'))
    out_json = json.loads("\n".join(data))
    return out_json


def test_json_schemas():
    schema_data = {}
    file_data = {}
    for filename in [x for x in os.listdir("json_schemas") if x.endswith(".json")]:
        with open(os.path.join("json_schemas", filename), "r") as file_p:
            json_data = json.load(file_p)
            file_data[filename] = json_data

    for filename, data in file_data.items():
        if "$schema" in data:
            schema_url = data["$schema"]
            if schema_url not in schema_data:
                loaded_schema = load_schema(schema_url)
                schema_data[schema_url] = loaded_schema
            else:
                loaded_schema = schema_data[schema_url]
            jsonschema.validate(data, loaded_schema)
