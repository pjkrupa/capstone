import argparse

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", 
        "--model",
        required=False, 
        help="Name of the API and the model to be used. Format is \"api-name/model-name\". For example: openai/gpt-4o. Default is ..."
        )
    parser.add_argument(
        '-p',
        '--path',
        required=True,
        help='Path to the text file where the test prompt is saved.',
    )
    parser.add_argument(
        '-r',
        '--runs',
        type=int,
        required=True,
        help='Number of times you want to run the test query.',
    )
    parser.add_argument(
        '-i',
        '--run_id',
        type=str,
        required=True,
        help='ID for this particular run so you can identify it later.'
    )
    return parser