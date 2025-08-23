import litellm
from litellm import completion
from settings import Settings
from pathlib import Path
import time

def get_response(settings: Settings, prompt: str) -> str:
    
    litellm.set_verbose = False
    tools = [settings.function]
    function_name = settings.function["function"]["name"]
    messages = [
    {"role": "user", "content": prompt}
    ]

    max_retries = 5
    backoff = 2

    for attempt in range(1, max_retries+1):
        try:
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
        except Exception as e:
            message = str(e).lower()
            if "rate limit" in message or "429" in message:
                if attempt == max_retries:
                    raise
                print(f"[WARN] Rate limited. Attempt {attempt}/{max_retries}. Retrying in {backoff} seconds...")
                time.sleep(backoff)
                backoff *= 2
            else:
                raise


# logic for parsing the raw response later:
# tool_calls = response['choices'][0]['message'].get('tool_calls', [])
# if not tool_calls:
#    raise ValueError("No tool call was returned by the model.")
    
# arguments_json = tool_calls[0]['function']['arguments']