import requests
import xml.etree.ElementTree as ET
import re
import json
from rich.progress import Progress

def get_rimi_products():
    product_sitemaps = [
        'https://www.rimi.lv/e-veikals/sitemaps/products/siteMap_rimiLvSite_Product_lv_1.xml',
        'https://www.rimi.lv/e-veikals/sitemaps/products/siteMap_rimiLvSite_Product_lv_2.xml',
        'https://www.rimi.lv/e-veikals/sitemaps/products/siteMap_rimiLvSite_Product_lv_3.xml',
        'https://www.rimi.lv/e-veikals/sitemaps/products/siteMap_rimiLvSite_Product_lv_4.xml',
        'https://www.rimi.lv/e-veikals/sitemaps/products/siteMap_rimiLvSite_Product_lv_5.xml'
    ]

    products = parse_product_sitemaps(product_sitemaps)

    manual_products = [
        "kuka kuko bruklenu abolu veganiska 200",
        "kartupeli jaunie kg",
        "lapu kaposts kale 180 g 1 sk",
        "tomati latvijas kg 1sk",
        "ananasi lielie kg",
        "rimi papira maiss mazs 32x17x34",
        "rimi papira maiss liels 32x17x45",
        "muslis graci sokolades 500g",
        "veganu kokosriekstu pir ar mango pasif 190g",
        "kartupeli delikatess fast ica 2kg",
        "dabigais tofu Lunter 180g",
        "rimi papira maisins liels ziemassvetku",
        "pokijs ar tofu un poke merci 320g",
        "plumes tumsas 500g",
        "rimi kaste",
    ]

    products += manual_products

    # only save to file the new products
    with open('rimi_products.txt', 'r') as file:
        old_products = json.load(file)
        for product in products:
            if product not in old_products:
                old_products.append(product)
        products = old_products

    # save it to file
    with open('rimi_products.txt', 'w') as file:
        json.dump(products, file, indent=4)

    # print_categories(products)

    return products

def parse_sitemap(url):
    response = requests.get(url)
    root = ET.fromstring(response.content)
    urls = []
    for child in root:
        # ignore https://www.rimi.lv/e-veikals/lv
        if child[0].text != 'https://www.rimi.lv/e-veikals/lv':
            urls.append(child[0].text)
    return urls

def parse_product_sitemaps(product_sitemaps):
    products = {}
    urls = []
    for url in product_sitemaps:
        urls += parse_sitemap(url)
    
    products = []

    with Progress() as progress:
        task = progress.add_task("Parsing rimi products from sitemap...", total=len(urls))
        for url in urls:
            # Remove the base URL
            clean_url = url.replace('https://www.rimi.lv/e-veikals/lv/produkti/', '')

            # Remove the suffix part from the URL
            product_path = re.sub(r'/p/.*', '', clean_url)

            # replace - with space
            product_path = product_path.replace('-', ' ')

            # Split the remaining URL into categories
            product_parts = product_path.split('/')
            name = product_parts[-1]

            products.append(name)
            progress.update(task, advance=1)

    return products