import os
import re
import json

def fix_json_format(line):
    # Remove trailing commas from lists and dictionaries
    line = re.sub(r',\s*([\]}])', r'\1', line)
    # Ensure property names are enclosed in double quotes
    line = re.sub(r'([{\s])([a-zA-Z0-9_]+)(\s*):', r'\1"\2"\3:', line)
    return line

def fix_and_validate_json_file(filepath):
    fixed_lines = []
    with open(filepath, 'r') as file:
        for line in file:
            fixed_line = fix_json_format(line.strip())
            fixed_lines.append(fixed_line)
    
    # Combine fixed lines into a single JSON string and validate it
    try:
        fixed_json_string = ' '.join(fixed_lines)
        json.loads(fixed_json_string)  # This will raise an exception if the JSON is invalid
        return '\n'.join(fixed_lines)
    except json.JSONDecodeError as e:
        print(f"Error in file {filepath}: {e}")
        return None

def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            fixed_content = fix_and_validate_json_file(filepath)
            if fixed_content:
                with open(filepath, 'w') as file:
                    file.write(fixed_content)
                print(f"Fixed file: {filename}")

# Process the directories
train_ann_dir = r"C:\Users\BQ Team 4\Desktop\OCR Finetuning\example_json"
#val_ann_dir = r"C:\Users\BQ Team 4\Desktop\OCR Finetuning\VAL_anno"

process_directory(train_ann_dir)
#process_directory(val_ann_dir)
