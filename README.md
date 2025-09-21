This is a tool to test how accuratly a particular LLM uses a JSON schema to extract information from unstructured data. To use this tool, you need:

1. A piece of test data (a text file)
2. A YAML file indicating the information you want to extract from the test data.
3. A PostgreSQL database where the results will be saved
4. Access to an LLM API (have your key ready)

The YAML file should look like this:

    fields:
  - name: function_name
    type: string
    description: "populate_patient_data"
  - name: function_description
    type: string
    description: "A JSON schema to be populated with information extracted from a medical examination record"
  - name: medical_record_number
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
    ...

Or: 
    python3 main.py \
        -p sample_medical_record.txt \
        -r 4 \
        -i test_a \
        -f patient_record_a.yaml \
        -m ollama_chat/llama3.1:8b

The `.env` file sets the variables for the PostgreSQL database. The CLI parameters can, alternatively, be set in the `.env` file.

    export OLLAMA_API_BASE="http://inference-gpu-droplet:11434"

    python3 main.py --path sample_medical_record.txt --runs 2 --run_id base --function patient_record.yaml

    openai/gpt-5-nano
    ollama_chat/llama3:8b
    ollama_chat/llama3.3:70b
    ollama_chat/command-r-plus:104b


last two model runs:
python3 main.py --path sample_medical_record.txt --runs x --run_id test_g --function patient_record.yaml -m ollama/command-r-plus:104b
python3 main.py --path sample_medical_record.txt --runs x --run_id test_h --function patient_record.yaml -m ollama/llama3.3:70b
python3 main.py \
    --path sample_medical_record.txt \
    --runs 2 \
    --run_id test_j \
    --function patient_record.yaml \
    --model ollama_chat/gpt-oss:120b

run locally:
python3 main.py \
    --path sample_medical_record.txt \
    --runs 3 \
    --run_id base \
    --function patient_record_a.yaml \
    --api_base http://localhost:11434 \
    --model ollama_chat/llama3.1:8b

b runs:
python3 main.py \
    --path sample_medical_record.txt \
    --runs 4 \
    --run_id test_b \
    --function patient_record_b.yaml \
    -m anthropic/claude-sonnet-4-20250514

python3 main.py \
    --path sample_medical_record.txt \
    --runs 1000 \
    --run_id test_b \
    --function patient_record_b.yaml \
    -m openai/gpt-4o

python3 main.py \
    --path sample_medical_record.txt \
    --runs 4 \
    --run_id test_b \
    --function patient_record_b.yaml \
    -m openai/gpt-5-nano

with ollama, rented GPU:
python3 main.py \
    --path sample_medical_record.txt \
    --runs 76 \
    --run_id test_e \
    --function patient_record_a.yaml \
    -m ollama/llama3.3:70b

redo local 3060 llama3.1 run with ollama_chat: ollama_chat/llama3.1:8b

python3 main.py \
    --path sample_medical_record.txt \
    --runs 4 \
    --run_id test_a \
    --function patient_record_a.yaml \
    -m ollama_chat/llama3.1:8b