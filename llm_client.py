from litellm import completion
from settings import Settings
from pathlib import Path

def get_response(settings: Settings, prompt: str) -> str:
    
    tools = [settings.function]
    function_name = settings.function["function"]["name"]
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

    raw_response = response.model_dump_json()
    
    return raw_response


# logic for parsing the raw response later:
# tool_calls = response['choices'][0]['message'].get('tool_calls', [])
# if not tool_calls:
#    raise ValueError("No tool call was returned by the model.")
    
# arguments_json = tool_calls[0]['function']['arguments']