from jsonschema import validate
import json

with open("openvas_config.schema", 'r') as json_schema, \
        open("./../config.json", 'r') as json_config:
    schema = json.load(json_schema)
    config = json.load(json_config)

    validate(instance=config, schema=schema)