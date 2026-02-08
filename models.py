class Product:
    def __init__(self, id, name, category, base_price):
        self.id = id
        self.name = name
        self.category = category
        self.base_price = float(base_price)

class Customer:
    def __init__(self, id, name, email, lifetime_value=0.0):
        self.id = id
        self.name = name
        self.email = email
        self.lifetime_value = float(lifetime_value)

class Order:
    def __init__(self, date, items, customer, amount, status):
        self.date = date
        self.items = items
        self.customer = customer
        self.amount = float(amount)
        self.status = status
