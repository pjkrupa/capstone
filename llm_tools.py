import yaml
from pathlib import Path

def yaml_to_json_schema(yaml_location: str) -> dict:
    """
    Opens the YAML file for query tool and converts it to a JSON schema. Returns it as a dictionary to be added to a "tool" function.
    """

    try:
        with open(yaml_location, "r") as f:
            yaml_text = f.read()
    except Exception as e: 
        print(f"Couldn't open the YAML file: {e}")
    

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
        name = field["name"]
        # Copy all keys except 'name' as schema attributes for this property
        prop_attrs = {k: v for k, v in field.items() if k != "name"}

        schema["properties"][name] = prop_attrs

        # Add to required if explicitly set or default to required (optional tweak)
        # Here we add fields that don't have 'optional: true' (if you want)
        # For now, assume all fields required, or add logic as you want
        schema["required"].append(name)

    return schema

def get_function(yaml_location: str) -> dict:
    converted_yaml = yaml_to_json_schema(yaml_location)
    function_name = Path(yaml_location).stem

    final_function = {
        "type": "function",
        "function": {
    "name": function_name,
    "description": "a JSON schema to be populated based on the user input in the prompt.",
    "parameters": converted_yaml
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
