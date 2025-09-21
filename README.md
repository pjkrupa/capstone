This is a tool to test how accuratly a particular LLM uses a JSON schema to extract information from unstructured data. To use this tool, you need:

1. A piece of test data (a text file)
2. A YAML file indicating the information you want to extract from the test data.
3. A PostgreSQL database where the results will be saved
4. Access to an LLM API (have your key ready)

The YAML file should look like this:

    fields:
    name: function_name
    type: string
    description: "populate_patient_data"
    name: function_description
    type: string
    description: "A JSON schema to be populated with information extracted from a medical examination record"
    name: medical_record_number
    type: string
    description: "Unique patient medical record identifier"
    enum: ["123456789"]

For the first two fields, enter the name of the function and a description. After that, you can include as many fields as you want, of any valid JSON type. Be sure to put include `enum: ["value"]` for each field, as that is the "answer" that will be used to validate the model's response.

You need a YAML file like this for each piece of test data. So if you want to run this test against 10 different invoices (for example), you need a YAML file like this for each invoice with the right "answers" you want the model to return.

For `runs`, the recommendation is to run the query some statistically-significant number of times to get an accurate picture of the kinds of errors the model can make for the test data and how frequently it makes them. 

To use this tool, from the terminal in the root directory:

    python3 main.py \
        --path [path] \
        --runs [number of runs] \
        --run_id [unique name for this run] \
        --model [model name. default is openai/gpt-4o] \
        --function [path]

So, for example:

    python3 main.py \
        --path sample_medical_record.txt \
        --runs 4 \
        --run_id test_a \
        --function patient_record_a.yaml \
        --model ollama_chat/llama3.1:8b

The CLI parameters can, alternatively, be set in the `.env` file. The `.env` file also sets the variables for the PostgreSQL database.