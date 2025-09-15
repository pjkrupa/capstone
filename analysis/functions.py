from pandas import DataFrame
import numpy as np

def preprocess_failures(df: DataFrame) -> DataFrame:
    """
    Takes the raw df and returns a df with:
        1. just the records that failed validation
        2. a column for each field that failed validation
        3. a tally count in those columns to indicate how validation failed on that row
    """
    failure_types = []
    
    # grabs the fields on which the validation failed
    def _collect_failures(x):
        if x:
            for key in x.keys():
                if key not in failure_types:
                    failure_types.append(key)
    
    # tallies failures in the appropriate column
    def _tally_failure(row):
        for key in row['validation_errors'].keys():
            if key in row.index:
                row[key] = 1
        return row
    
    # makes a copy of the df with only the failed records
    failures_df = df[df['passed_validation'] == False].copy()
    
    # applies the helper function to the df copy
    failures_df['validation_errors'].apply(_collect_failures)
    
    # makes a column for each field failure, sets it to 0
    for item in failure_types:
        failures_df[item] = 0
    
    # adds a tally mark in the correct column for each field failure
    failures_df = failures_df.apply(_tally_failure, axis=1)
    
    return failures_df

def sum_failures(df):
    group_cols = ['run_id', 'model']
    exclude_cols = [
        'id', 
        'run_id', 
        'model', 
        'raw_response', 
        'passed_validation', 
        'validation_errors',
        'timestamp', 
        'duration'
        ]
    df_cols = df.columns
    sum_cols = [x for x in df_cols if x not in exclude_cols]
    df_failures_analysis = (
        df.groupby(group_cols, as_index=False)[sum_cols]
        .sum()
    )
    df_final = df_failures_analysis.rename(columns={col: f"{col}_failure" for col in sum_cols})
    return df_final

def show_run_stats(df):
    model_costs = {
        "openai/gpt-4o": {
            "prompt": 5.0,
            "cached": 2.50,
            "completion": 20.0
        },
        "openai/gpt-5-nano": {
            "prompt": 0.050,
            "cached": 0.005,
            "completion": 0.40
        },
        "anthropic/claude-sonnet-4-20250514": {
            "prompt": 3.0,
            "cached": 3.0,
            "completion": 15.0
        }
    }
    sample_size = df.shape[0]
    pass_percentage = df['passed_validation'].mean()
    pass_percentage = round(pass_percentage*100, 2)
    run_time = df["timestamp"].max() - df["timestamp"].min()

    try:
        cached_tokens = df["raw_response"].apply(lambda x: x["usage"]["prompt_tokens_details"]["cached_tokens"]).sum()
    except Exception as e:
        cached_tokens = 0
    try:
        prompt_tokens = df["raw_response"].apply(lambda x: x["usage"]["prompt_tokens"]).sum()
    except Exception as e:
        prompt_tokens = 0
    try:
        completion_tokens = df["raw_response"].apply(lambda x: x["usage"]["completion_tokens"]).sum()
    except Exception as e:
        completion_tokens = 0
    model = df["model"].iloc[0]
    run_id = df["run_id"].iloc[0]
    
    if df['model'].iloc[0].split("/")[0] == "ollama_chat" or "ollama":
        run_cost = 0
    else:
        run_cost = round(
            ((prompt_tokens-cached_tokens) / 1000000 * model_costs[model]["prompt"]) + 
            (cached_tokens / 1000000 * model_costs[model]["cached"]) +
            (completion_tokens / 1000000 * model_costs[model]["completion"]), 
            2
            )
    
    models = show_unique(df, column='model')
    models = models.tolist()
    print(f"Run ID: {run_id}")
    print(f"Models used: {models}")
    print(f"Number of requests: {sample_size}")
    print(f"Estimated duration of the entire run: {run_time}")
    print(f"Validated requests: {pass_percentage}%")
    print(f"The run used {prompt_tokens:,} prompt tokens and {completion_tokens:,} completion tokens.")
    print(f"Estimated cost of the run: US${run_cost}")


def show_failures(df):
    regular_columns = [
        'id', 
        'run_id', 
        'model', 
        'raw_response', 
        'passed_validation', 
        'validation_errors', 
        'timestamp',
        'duration'
    ]
    
    all_columns = df.columns.to_list()
    
    for item in all_columns:
        if item not in regular_columns:
            df[item] = df[item].fillna(0)
            count = df[item].sum()
            print(f"{item:<30} failures: {count:>5}")

def show_unique(df: DataFrame, column: str):
    sorted = df[column].unique()
    sorted = np.sort(sorted)
    return sorted