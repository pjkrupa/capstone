from litellm import completion
from llm_tools import tools
import json

def get_response(model: str, prompt: str, api_key: str):
    messages = [
    {"role": "user", "content": prompt}
    ]

    response = completion(
        model=model,
        tools=tools,
        api_key=api_key,
        messages=messages,
        tool_choice="auto",
    )

    

    tool_calls = response['choices'][0]['message'].get('tool_calls', [])
    if not tool_calls:
        raise ValueError("No tool call was returned by the model.")
    
    arguments_json = tool_calls[0]['function']['arguments']

    patient_record = json.loads(arguments_json)
    return patient_record
