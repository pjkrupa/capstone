from setup_parser import get_parser
from settings import Settings, Result
import psycopg2
import getpass
from llm_client import get_response
from llm_tools import validate_yaml, get_function
from database import make_db_string, make_tables, save_response, row_count, pass_count
from validation import json_validator, tool_calls
import sys

settings = Settings()
parser = get_parser()



if __name__ == "__main__":

    args = parser.parse_args()
    args_dict = {k: v for k, v in vars(args).items() if v is not None}
    settings = Settings().model_copy(update=args_dict)
    yaml_dict = validate_yaml(settings.function_path)
    if not yaml_dict:
        print(f"Validation of {settings.function_path} failed, exiting.")   
        sys.exit(1)
    settings.function = get_function(yaml_dict)

    if settings.model.split("/")[0] != "ollama_chat":
        while True:
            api_key = getpass.getpass("Enter your API key: ")
            if not api_key:
                print("API key cannot be empty, please try again.")
                continue
            else:
                settings.api_key = api_key
                break

    try:
        with open(settings.path) as f:
            prompt  = f.read()
    except Exception as e:
        print(f"There was a problem loading the prompt file: {e}")
        sys.exit(1)
    
    database = make_db_string(settings)
    
    with psycopg2.connect(database) as conn:
        make_tables(conn, settings)

        counter = 0
        for i in range(0,settings.runs):
            result = Result()
            print(f"Sending query {i+1} of {settings.runs}")
            result.raw_response = get_response(settings, prompt)
            if not result.raw_response:
                result.passed_validation = False
                result.validation_errors = '{"model_failure": "true"}'
            elif not tool_calls(settings, result.raw_response):
                result.passed_validation = False
                result.validation_errors = '{"no_tools_call": "true"}'
            else:
                validation_tuple = json_validator(settings, result.raw_response)
                result.passed_validation = validation_tuple[0]
                result.validation_errors = validation_tuple[1]
            
            try:
                save_response(conn=conn, result=result, settings=settings)
                print("Save successful.")
                print(f"Passed Validation? -> {result.passed_validation}")
                counter += 1
            except Exception as e:
                print(f"Something went wrong: {e}")
                continue
        final_row_count = row_count(conn=conn, settings=settings)
        passed = pass_count(conn=conn, settings=settings)
        print(f"Saved {counter} records for the {settings.run_id} run for model {settings.model}.")
        print(f"There are a total of {final_row_count} rows for the {settings.model} on the {settings.run_id} run.")
        print(f"{passed} responses passed validation.")
        