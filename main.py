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

def main():
    # receipt_texts = scan_multiple_receipts('receipts')
    # # save them to files
    # write_receipts_texts_to_files(receipt_texts, 'texts')

    # receipts_dict = parse_multiple_receipts(receipt_texts)
    receipts_dict = parse_multiple_receipts_folder('texts')
    # print(receipts_dict)
    # save it to file json format
    # with open('receipts.txt', 'w', encoding='utf-8') as f:
    #     json.dump(receipts_dict, f, indent=4)
    
    # now lets identify products
    products = get_product_names(receipts_dict)
    print(products)
    # find_products_of_same_name(products)
    # find_products_of_same_name_but_misspelled(products)

main()