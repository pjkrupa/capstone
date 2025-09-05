from settings import Settings
import yaml
import jsonschema, json
from jsonschema import Draft7Validator

def build_answer_schema(settings: Settings):
        """
        This function uses the YAML file to build a JSON schema that includes the enum values for validating the LLM-produced JSON
        """
        
        with open(settings.function_path, "r") as f:
             yaml_text = f.read()

        yaml_dict = yaml.safe_load(yaml_text)
        
        schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
    }

        fields = yaml_dict.get("fields", [])

        for field in fields:

            if field["name"] == "function_name":
                continue

            if field["name"] == "function_description":
                continue 

            name = field["name"]

            prop_attrs = {k: v for k, v in field.items() if k not in ("name")}
            schema["properties"][name] = prop_attrs
            schema["required"].append(name)
        
        return schema

def json_validator(settings: Settings, raw_response: str):
    json_schema = build_answer_schema(settings)
    raw_response = json.loads(raw_response)
    test_response = raw_response['choices'][0]['message']['tool_calls'][0]['function']['arguments']
    data = json.loads(test_response)

    validator = Draft7Validator(json_schema)
    errors = list(validator.iter_errors(data))

    if not errors:
         return True, None
    else:
        errors_json = {}
        for e in errors:
            key = ".".join(str(p) for p in e.path) or "_root_"
            errors_json[key] = {
            "message": e.message,
            "validator": e.validator,
            "validator_value": e.validator_value,
            }
        errors_json = json.dumps(errors_json, indent=2)
        return False, errors_json
    
def tool_calls(settings: Settings, raw_response: str) -> bool:
    raw_response = json.loads(raw_response)
    return bool(raw_response['choices'][0]['message']['tool_calls'])