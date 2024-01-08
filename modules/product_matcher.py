    # 1. Get all products from the receipts
    # 2. Find all products of the same name
    # 3. Find products of the same name but misspelled
    # 4. Print those same name products and their name variants
    # 5. Print products with no name variants
    # 6. Normalize names of the products
from fuzzywuzzy import process
from rich.progress import Progress

def spellcheck_receipts(receipts_dict, standardized_names):
    """
    Spellcheck all products in the receipts.

    Parameters:
    receipts_dict (dict): Dictionary of receipts.
    standardized_names (list): List of standardized product names.

    Returns:
    dict: Dictionary of receipts with spellchecked products.
    """
    with Progress() as progress:
        task = progress.add_task("Spellchecking receipts...", total=len(receipts_dict))
        for receipt in receipts_dict:
            for product in receipt['products']:
                best_match = find_best_match(product['name'], standardized_names)
                if best_match[1] > 80:
                    product['name'] = best_match[0]
                    # if best_match[1] < 90:
                    #     print(product['name'] + ' -> ' + best_match[0] + ' with score ' + str(best_match[1]))
                # else:
                #     print(product['name'] + ' -> ' + 'No match found')
            progress.update(task, advance=1)
    return receipts_dict

def find_best_match(product_name, standardized_names):
    manual_replacements = {
        "Kons. baltās pupiņas Rimi Smart 400/2409'": 'baltas pupinas rimi smart 400g',
        'Melnās olīvas Rimi Basic bez kauliņiem 260g.':'melnas olivas rimi bez kauliniem 350g 150g',
        'Dabīgi gāzēts tējas dz. Sun365 kombūcha 0,5L':'tejas dzer kombucha trad sun365 bio 0 5l',
        'Tomāti Latvijas, kg, 1.ši Līsa':'tomati latvijas kg 1sk',
        'Laims C/48—54, kg 1,29 F':'laims c 48 54 kg',
    }
    if product_name in manual_replacements:
        return [manual_replacements[product_name], 100]
    # preprocess product_name
    product_name = product_name.lower()
    # replace latvian letters with english letters
    lv_let = {
        'ā': 'a',
        'č': 'c',
        'ē': 'e',
        'ģ': 'g',
        'ī': 'i',
        'ķ': 'k',
        'ļ': 'l',
        'ņ': 'n',
        'š': 's',
        'ū': 'u',
        'ž': 'z'
    }
    for letter in product_name:
        if letter in lv_let:
            product_name = product_name.replace(letter, lv_let[letter])

    # remove all non-alphanumeric characters
    product_name = ''.join(e if e.isalnum() else ' ' for e in product_name)


    best_match = process.extractOne(product_name, standardized_names)
    return best_match
