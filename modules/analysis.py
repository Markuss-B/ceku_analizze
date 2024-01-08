import matplotlib.pyplot as plt
import datetime

def get_products_dict(receipts_dict):
    '''
    Flips receipts with focus on products.
    Returns a dictionary with products as keys and and values as follows:
        receiptid, date, price_per_unit, quantity, total, discount, total_with_discount
    '''
    products_dict = {}
    i = 0
    for receipt in receipts_dict:
        for product in receipt['products']:
            if product['name'] not in products_dict:
                products_dict[product['name']] = []
            products_dict[product['name']].append([i, receipt['date'], product['price_per_unit'], product['quantity'], product['total'], product['discount'], product['total_with_discount']])        
        i += 1
    return products_dict

def graph_product_price(name, data):
    '''
    Graphs product price over time.
    '''

    dates = []
    prices = []
    for entry in data:
        print(entry[1], end=' ')
        print(entry[2])
        # remove time from date
        entry[1] = entry[1].split(' ')[0]
        dates.append(entry[1])
        prices.append(entry[2])
    plt.scatter(dates, prices)
    plt.title(name)
    plt.xlabel('Date')
    plt.ylabel('Price')
    # rotate dates
    plt.xticks(rotation=45)
    plt.show()

def find_product_with_most_entries(products_dict):
    '''
    Returns the product with the most entries.
    '''
    most_entries = 0
    most_entries_product_name = None
    most_entries_product_data = None
    for product in products_dict:
        if len(products_dict[product]) > most_entries:
            most_entries = len(products_dict[product])
            most_entries_product_name = product
            most_entries_product_data = products_dict[product]
    return most_entries_product_name, most_entries_product_data

def find_most_expensive_receipt(receipts_dict):
    '''
    Returns the most expensive receipt.
    '''
    most_expensive = 0
    most_expensive_receipt = None
    for receipt in receipts_dict:
        if receipt['total'] == None:
            continue
        if receipt['total'] > most_expensive:
            most_expensive = receipt['total']
            most_expensive_receipt = receipt
    return most_expensive_receipt

def sort_products_by_frequency(products_dict):
    '''
    Sorts products by frequency.
    '''
    sorted_products = sorted(products_dict.items(), key=lambda x: len(x[1]), reverse=True)
    return sorted_products

def graph_multiple_products(products_dict):
    """
    Graphs multiple products in one graph. Each product's data is sorted by date.
    Args:
    - products_dict (dict): A dictionary where keys are product names and values are lists of 
                            [id, date, price_per_unit, ...].
    """
    plt.figure(figsize=(10, 6))
    print(products_dict)
    print(type(products_dict))

    for product_name, data in products_dict.items():
        # Ensure data is sorted by date (assuming date is at index 1 in the data)
        data.sort(key=lambda x: datetime.datetime.strptime(x[1], "%Y-%m-%d %H:%M:%S"))

        # Extract dates and prices for the product
        dates = [datetime.datetime.strptime(entry[1], "%Y-%m-%d %H:%M:%S") for entry in data]
        prices = [entry[2] for entry in data]

        # Plot each product's price history
        plt.plot(dates, prices, label=product_name)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Price History of Multiple Products')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def sort_products_by_price_per_unit(receipts_dict):
    '''
    Sorts products by price per unit.
    '''
    products_dict = get_products_dict(receipts_dict)
    sorted_products = sorted(products_dict.items(), key=lambda x: x[1][0][2], reverse=True)
    return sorted_products