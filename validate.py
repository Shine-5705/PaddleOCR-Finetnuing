import json
def validate_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                json.loads(line.strip())
            except json.JSONDecodeError as e:
                print(f"Error in line {line_num}: {e}")
                print(f"Problematic line: {line[:100]}...")  # Print first 100 chars

# Use this function to validate your files
validate_jsonl('example_json\example.json')
#validate_jsonl('combine_train.jsonl')