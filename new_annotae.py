import cv2
import json
import os
import pandas as pd

def annotate_image(image_path):
    image = cv2.imread(image_path)
    image_copy = image.copy()
    annotations = []
    current_annotation = {}

    # Mouse callback function to capture clicks
    def draw_rectangle(event, x, y, flags, param):
        nonlocal current_annotation

        if event == cv2.EVENT_LBUTTONDOWN:
            current_annotation['x1'], current_annotation['y1'] = x, y
            current_annotation['drawing'] = True

        elif event == cv2.EVENT_LBUTTONUP:
            if 'drawing' in current_annotation and current_annotation['drawing']:
                current_annotation['x2'], current_annotation['y2'] = x, y
                annotations.append(current_annotation.copy())
                current_annotation.clear()

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_rectangle)

    while True:
        for annotation in annotations:
            if 'x1' in annotation and 'x2' in annotation and 'y1' in annotation and 'y2' in annotation:
                cv2.rectangle(image_copy, (annotation['x1'], annotation['y1']), (annotation['x2'], annotation['y2']), (0, 255, 0), 2)

        cv2.imshow('image', image_copy)
        key = cv2.waitKey(1) & 0xFF

        # Press 's' to save annotations and exit
        if key == ord('s'):
            break

        # Press 'r' to reset annotations
        elif key == ord('r'):
            annotations.clear()
            image_copy = image.copy()

        # Press 'q' to quit without saving
        elif key == ord('q'):
            annotations = []
            break

    cv2.destroyAllWindows()
    return annotations

def combine_annotations_with_csv(annotations, csv_path, image_path, save_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Create the output structure
    output_data = {
        'filename': os.path.basename(image_path),
        'split': 'train',  # Replace with appropriate split information
        'imgid': 1,  # Replace with appropriate image ID
        'html': {
            'structure': {'tokens': []},
            'cell': []
        }
    }

    for i, annotation in enumerate(annotations):
        if i < len(df):
            text = df.iloc[i].values
            cell_data = {
                'tokens': list(map(str, text)),  # Convert text to tokens
                'bbox': [annotation['x1'], annotation['y1'], annotation['x2'], annotation['y2']]  # Bounding box coordinates
            }
            output_data['html']['cell'].append(cell_data)

    # Save the combined data as JSON
    with open(save_path, 'w') as f:
        json.dump(output_data, f, indent=4)
    print(f'Annotations and extracted text saved to {save_path}')

if __name__ == "__main__":
    image_path = r'example.png'  # Replace with your image path
    csv_path = r'example.csv'  # Replace with your CSV file path
    save_path = 'example.json'  # Path to save annotations JSON file

    if os.path.exists(image_path) and os.path.exists(csv_path):
        annotations = annotate_image(image_path)
        combine_annotations_with_csv(annotations, csv_path, image_path, save_path)
    else:
        print(f'Image file or CSV file not found at {image_path} or {csv_path}')
