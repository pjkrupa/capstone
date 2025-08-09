from litellm import completion
from settings import Settings
from pathlib import Path

def get_response(settings: Settings, prompt: str) -> str:
    
    function_name = Path(settings.function_path).stem
    tools = [settings.function]
    messages = [
    {"role": "user", "content": prompt}
    ]

    response = completion(
        model=settings.model,
        tools=tools,
        api_key=settings.api_key,
        messages=messages,
        stream=False,
        tool_choice={
            "type": "function",
            "function": {
                "name": function_name
                }
            }
    )

    print(f"From before JSON conversion: {type(response)}")
    raw_response = response.model_dump_json()
    print(f"From after JSON conversion: {type(raw_response)}")
    return raw_response


# logic for parsing the raw response later:
# tool_calls = response['choices'][0]['message'].get('tool_calls', [])
# if not tool_calls:
#    raise ValueError("No tool call was returned by the model.")
    
# arguments_json = tool_calls[0]['function']['arguments']