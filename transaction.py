# transaction.py


class Transaction:
    def __init__(self, date, category, amount, description, transaction_id):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description
        self.transaction_id = transaction_id
