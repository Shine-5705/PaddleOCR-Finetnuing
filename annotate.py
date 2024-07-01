import cv2
import pytesseract
import json
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path according to your Tesseract installation

def preprocess_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Further noise reduction using median blur
    processed_image = cv2.medianBlur(thresh, 3)
    
    return processed_image

def annotate_and_extract_text(image_path, save_path):
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
            with open(save_path, 'w') as f:
                json.dump(annotations, f, indent=4)
            print(f'Annotations saved to {save_path}')
            break

        # Press 'r' to reset annotations
        elif key == ord('r'):
            annotations.clear()
            image_copy = image.copy()

        # Press 'q' to quit without saving
        elif key == ord('q'):
            break

    cv2.destroyAllWindows()

    # Extract text using Tesseract OCR for each annotated bounding box
    extracted_data = {
        'filename': os.path.basename(image_path),
        'split': 'train',  # Replace with appropriate split information
        'imgid': 1,  # Replace with appropriate image ID
        'html': {
            'structure': {'tokens': []},
            'cell': []
        }
    }

    processed_image = preprocess_image(image)

    for annotation in annotations:
        if 'x1' in annotation and 'x2' in annotation and 'y1' in annotation and 'y2' in annotation:
            x1, y1 = annotation['x1'], annotation['y1']
            x2, y2 = annotation['x2'], annotation['y2']
            cropped_image = processed_image[y1:y2, x1:x2]
            extracted_text = pytesseract.image_to_string(cropped_image, config='--psm 6')
            if extracted_text.strip():  # Only add non-empty cells
                cell_data = {
                    'tokens': extracted_text.split(),  # Split text into tokens
                    'bbox': [x1, y1, x2, y2]  # Bounding box coordinates
                }
                extracted_data['html']['cell'].append(cell_data)

    # Optionally, save extracted_data as JSON
    with open(f'{os.path.splitext(image_path)[0]}_annotations.json', 'w') as f:
        json.dump(extracted_data, f, indent=4)
    print(f'Annotations and extracted text saved to {os.path.splitext(image_path)[0]}_annotations.json')

if __name__ == "__main__":
    image_path = r'example.png'  # Replace with your image path
    save_path = 'example.json'  # Path to save annotations JSON file

    if os.path.exists(image_path):
        annotate_and_extract_text(image_path, save_path)
    else:
        print(f'Image file not found at {image_path}')
