To use this tool, from the terminal in the root directory:
    python3 main.py --path [path] --runs [number of runs] --run_id [unique name for this run] --model [model name. default is openai/gpt-4o] --function [path]
    ...

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
    --model ollama_chat/llama3:8b

b runs:
python3 main.py \
    --path sample_medical_record.txt \
    --runs 4 \
    --run_id test_b \
    --function patient_record_b.yaml \
    -m anthropic/claude-sonnet-4-20250514

python3 main.py \
    --path sample_medical_record.txt \
    --runs 4 \
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
    --runs 4 \
    --run_id test_b \
    --function patient_record_b.yaml \
    -m ollama_chat/llama3.3:70b