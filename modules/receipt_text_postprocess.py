import re

def post_process_cleanup(text):
    """
    Clean up text after OCR by applying regex and string replacements.

    Parameters:
    text (str): The text output from OCR.

    Returns:
    str: Cleaned up text.
    """
    
    text = text.replace("Atī.", "Atl.") # common misspelling of "Atl."
    text = text.replace("AtĪ.", "Atl.") # common misspelling of "Atl."
    text = text.replace("Atīl.", "Atl.") # common misspelling of "Atl."
    text = text.replace("At1l.", "Atl.") # common misspelling of "Atl."
    text = text.replace("At1.", "Atl.") # common misspelling of "Atl."
    text = text.replace("ĒUR", "EUR") # EUR gets misspelled as ĒUR
    text = text.replace("EŪR", "EUR")
    text = text.replace("FUR", "EUR")
    text = text.replace("1,gab", "1 gab") # sometimes comma is used instead of space
    text = text.replace("1_gab", "1 gab")


    # replace "O" with "0" in numbers
    text = re.sub(r'(\d)O(\d)', r'\1O\2', text)
    text = re.sub(r'O,(\d)', r'0,\1', text)
    text = re.sub(r'Ž,(\d)', r'2,\1', text)

    # find all misspellings of "Gala cena" with fuzzywuzzy and replace them with "Gala cena"
    gala_cena_misspellings = ["Gala cena", "Gala cema", "Gala cenā", '"Gala cena', "'Gala cena", '\'"Gala cena']
    for misspelling in gala_cena_misspellings:
        text = text.replace(misspelling, "Gala cena")

    text = text.replace("” Gala cena", " Gala cena")

    return text

# text = "Atī. O,71 EUR"
# print(text)
# text = post_process_cleanup(text)
# print(text)