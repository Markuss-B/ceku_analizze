import os
from difflib import SequenceMatcher

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def compare_texts_similarity(ocr_text, manual_text):
    # Using SequenceMatcher to calculate similarity
    matcher = SequenceMatcher(None, ocr_text, manual_text)
    return matcher.ratio()

def compare_receipt_ocr_file_to_manual_file(filename):
    '''
    Compares OCR-generated text file to manually transcribed text file.
    OCR-generated in the 'data/receipt_texts/ocr' directory and manually transcribed in the 'data/receipt_texts/manual' directory.

    Parameters:
        filename (str): name of file to compare
    '''
    ocr_directory = 'data/receipt_texts/ocr'  # Directory containing OCR-generated text files
    manual_directory = 'data/receipt_texts/manual'  # Directory containing manually transcribed text files

    ocr_text_path = os.path.join(ocr_directory, filename)
    manual_text_path = os.path.join(manual_directory, filename)

    if not os.path.exists(manual_text_path):
        print(f"No manual transcription found for {filename}")
        return
    
    if not os.path.exists(ocr_text_path):
        print(f"No OCR-generated text found for {filename}")
        return
    
    ocr_text = read_file(ocr_text_path)
    manual_text = read_file(manual_text_path)

    similarity = compare_texts_similarity(ocr_text, manual_text)
    print(f"Similarity for {filename}: {similarity:.2f}")

    

