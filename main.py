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
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import print as rprint
from modules.receipt_scanner import scan_multiple_receipts, write_receipts_texts_to_files
from modules.receipt_parser import parse_multiple_receipts, parse_multiple_receipts_folder
from modules.product_matcher import *
from modules.xml_extraction import get_rimi_products
from modules.analysis import *

# Initialize Rich Console
console = Console()

def main():
    console.print('Welcome to the Receipt Analysis System!', style="bold blue")

    # Setup or Load Data
    if Prompt.ask('Do you want to setup receipts data?', choices=['y', 'n'], default='n') == 'y':
        console.print('Setting up receipts data...', style="italic")
        receipts = setup_receipts_data()
    else:
        console.print('Loading receipts data from files...', style="italic")
        receipts = get_receipts_data()

    console.print('Receipts data loaded!', style="green")

    console.print('Making a list of products with prices and dates...', style="italic")
    products_dict = get_products_dict(receipts)
    console.print('Products list ready!', style="green")

    # console.print('Displaying price history for the product with most entries:', style="bold")
    # name, data = find_product_with_most_entries(products_dict)
    # graph_product_price(name, data)

    while True:
        console.print("\n[bold]Select an analysis option:[/bold]")
        console.print("[1] Price History for a Specific Product")
        console.print("[2] Most Bought Products")
        console.print("[3] Most Expensive Products")
        console.print("[4] Most Expensive Receipt")
        console.print("[5] Exit")

        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5"])

        if choice == "1":
            # Initially display the top 10 most bought products
            sorted_products = sort_products_by_frequency(products_dict)  # Assuming this function is implemented
            console.print("Most bought products:", style="bold")
            for index, (name, data) in enumerate(sorted_products[:10], start=1):
                console.print(f"[{index}] {name} ({len(data)} entries)")

            while True:
                search_query = Prompt.ask("Enter a product name to search, 'select' to choose from the above list, or 'exit' to return")

                if search_query.lower() == 'exit':
                    break

                if search_query.lower() == 'select':
                    selected_index = Prompt.ask("Enter the number of the product you want to select", default="1")
                    try:
                        selected_product = sorted_products[int(selected_index) - 1][0]
                        graph_product_price(selected_product, products_dict[selected_product])
                        break
                    except (IndexError, ValueError):
                        console.print("Invalid selection. Please try again.", style="red")
                else:
                    # Perform a fuzzy search among all products
                    matches = process.extract(search_query, products_dict.keys(), limit=10)
                    console.print("Top matching products:", style="bold")
                    for i, (match, _) in enumerate(matches, start=1):
                        console.print(f"[{i}] {match} ({len(products_dict[match])} entries)")

                    selection = Prompt.ask("Select a product number to see its price history, 'search' to search again, or 'exit' to return")
                    if selection.isdigit() and 1 <= int(selection) <= len(matches):
                        selected_product = matches[int(selection) - 1][0]
                        graph_product_price(selected_product, products_dict[selected_product])
                        break
                    elif selection.lower() == 'exit':
                        break
                    elif selection.lower() != 'search':
                        console.print("Invalid selection. Please try again.", style="red")
        elif choice == "2":
            moust_bough_products = sort_products_by_frequency(products_dict)
            console.print("Most bought products:", style="bold")
            for index, (name, data) in enumerate(moust_bough_products[:10], start=1):
                console.print(f"[{index}] {name} ({len(data)} entries)")

            # graph the price changes for all of them
            most_bought_products = sort_products_by_frequency(products_dict)[:5]
            # fix the data format
            most_bought_dict = {name: data for name, data in most_bought_products}

            graph_multiple_products(most_bought_dict)
        elif choice == "3":
            exp_prod = sort_products_by_price_per_unit(receipts)  # Function to be implemented
            console.print("Most expensive products:", style="bold")
            for index, (name, data) in enumerate(exp_prod[:10], start=1):
                console.print(f"[{index}] {name} ({data[0][2]} €)")
        elif choice == "4":
            console.print('Finding the most expensive receipt...', style="italic")
            exp_receipt = find_most_expensive_receipt(receipts)
            print_receipt(exp_receipt)
        elif choice == "5":
            console.print("Exiting the system. Goodbye!", style="bold red")
            break
        else:
            console.print("Invalid choice, please try again.", style="red")



def setup_receipts_data():
    receipt_texts = scan_multiple_receipts('receipts')
    write_receipts_texts_to_files(receipt_texts, 'texts')

    receipts_dict = parse_multiple_receipts(receipt_texts)
    with open('receipts.txt', 'w', encoding='utf-8') as f:
        json.dump(receipts_dict, f, indent=4)

    rimi_products = get_rimi_products()  # automatically saves to file 'rimi_products.txt'
    spellchecked_receipts = spellcheck_receipts(receipts_dict, rimi_products)

    with open('receipts_spellchecked.txt', 'w', encoding='utf-8') as f:
        json.dump(spellchecked_receipts, f, indent=4)
    
    return spellchecked_receipts

def get_receipts_data():
    with open('receipts_spellchecked.txt', 'r', encoding='utf-8') as f:
        receipts_dict = json.load(f)
    return receipts_dict

def print_receipt(receipt):
    receipt_table = Table(title="Receipt Details", title_style="bold green")
    receipt_table.add_column("Date", justify="right")
    receipt_table.add_column("Store")
    receipt_table.add_column("Total", justify="right")
    receipt_table.add_row(receipt['date'], receipt['store'], str(receipt['total']))
    console.print(receipt_table)

    # ask if user wants to see products
    if Prompt.ask('Do you want to see the products?', choices=['y', 'n'], default='n') == 'y':
        product_table = Table(title="Products", title_style="bold magenta")
        product_table.add_column("Name")
        product_table.add_column("Price per Unit")
        product_table.add_column("Quantity")
        product_table.add_column("Unit")
        product_table.add_column("Total")
        product_table.add_column("Discount", justify="right")
        product_table.add_column("Total with Discount", justify="right")
        for product in receipt['products']:
            print_product(product, product_table)
        console.print(product_table)

def print_product(product, product_table=None):
    if product_table is None:
        product_table = Table()
        product_table.add_column("Name")
        product_table.add_column("Price per Unit")
        product_table.add_column("Quantity")
        product_table.add_column("Unit")
        product_table.add_column("Total")
        product_table.add_column("Discount", justify="right")
        product_table.add_column("Total with Discount", justify="right")

    discount = product['discount'] if product['discount'] else "-"
    total_with_discount = product['total_with_discount'] if product['discount'] else "-"
    product_table.add_row(product['name'], str(product['price_per_unit']), str(product['quantity']), 
                          product['measurement_unit'], str(product['total']), str(discount), str(total_with_discount))
    if product_table is None:
        console.print(product_table)


main()
