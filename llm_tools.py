import yaml
from pathlib import Path

def validate_yaml(yaml_location: str):

    valid_types = ["string", "number", "integer", "object", "array", "boolean", "null"]
    try:
        with open(yaml_location, "r") as f:
            yaml_text = f.read()
    except FileNotFoundError:
        print(f"File not found: {yaml_location}")
        return False
    except PermissionError:
        print(f"Permission denied: {yaml_location}")
        return False
    except IsADirectoryError:
        print(f"Path is a directory, not a file: {yaml_location}")
        return False
    except OSError as e:
        print(f"OS error when opening file: {e}")
        return False
    
    try:
        yaml_dict = yaml.safe_load(yaml_text)
    except yaml.YAMLError as e:
        print(f"YAML parsing error: {e}")
        return False
    
    fields = yaml_dict.get("fields", [])
    for field in fields:
        if field["type"] not in valid_types:
            print(f"Invalid type: {field["type"]}. All types must be one of the following: {valid_types}.")
            print(f"Please edit {yaml_location} and try again.")
            return False
    return yaml_dict
        
def get_function(yaml_dict: dict) -> dict:
    """
    Opens the YAML file for query tool and converts it to a JSON schema. Returns it as a dictionary to be added to a "tool" function.
    """

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
            function_name = field.get("description", "").strip()
            continue

        if field["name"] == "function_description":
            function_description = field.get("description", "").strip()
            continue 

        name = field["name"]

        prop_attrs = {k: v for k, v in field.items() if k not in ("name", "value", "enum")}
        schema["properties"][name] = prop_attrs
        schema["required"].append(name)
    
    print(schema)

    final_function = {
        "type": "function",
        "function": {
    "name": function_name,
    "description": function_description,
    "parameters": schema
    }
    }

    return final_function

tools = [
    {
        "type": "function",
        "function": {
            "name": "populate_patient_record",
            "description": "Populate a patient record with medical details based on user input.",
            "parameters": {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "title": "PatientRecord",
                "type": "object",
                "properties": {
                    "medical_record_number": {"type": "string"},
                    "patient_name": {"type": "string"},
                    "age": {"type": "integer", "minimum": 0},
                    "weight": {"type": "number", "minimum": 0},
                    "blood_pressure": {
                        "type": "string",
                        "pattern": "^\\d{2,3}/\\d{2,3}$"
                    },
                    "date_admitted": {"type": "string", "format": "date"},
                    "date_discharged": {"type": "string", "format": "date"},
                    "attending_physician": {"type": "string"},
                    "diagnosis": {"type": "string"},
                    "other_diagnosis": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "current_medications": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": [
                    "medical_record_number",
                    "name",
                    "age",
                    "date_admitted",
                    "attending_physician",
                    "diagnosis"
                ]
            }
        }
    }
]
