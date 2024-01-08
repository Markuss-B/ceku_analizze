import matplotlib.pyplot as plt

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
