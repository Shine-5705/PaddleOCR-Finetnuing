import json
import os

def validate_and_fix_json_structure(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    
    open_braces = 0
    open_brackets = 0
    corrected_lines = []
    
    for line in lines:
        open_braces += line.count('{')
        open_braces -= line.count('}')
        open_brackets += line.count('[')
        open_brackets -= line.count(']')
        corrected_lines.append(line)
    
    # Add missing braces/brackets at the end if needed
    if open_brackets > 0:
        corrected_lines.append(']' * open_brackets + '\n')
    if open_braces > 0:
        corrected_lines.append('}' * open_braces + '\n')

    with open(filepath, 'w') as file:
        file.writelines(corrected_lines)

def fix_trailing_commas_and_quotes(lines):
    corrected_lines = []
    for line in lines:
        line = line.replace("'", '"')  # Ensure proper quotes
        if line.strip().endswith(','):
            line = line.rstrip(',') + '\n'  # Remove trailing commas
        corrected_lines.append(line)
    return corrected_lines

def validate_and_fix_json(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                lines = file.readlines()
            
            # Fix trailing commas and quotes first
            lines = fix_trailing_commas_and_quotes(lines)
            
            with open(filepath, 'w') as file:
                file.writelines(lines)
            
            print(f"Validating and fixing {filepath}")
            validate_and_fix_json_structure(filepath)

# Validate and fix JSON files in the directories
train_ann_dir = r"C:\Users\BQ Team 4\Desktop\OCR Finetuning\TRAIN_ann"
val_ann_dir = r"C:\Users\BQ Team 4\Desktop\OCR Finetuning\VAL_anno"
validate_and_fix_json(train_ann_dir)
validate_and_fix_json(val_ann_dir)
