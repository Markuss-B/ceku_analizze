def correct_product_prices(receipt_dict):
    '''
    Corrects the product prices in the receipt dict.
    
    Corrects values:
        price_per_unit
        total
        discount
        total_with_discount

    Returns the receipt dict.
    '''

    # for receipt in receipt_dict:
    #     for product in receipt['products']:
    pass

def normalize_price(price):
    # Correct common OCR errors (misplaced decimal points)
    if price > 100:
        price /= 100
    return round(price, 2)

def correct_prices(price_per_unit, quantity, total, discount, total_with_discount):
    # Normalize prices
    price_per_unit = normalize_price(price_per_unit)
    total = normalize_price(total)
    if discount is not None:
        discount = -abs(normalize_price(discount))
    if total_with_discount is not None:
        total_with_discount = normalize_price(total_with_discount)

    if discount is None and total_with_discount is None:
        if total is None:
            total = round(price_per_unit * quantity, 2)
        elif price_per_unit is None:
            price_per_unit = round(total / quantity, 2)
        elif quantity is None:
            quantity = round(total / price_per_unit, 2)
        
            

    return [price_per_unit, quantity, total, discount, total_with_discount]

# Example usage
corrected_prices = correct_prices(195, 1, 199, 0.3, 1.69)
print(corrected_prices)



# # Example usage
# corrected_prices = correct_prices(1.99, 1, 199, -0.3, 1.69)
# print(corrected_prices)

# def run_tests():
#     tests = [
#         # Test case format: (price_per_unit, quantity, total, discount, total_with_discount, expected_output)
#         (1.99, 1, 1.99, None, None, [1.99, 1, 1.99, None, None]),  # No Discount, Correct Values
#         (2.50, 2, 500, None, None, [2.50, 2, 5.00, None, None]),   # No Discount, OCR Error in Total
#         (0.99, 10, 9.90, -2.00, 7.90, [0.99, 10, 9.90, -2.00, 7.90]), # Discount, Correct Values
#         (1.50, 2, 300, -0.30, 2.70, [1.50, 2, 3.00, -0.30, 2.70]), # Discount, OCR Error in Total and Discount
#         (1.00, 5, 5.00, -1.00, 400, [1.00, 5, 5.00, -1.00, 4.00]), # Discount, OCR Error in Total With Discount
#         (100.00, 1, 10000, None, None, [1.00, 1, 1.00, None, None]), # High Values
#         (0.00, 0, 0.00, None, None, [0.00, 0, 0.00, None, None]),   # Zero Values
#         (-1.99, 1, -1.99, None, None, [-1.99, 1, -1.99, None, None]) # Negative Values
#     ]

#     for i, test in enumerate(tests):
#         result = correct_prices(*test[:5])
#         assert result == test[5], f"Test {i + 1} failed: {result} != {test}"
#         print(f"Test {i + 1} passed.")

# # Run the tests
# run_tests()

