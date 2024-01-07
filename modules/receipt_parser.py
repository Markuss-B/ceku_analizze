import re
import os
import datetime
from modules.receipt_text_postprocess import post_process_cleanup

def extract_store(text, store_list):
    for store in store_list:
        if store in text:
            return store
    
    # search for "SIA" with regex
    sia_pattern = re.compile(r'SIA\s+(.+)')
    match = sia_pattern.search(text)
    if match:
        return match.group(0)
    
    return "Unknown Store"

def split_by_segment(text):
    # When using pytesseract to extract text from receipt image, the text is split into segments and divided by the word "Segment"
    # returns the receipt text split into segments
    segments = text.split("Segment")
    # Remove the first element of the list since it is empty
    segments.pop(0)
    return segments

def identify_segments(segments):
    '''
    # Lets assume that the first segment is the header
    header_segment = segments[0]
    # Second segment is the product list
    product_segment = segments[1]
    # Third segment is the discount list
    discount_segment = segments[2]
    # Fourth segment is the payment details
    payment_segment = segments[3]

    # To identify the segments if problems arise consider using the following:
    Segment 0 is the header
    The rest of the segments are identified by contents
    Product list segment is identified by having
      "gab X Y,Z EUR" in the segment or "Atl. X,Y Gala cena Z,Y"
    Discount segment is identified by:
      starting with "ATLAIDES"
    Payment segment is identified by:
        having one of these:
        "Maksājuma karte"
        "BANKAS KVĪTS"
        "KOPĀ:"
    Other segments are unipoortant
    '''
    pass

def identify_product_segment(segments):
    # we need to find a price details segment somewhere in the segment
    price_details_pattern = re.compile(r'\d+(,\d+)?\s*(gab|kg|g|ml|l)\s*X\s*\d+(,\d+)?\s*EUR')
    for segment in segments:
        if price_details_pattern.search(segment):
            return segment
        
    return None


def extract_products_details(text):
    '''
    Extracts product details from text.
    Output is a list of dictionaries.
    Each dictionary contains the following keys:
        name - product name details
        price - price details
        discount - discount details if any
    '''

    # Define patterns for price details and discounts
    price_detail_pattern = re.compile(r'\d+(,\d+)?(\s*|.)(gab|kg|g|ml|l)\s*(X|x)(\s*|.)\d+(,\d+)?\s*EUR')
    discount_pattern = re.compile(r'(Atl|atl)\.\s+-\d+(,\d+)?\s+.*((G|g)ala(\s+|.)cena)?\s+\d+(,\d+)?')

    # Split text into lines and remove empty lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    product_details = []
    current_product = {}

    for line in lines:
        # Check if the line contains price details
        if price_detail_pattern.search(line):
            current_product['price'] = line
        # Check if the line contains a discount
        elif discount_pattern.search(line):
            current_product['discount'] = line
            # End of a product block, add to list and reset current_product
            product_details.append(current_product)
            current_product = {}
        # If it's neither, then it's part of the product name
        else:
            # if already have price details, then this is next product
            if 'price' in current_product:
                current_product['discount'] = None
                product_details.append(current_product)
                current_product = {}
            # If we already have a product name, append this line to it
            if 'name' in current_product:
                current_product['name'] += ' ' + line
            else:
                current_product['name'] = line

    # Add the last product if any details were captured
    if current_product:
        product_details.append(current_product)

    return product_details

def extract_products(text):
    '''
    Extracts products from text.
    Output is a list of dictionaries.
    Each dictionary contains:
        name
        price_per_unit
        quantity
        measurment_unit
        total
        discount
        total_with_discount
    '''	
    products_details = extract_products_details(text)
    # print(products_details)

    products = []

    for product in products_details:
        name = None
        price_per_unit = None
        quantity = None
        measurement_unit = None
        total = None
        discount = None
        total_with_discount = None

        # if 'name' not in product:
        #     print(text)
        #     print(products_details)
        name = product['name']
        if 'price' not in product:
            print(text)
            print(products_details)
        price_details = product['price']
        if 'discount' in product:
            discount_details = product['discount']
        else:
            discount_details = None

        # Extract the price per
        price_per_pattern = re.compile(r'(\d+(,\d+)?)\s*EUR')
        match = price_per_pattern.search(price_details)
        price_per_unit = match.group(1)
        price_per_unit = float(price_per_unit.replace(',', '.'))

        # Extract the quantity and measurement unit
        quantity_pattern = re.compile(r'(\d+(,\d+)?)\s*((gab|kg|g|ml|l))')
        match = quantity_pattern.search(price_details)
        quantity = match.group(1)
        measurement_unit = match.group(3)
        quantity = float(quantity.replace(',', '.'))

        # extract the discount
        if discount_details:
            discount_pattern = re.compile(r'-\d+(,\d+)?')
            match = discount_pattern.search(discount_details)
            discount = match.group(0)
            discount = float(discount.replace(',', '.'))
        else:
            discount = None


        # Extract the total
        total_pattern = re.compile(r'EUR(\s*/\s*(kg|g|ml|l|gab))?\s+(\d+(,\d+)?)') # for "2,30" in "2 gab X 1,15 EUR 2,30 A"
        match = total_pattern.search(price_details)
        if match:
            total = match.group(3)
            total = float(total.replace(',', '.'))

        if discount:
            total_from_discount_details_pattern = re.compile(r'Gala\s+cena\s+(\d+(,\d+)?)') # for "1,98" in "Atl. -0,32 Gala cena 1,98"
            match = total_from_discount_details_pattern.search(discount_details)
            if match:
                total_with_discount = match.group(1)
                total_with_discount = float(total_with_discount.replace(',', '.'))
        
        # # Extract the total
        # # Total is gotten from the price details after EUR or after Gala cena if there is a discount
        # # we want to compare the total from after EUR and after Gala cena and the calculated total
        # # This can be used to check how correct is the ocr, this won't be done for now
        # # Total priority is as follows: Gala cena > EUR > calculated total
        
        # calculated_total = round(price * count,2) + discount
        # total_pattern = re.compile(r'EUR\s+(\d+(,\d+)?)')
        # match = total_pattern.search(price_details)
        # if match:
        #     total = match.group(1)
        #     total = round(float(total.replace(',', '.')),2) + discount
        #     # check if total from price details matches calculated total
        #     if total != calculated_total:
        #         # check if difference is by times 10 or 100
        #         # if so then ocr missed a , or .
        #         difference = total / calculated_total
        #         if difference >= 8 and difference <= 12:
        #             total = total / 10
        #         elif difference >= 80 and difference <= 120:
        #             total = total / 100
        # else:
        #     total = calculated_total
        
        # if discount != 0:
        #     total_from_discount_details_pattern = re.compile(r'Gala\s+cena\s+(\d+(,\d+)?)')
        #     match = total_from_discount_details_pattern.search(discount_details)
        #     if match:
        #         total_from_discount_details = match.group(1)
        #         total_from_discount_details = float(total_from_discount_details.replace(',', '.'))

        #         if total_from_discount_details != total:
        #             # print("Total from discount details does not match total from price details")
        #             # print(f"Total from discount details: {total_from_discount_details}")
        #             # print(f"Total from price details: {total}")
        #             # print("Using total from discount details")
        #             total = total_from_discount_details

        products.append({
            'name': name,
            'price_per_unit': price_per_unit,
            'quantity': quantity,
            'measurement_unit': measurement_unit,
            'total': total,
            'discount': discount,
            'total_with_discount': total_with_discount
        })
        

    return products

def extract_total(text):
    patterns = [
        re.compile(r'KOPĀ:\s+(\d+(,\d+)?)\s+EUR'),
        re.compile(r'Samaksai\s+EUR\s+(\d+(,\d+)?)'),
        re.compile(r'Bankas\s+karte\s+(\d+(,\d+)?)')
    ]
    totals = []
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            total = match.group(1)
            total = float(total.replace(',', '.'))
            totals.append(total)
    if len(totals) == 0:
        print("Total not found")
        return None

    # if all totals are the same, return that total
    if len(set(totals)) == 1:
        return totals[0]

    # if two totals are the same and the third is different, return the two that are the same
    if len(set(totals)) == 2:
        for total in totals:
            if totals.count(total) == 2:
                return total
    
    # if all totals are different, return error
    # print("All totals are different")
    return totals[0]

def extract_date(text):
    # receipt can contain mutiple dates
    # 2023-10-16 12:23:43
    # LAIKS 2023-10-16 12:23:43
    # find both and return if equal
    # if not equal return the one without datetime errors like being in the future or having more hours or minutes than possible

    date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})')
    match = date_pattern.findall(text)
    if not match:
        return None
    
    # Check for datetime correctness
    correct_dates = []
    for date in match:
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            if date <= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
                correct_dates.append(date)
        except ValueError:
            pass
    
    if len(correct_dates) == 1:
        # print("One correct date found")
        return correct_dates[0]
    
    if len(set(correct_dates)) == 1:
        # print("Multiple correct dates found")
        return correct_dates[0]
    else:
        # return the largest date
        return max(correct_dates)

def parse_receipt(receipt_text):
    '''
    Function for converting receipt text to dictionary either from raw text or from path to text file
    Returns receipt dictionary containing the following keys:
        date
        store
        total
        products
    '''
    store_list = ['Rimi', 'Maxima']
    # if receipt_text is a path to a text file, read the text file
    if os.path.isfile(receipt_text):
        receipt_text = open(receipt_text, 'r', encoding='utf-8').read()
    
    receipt_text = post_process_cleanup(receipt_text)

    receipt = {
        'date': None,
        'store': None,
        'total': None,
        'products': None
    }

    segmented_ocr_text = split_by_segment(receipt_text)
    if len(segmented_ocr_text) < 2:
        print("Error: Receipt text does not contain enough segments")
        print(receipt_text)
        print(segmented_ocr_text)
        return None
    store_name = extract_store(segmented_ocr_text[0], store_list)
    product_segment = identify_product_segment(segmented_ocr_text)
    products = extract_products(product_segment)
    total = extract_total(receipt_text)
    date = extract_date(receipt_text)

    receipt['date'] = date
    receipt['store'] = store_name
    receipt['total'] = total
    receipt['products'] = products

    return receipt

def parse_multiple_receipts_folder(directory_path: str):
    '''
    Parses multiple receipts from text files in a directory
    Returns a list of receipt dictionaries
    '''
    receipts = []
    files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
    for file in files:
        file_path = os.path.join(directory_path, file)
        receipt = parse_receipt(file_path)
        receipts.append(receipt)
    return receipts

def parse_multiple_receipts(receipt_texts: dict):
    '''
    Parses multiple receipt texts
    Returns a list of receipt dictionaries containing:
        date
        store
        total
        products
    '''
    receipts = []
    for txt in receipt_texts.values():
        receipt = parse_receipt(txt)
        receipts.append(receipt)

    return receipts

def print_receipt(receipt):
    '''
    Prints receipt data
    '''
    print(f"Date: {receipt['date']}")
    print(f"Store: {receipt['store']}")
    print(f"Total: {receipt['total']}")
    print("Products:")
    for product in receipt['products']:
        print(f"Name: {product['name']}")
        print(f"\tPrice per: {product['price_per_unit']}")
        print(f"\tQuantity: {product['quantity']}")
        print(f"\tMeasurement: {product['measurement_unit']}")
        print(f"\tTotal: {product['total']}")
        print(f"\tDiscount: {product['discount']}")
        print(f"\tTotal with discount: {product['total_with_discount']}")
        print()
    

# def parser_postprocess():
# TODO receipt total validation

# receipt = parse_receipt('data/receipt_texts/ocr/receipt1.txt')

# for key, value in receipt.items():
#     if key == 'products':
#         print(f"{key}:")
#         for product in value:
#             for k, v in product.items():
#                 if k == 'name':
#                     print(f"{k}: {v}")
#                 else: 
#                     print(f"\t{k}: {v}")
#     else:
#         print(f"{key}: {value}")


# # Sample usage
# some functions were renamed after this was written
# # opem ocr file from data/receipt_texts/ocr
# ocr_text = open('data/receipt_texts/ocr/receipt1.txt', 'r', encoding='utf-8').read()
# ocr_text = post_process_cleanup(ocr_text)

# receipt = {
#     'datetime': None,
#     'store': None,
#     'total': None,
#     'products': None
# }

# store_list = ['Rimi', 'Maxima']

# segmented_ocr_text = segment(ocr_text)
# store_name = extract_store(segmented_ocr_text[0], store_list)
# products = extract_products(segmented_ocr_text[1])
# total = extract_total(ocr_text)
# date = extract_date(ocr_text)

# receipt['datetime'] = date
# receipt['store'] = store_name
# receipt['total'] = total
# receipt['products'] = products

# print(receipt)

# # print(f"Store: {store_name}")
# # print(f'Total: {total}')
# # for product in products:
# #     print(f"Product Name: {product['name']}")
# #     print(f"Price per: {product['price_per_unit']}")
# #     print(f"Quantity: {product['quantity']}")
# #     print(f"Measurement: {product['measurement']}")
# #     print(f"Total: {product['total']}")
# #     print(f"Discount: {product['discount']}")
# #     print(f"Total with discount: {product['total_with_discount']}")
# #     print()