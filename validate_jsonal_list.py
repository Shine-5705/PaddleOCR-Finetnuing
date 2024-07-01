import os
import json

def escape_backslashes(json_data):
    # Correct the backslashes in the filename path
    if 'filename' in json_data:
        json_data['filename'] = json_data['filename'].replace('\\', '\\\\')
    return json_data

def validate_json_structure(json_data, base_image_dirs):
    try:
        # Check for mandatory fields
        required_keys = ['filename', 'split', 'imgid', 'html']
        for key in required_keys:
            if key not in json_data:
                print(f"Error: Missing mandatory field '{key}' in {json_data}")
                return False

        # Check if the image file exists in any of the base directories
        image_exists = any(os.path.exists(os.path.join(base_dir, json_data['filename'].replace('\\\\', '\\'))) for base_dir in base_image_dirs)
        if not image_exists:
            print(f"Error: Image file {json_data['filename']} does not exist in any of the specified directories")
            return False

        # Validate html structure and cells
        html_data = json_data['html']
        if 'structure' not in html_data or 'cells' not in html_data:
            print(f"Error: Missing 'structure' or 'cells' in 'html' of {json_data}")
            return False

        # Check structure tokens
        if 'tokens' not in html_data['structure']:
            print(f"Error: Missing 'tokens' in 'structure' of 'html' in {json_data}")
            return False

        # Validate each cell
        for cell in html_data['cells']:
            if 'tokens' not in cell or 'bbox' not in cell:
                print(f"Error: Missing 'tokens' or 'bbox' in a cell of {json_data}")
                return False

        return True

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def validate_jsonl_file(jsonl_file, base_image_dirs):
    all_valid = True
    try:
        with open(jsonl_file, 'r') as file:
            for line in file:
                try:
                    json_data = json.loads(line.strip())
                    if not validate_json_structure(json_data, base_image_dirs):
                        all_valid = False
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON line: {e}")
                    all_valid = False
    except FileNotFoundError:
        print(f"File not found: {jsonl_file}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
    if all_valid:
        print(f"All entries in {jsonl_file} are valid.")
    else:
        print(f"Some entries in {jsonl_file} have errors.")
    return all_valid

def combine_and_fix_json_files(directories, output_file):
    with open(output_file, 'w') as outfile:
        for directory in directories:
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    filepath = os.path.join(directory, filename)
                    with open(filepath, 'r') as infile:
                        json_data = json.load(infile)
                        json_data = escape_backslashes(json_data)
                        json_line = json.dumps(json_data)
                        outfile.write(json_line + '\n')

# Example usage
base_image_dirs = [
    r'C:\Users\BQ Team 4\Desktop\OCR Finetuning\TRAIN_img',
    r'C:\Users\BQ Team 4\Desktop\OCR Finetuning\VAL_img'
]
json_directories = [
    r'C:\Users\BQ Team 4\Desktop\OCR Finetuning\TRAIN_ann',
    r'C:\Users\BQ Team 4\Desktop\OCR Finetuning\VAL_anno'
]
output_jsonl_file = r'C:\Users\BQ Team 4\Desktop\OCR Finetuning\combined_output2.jsonl'

combine_and_fix_json_files(json_directories, output_jsonl_file)
validate_jsonl_file(output_jsonl_file, base_image_dirs)
