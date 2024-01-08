class Receipt:
    def __init__(self, receipt_id, date, total):
        self.receipt_id = receipt_id
        self.date = date
        self.total = total
        self.products = []

    def get_receipt_id(self):
        return self.receipt_id

    def get_date(self):
        return self.date

    def get_total(self):
        return self.total

    def get_products(self):
        return self.products

    def set_receipt_id(self, receipt_id):
        self.receipt_id = receipt_id

    def set_date(self, date):
        self.date = date

    def set_total(self, total):
        self.total = total

    def set_products(self, products):
        self.products = products

    def __str__(self):
        return f"Receipt ID: {self.receipt_id}\nDate: {self.date}\nTotal: {self.total}\nProducts: {self.products}"

class Product:

class ReceiptProduct: