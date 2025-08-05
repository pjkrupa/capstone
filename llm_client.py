from litellm import completion
from settings import Settings
from llm_tools import tools
import json

def get_response(settings: Settings, prompt: str) -> str:
    
    messages = [
    {"role": "user", "content": prompt}
    ]

    response = completion(
        model=settings.model,
        tools=tools,
        api_key=settings.api_key,
        messages=messages,
        tool_choice={
            "type": "function",
            "function": {
                "name": settings.tool
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