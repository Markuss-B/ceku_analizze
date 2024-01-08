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
        console.print("[5] Receipt total over time graph")
        console.print("[0] Exit")

        choice = Prompt.ask("Enter your choice", choices=["0", "1", "2", "3", "4", "5"])
        if choice == "0":
            console.print("Exiting the system. Goodbye!", style="bold red")
            break
        elif choice == "1":
            # Initially display the top 10 most bought products
            sorted_products = sort_products_by_frequency(products_dict)
            search_option(products_dict, sorted_products, 'Top 10 most bought products:')

        elif choice == "2":
            moust_bough_products = sort_products_by_frequency(products_dict)
            console.print("Most bought products:", style="bold")
            # Displays the top 5 most bought products
            for index, (name, data) in enumerate(moust_bough_products[:5], start=1):
                console.print(f"[{index}] {name} ({len(data)} entries)")

            graph_multiple_products(moust_bough_products[:5])
        elif choice == "3":
            exp_prod = sort_products_by_price_per_unit(receipts)  # Function to be implemented
            console.print("Most expensive products:", style="bold")
            for index, (name, data) in enumerate(exp_prod[:10], start=1):
                console.print(f"[{index}] {name} ({data[0][2]} €)")
            
            # press enter to continue
            input("Press Enter to continue...")
        elif choice == "4":
            console.print('Finding the most expensive receipt...', style="italic")
            exp_receipt = find_most_expensive_receipt(receipts)
            print_receipt(exp_receipt)
            console.clear()
        elif choice == "5":
            console.print('Displaying receipt total over time graph...', style="italic")
            # ask to choose over all time or over to sum over months
            choice = Prompt.ask("[1] Sum over months\n[2] Sum over all time\nEnter your choice", choices=["1", "2", "0"])
            if choice == "1":
                graph_receipt_total_over_months(receipts)
            elif choice == "2":
                graph_receipt_total_over_time(receipts)
            elif choice == "0":
                continue
            console.clear()
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
        # ask to continue
        input("Press Enter to continue...")
    
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

def search_option(products_dict, initial_products, text):
    console.print(text, style="bold")
    # print(initial_products)
    for index, (name, data) in enumerate(initial_products[:10], start=1):
        console.print(f"[{index}] {name} ({len(data)} entries)")

    while True:
        search_query = Prompt.ask("Enter a product name to search, or number to choose from the above list, or 'exit' to return")

        if search_query == "exit":
            break

        if search_query.isdigit():
            # User chose from the list
            if int(search_query) <= 10:
                try:
                    search_query = initial_products[int(search_query) - 1][0]
                    graph_product_price(search_query, products_dict[search_query])
                except IndexError:
                    console.print("Invalid choice", style="bold red")
                    continue
            else:
                console.print("Invalid choice", style="bold red")
                continue
        else:
            # User entered a search query
            search_query = search_query.lower()

            # Perform a fuzzy search among all products
            matches = process.extract(search_query, products_dict.keys(), limit=10)
            # find matches in products_dict
            matches = [(name, products_dict[name]) for name, score in matches]
            search_option(products_dict, matches, "Top matching products:")
            break

main()
