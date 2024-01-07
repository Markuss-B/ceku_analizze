import pytesseract
import os
import cv2
import pdf2image
from rich.progress import Progress
from modules.receipt_image_preproces import preprocess_image, detect_lines, segment_image

# # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# # Example usage

# options = "--psm 4 -l lav"
# receipt = "receipts/receipt1.jpg"

# text = pytesseract.image_to_string(receipt, config=options)

# print(text)

def scan_receipt(receipt_path):
    ''' 
    Extracts text from receipt image using pytesseract

    Parameters:
        receipt_path (str): path to receipt image

    Returns:
        text (str): text extracted from receipt image

    Raises:
        FileNotFoundError: if receipt_path is not a valid path
    '''
    try :
        os.path.isfile(receipt_path)
    except FileNotFoundError:
        print(f"File {receipt_path} not found")
        return None

    if receipt_path.endswith('.jpg'):
        receipt_img = cv2.imread(receipt_path)
    elif receipt_path.endswith('.pdf'):
        receipt_img = pdf2image.convert_from_path(receipt_path)[0]
    else:
        print(f"File {receipt_path} is not a valid image or pdf file")
        return None

    # Segmenting the image didn't help improve ocr accuracy
    # Preprocess image
    preprocessed_img = preprocess_image(receipt_img)
    # Detect lines
    detected_lines = detect_lines(preprocessed_img)
    # Segment image
    image = cv2.imread(receipt_path)
    segments = segment_image(image, detected_lines)

    # Apply OCR to each segment
    options = "--psm 4 -l lav"
    text = ""
    i = 0
    for segment in segments:
        text += "Segment " + pytesseract.image_to_string(segment, config=options) + "\n"
        # # show text and image
        # text = pytesseract.image_to_string(segment, config=options) + "\n"
        # print(text)
        # cv2.imshow('image', segment)
        # cv2.waitKey(0)

    # options = "--psm 4 -l lav"
    # text = pytesseract.image_to_string(receipt_path, config=options)

    return text


def scan_multiple_receipts(directory_path):
    '''
    Extracts text from all receipt images in a directory

    Parameters:
        directory_path (str): path to directory containing receipt images

    Returns:
        extracted_texts (dict): dictionary of text extracted from receipt images where key is the image name and value is the text

    Raises:
        FileNotFoundError: if directory_path is not a valid path
    '''

    extracted_texts = {}

    try:
        os.listdir(directory_path)
    except FileNotFoundError:
        print(f"Directory {directory_path} not found")
        return extracted_texts

    files = [f for f in os.listdir(directory_path) if f.endswith('.jpg') or f.endswith('.pdf')]

    if len(files) == 0:
        print("No receipt images found in directory " + directory_path)
        return extracted_texts

    with Progress() as progress:
        task = progress.add_task("Extracting text from receipts...", total=len(files))

        for file in files:
            image_path = os.path.join(directory_path, file)
            text = scan_receipt(image_path)
            filename = os.path.splitext(file)[0]
            extracted_texts[filename] = text

            progress.update(task, advance=1)
    
    return extracted_texts

def write_receipt_text_to_file(receipt_text, file_path):
    '''
    Writes receipt text to a new file

    Parameters:
        receipt_text (str): text extracted from receipt image
        file_path (str): path to new file
    '''
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(receipt_text)

def write_receipts_texts_to_files(extracted_texts, directory_path):
    '''
    Writes receipt texts to new files

    Parameters:
        extracted_texts (dict): dictionary of text extracted from receipt images where key is the image name and value is the text
        directory_path (str): path to directory where new files will be created
    '''
    try:
        os.listdir(directory_path)
    except FileNotFoundError:
        print(f"Directory {directory_path} not found")
        return False

    for filename, text in extracted_texts.items():
        file_path = os.path.join(directory_path, filename + '.txt')
        write_receipt_text_to_file(text, file_path)
    
    return True

# # # test
# # directory_path = "receipts"
# # extracted_texts = extract_text_from_receipts(directory_path)
# # print(extracted_texts.keys())

# # # # test
# # receipt_path = "receipt_images/receipt1.jpg"
# # text = extract_text_from_receipt(receipt_path)
# # # print(text)
# # save_path = "data/receipt_texts/ocr/receipt1.txt"
# # write_receipt_text_to_file(text, save_path)