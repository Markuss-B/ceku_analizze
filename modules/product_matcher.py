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
    i = 0
    for receipt in receipts:
        for product in receipt['products']:
            # save product name with receipt id
            products.append([product['name'], i])
        i += 1
    
    return products

def find_products_of_same_name(products: list):
    # 2. Find all products of the same name
    for product in products:
        occurances = products.count(product)
        print(f'{product} occurs {occurances} times')
    
def find_products_of_same_name_but_misspelled(products: list):
    # 3. Find products of the same name but misspelled
    # make all words lowercase
    # for i in range(len(products)):
    #     products[i] = products[i].lower()
    #     # remove all commas and special characters
    #     remove = [',', '.', '!', '?', '"', "'", '(', ')', '[', ']', '{', '}', ':', ';', '-', '_', '+', '=', '/', '\\', '|', '<', '>', '@', '#', '$', '%', '^', '&', '*', '~', '`']
    #     for char in remove:
    #         products[i] = products[i].replace(char, '')
    #     # remove all numbers
    #     products[i] = ''.join([i for i in products[i] if not i.isdigit()])

    # sort them alphabetically
    products.sort()

    product_matches = {}
    products_matched = {}
    for product, id in products:
        # print(product_matches)
        if product in product_matches.keys():
            # print(f'{product} already has a match')
            continue
        matches = find_similar_products(product, products)
        product_matches[product] = matches
        if len(matches) > 0:
            products_matched[[product, id]] = matches
            # print(f'{product, id} has the following misspellings: {matches}')
        # else:
            # print(f'{product} has no misspellings')
        # print(f'{product} has the following misspellings: {matches}')
    
    return products_matched


def find_similar_products(misspelled_name, product_list, limit=4):
    # Normalize and preprocess the names
    misspelled_name = misspelled_name.lower()
    product_list = [[product.lower(), id] for product, id in product_list if product.lower() != misspelled_name]

    # Get the top 'limit' matches based on similarity
    matches = process.extract(misspelled_name, product_list, limit=limit)

    # Keep the ones with score >90
    matches = [match[0] for match in matches if match[1] >= 90 and match[1] <100]
    # print(matches)

    return matches

def normalize_product_names(receipts_dict, products_mathed):
    # 6. Normalize names of the products
    for product in products_mathed:
        for match in products_mathed[product]:
            # print(match)
            # print(receipts_dict[match[1]]['products'][match[2]]['name'])
            receipts_dict[match[1]]['products'][match[2]]['name'] = product
            # print(receipts_dict[match[1]]['products'][match[2]]['name'])
    
    return receipts_dict