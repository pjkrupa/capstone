from setup_parser import get_parser
from settings import Settings
import psycopg2
import getpass
from llm_client import get_response
from llm_tools import validate_yaml, get_function
from database import make_db_string, make_tables, save_response, row_count
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
            print(f"Sending query {i+1}")
            raw_response = get_response(settings, prompt)
            try:
                save_response(conn=conn, raw_response=raw_response, settings=settings)
                print("Save successful.")
                counter += 1
            except Exception as e:
                print(f"Something went wrong: {e}")
                continue
        final_row_count = row_count(conn=conn, settings=settings)
        print(f"Saved {counter} records for the {settings.run_id} run.")
        print(f"The {settings.run_id} run has a total of {final_row_count} rows.")
        