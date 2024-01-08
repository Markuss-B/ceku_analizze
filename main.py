'''
Product analysis
1. Scan receipts in to the system as a directory
2. Find all products in the receipts
3. Find for each product prices with dates
4. Let user choose a product for which he wants to see the price history

User analysis
Most bought products
Most expensive products
Most expensive receipt
All visits to stores
'''
import json
from modules.receipt_scanner import scan_multiple_receipts, write_receipts_texts_to_files
from modules.receipt_parser import parse_multiple_receipts, parse_multiple_receipts_folder
from modules.product_matcher import *
from modules.xml_extraction import get_rimi_products
from modules.analysis import *

def main():
    print('Welcome to the receipt analysis system!')
    if input('Do you want to setup receipts data? (y/n) ') == 'y':
        print('Setting up receipts data...')
        receipts = setup_receipts_data()
    else:
        print('Loading receipts data from files...')
        receipts = get_receipts_data()

    print('Receipts data loaded!')
    print('Making a list of products with prices and dates...')
    products_dict = get_products_dict(receipts)
    # print(products_dict)
    print('Done!')

    print('Price history for a product with most entries:')
    name, data = find_product_with_most_entries(products_dict)
    # print(product)
    graph_product_price(name, data)

    print('Most expensive receipt:')
    exp_receipt = find_most_expensive_receipt(receipts)
    print_receipt(exp_receipt)
    

    


def setup_receipts_data():
    receipt_texts = scan_multiple_receipts('receipts')
    # save them to files
    write_receipts_texts_to_files(receipt_texts, 'texts')

    receipts_dict = parse_multiple_receipts(receipt_texts)
    # print(receipts_dict)
    # save it to file json format
    with open('receipts.txt', 'w', encoding='utf-8') as f:
        json.dump(receipts_dict, f, indent=4)

    rimi_products = get_rimi_products() # automatically saves to file 'rimi_products.txt'
    # print(rimi_products)

    spellchecked_receipts = spellcheck_receipts(receipts_dict, rimi_products)
    # print(spellchecked_receipts)

    # spellchecked_receipts = correct_product_prices(spellchecked_receipts)

    with open('receipts_spellchecked.txt', 'w', encoding='utf-8') as f:
        json.dump(spellchecked_receipts, f, indent=4)
    
    return spellchecked_receipts

def get_receipts_data():
    with open('receipts_spellchecked.txt', 'r', encoding='utf-8') as f:
        receipts_dict = json.load(f)
    return receipts_dict

def print_receipt(receipt):
    print('Date:', receipt['date'])
    print('Store:', receipt['store'])
    print('Total:', receipt['total'])
    print('Products:')
    for product in receipt['products']:
        print_product(product)

def print_product(product):
    print('Name:', product['name'])
    print('\tPrice per unit:', product['price_per_unit'])
    print('\tQuantity:', product['quantity'])
    print('\tUnit:', product['measurement_unit'])
    print('\tTotal:', product['total'])
    if product['discount'] != None:
        print('\tDiscount:', product['discount'])
        print('\tTotal with discount:', product['total_with_discount'])

main()