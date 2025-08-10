from settings import Settings
import jsonschema, json

def json_validator(settings: Settings, raw_response: dict):
    json_schema = settings.function['function']['parameters']
    raw_response = json.loads(raw_response)
    test_response = raw_response['choices'][0]['message']['tool_calls'][0]['function']['arguments']
    data = json.loads(test_response)

    try:
        jsonschema.validate(instance=data, schema=json_schema)
        return True
    except jsonschema.ValidationError as e:
        print("Validation failed:", e)
        return False
