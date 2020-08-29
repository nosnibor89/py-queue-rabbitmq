class Payment:
    def __init__(self, name, amount, card_number):
        self.name = name
        self.amount = amount
        self.card_number = card_number


class PurchaseOder:
    def __init__(self, po_number, amount_to_pay, company):
        self.po = po_number
        self.amount = amount_to_pay
        self.company = company
