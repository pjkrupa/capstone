from setup_parser import get_parser
import getpass
from llm_client import get_response

parser = get_parser()


if __name__ == "__main__":

    args = parser.parse_args()

    model = args.model or "openai/gpt-4o"
    path = args.path
    query_n = args.number

    while True:
        api_key = getpass.getpass("Enter your API key: ")
        if not api_key:
            print("API key cannot be empty, please try again.")
            continue
        else:
            break
    
    with open(path) as f:
        prompt  = f.read()

    for i in range(0,query_n):
        print(f"Query {i}")
        llm_response = get_response(model, prompt, api_key)
        print(f"The response is type {type(llm_response)}")
        print(llm_response)