from abc import ABC, abstractmethod
from datetime import datetime

class Donation(ABC):
    def __init__(self, donor_name, amount):
        self.donor_name = donor_name
        self.amount = amount

    @abstractmethod
    def record_donation(self):
        pass

class CashDonation(Donation):
    def __init__(self, donor_name, amount, donation_date=datetime.now()):
        super().__init__(donor_name, amount)
        self.donation_date = donation_date

    def record_donation(self):
        print(f"Cash donation of ${self.amount} recorded on {self.donation_date} by {self.donor_name}.")

class ItemDonation(Donation):
    def __init__(self, donor_name, amount, item_type):
        super().__init__(donor_name, amount)
        self.item_type = item_type

    def record_donation(self):
        print(f"Item donation of {self.item_type} with a value of ${self.amount} recorded by {self.donor_name}.")
