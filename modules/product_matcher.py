    # 1. Get all products from the receipts
    # 2. Find all products of the same name
    # 3. Find products of the same name but misspelled
    # 4. Print those same name products and their name variants
    # 5. Print products with no name variants
    # 6. Normalize names of the products
from fuzzywuzzy import process

def get_product_names(receipts: dict):
    # 1. Get all products from the receipts
    products = []
    for receipt in receipts:
        for product in receipt['products']:
            products.append(product['name'])
    
    return products

def find_products_of_same_name(products: list):
    # 2. Find all products of the same name
    for product in products:
        occurances = products.count(product)
        print(f'{product} occurs {occurances} times')
    
def find_products_of_same_name_but_misspelled(products: list):
    # 3. Find products of the same name but misspelled
    # make all words lowercase
    for i in range(len(products)):
        products[i] = products[i].lower()

    product_matches = {}
    for product in products:
        if product in product_matches or product in product_matches.values():
            continue
        matches = find_similar_products(product, products)
        product_matches[product] = matches
        print(f'{product} has the following misspellings: {matches}')


def find_similar_products(misspelled_name, product_list, limit=3):
    # Normalize and preprocess the names
    misspelled_name = misspelled_name.lower()
    product_list = [product.lower() for product in product_list]

    # Get the top 'limit' matches based on similarity
    matches = process.extract(misspelled_name, product_list, limit=limit)
    return matches