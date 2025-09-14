import random
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# project requirement sqlachemy : 1.3.19

class MoneyTransferError(Exception):
    pass
class SameCardError(Exception):
    pass
class CardNumberError(Exception):
    pass
class CardNotFoundError(Exception):
    pass

Base = declarative_base()

class Card(Base):
    __tablename__ = 'card'
    id = Column(Integer, primary_key=True)
    number = Column(String)
    pin = Column(String)
    balance = Column(Integer)

    def __init__(self, code_bank=None, **kwargs):
        # so we still have access to the constructor of Card by SQLAlchemy
        if code_bank:
            self.number = self._generate_card_number(code_bank)
            self.pin = self._generate_pin()
            self.balance = 0
            print(f"Your card number is:\n{self.number}")
            print(f"Your card code is:\n{self.pin}")
        super().__init__(**kwargs)

    def _generate_number(self, nb=1):
        return "".join([random.choice("0123456789") for _ in range(nb)])

    @staticmethod
    def checksum(sequence):
        total = 0
        for i in range(len(sequence)):
            if i % 2 == 0:
                total += int(sequence[i]) * 2 if (int(sequence[i]) * 2 <= 9) else int(sequence[i]) * 2 - 9
            else:
                total += int(sequence[i])
        return str((10 - (total % 10)) % 10)

    def _generate_card_number(self, code_bank):
        customer_number = self._generate_number(9)
        return f"{code_bank}{customer_number}{Card.checksum(code_bank + customer_number)}"

    def _generate_pin(self):
        return self._generate_number(4)

    @staticmethod
    def validate_card(sequence):
        check = Card.checksum(sequence[:-1])
        test_check = sequence[-1]
        return check == test_check

    def __str__(self):
        return f"Card number: {self.number} - Pin: {self.pin} - Balance: {self.balance}"


def query(func):
    def wrapper(self, *args, **kwargs):
        session = self.Session()
        try:
            result = func(self, session, *args, **kwargs)
            session.commit()
            return result
        finally:
            session.close()

    return wrapper


class Bank:
    _IIN_CODE = "400000"
    engine = None

    def __init__(self):
        if Bank.engine is None:
            Bank.engine = create_engine("sqlite:///card.s3db")
            Base.metadata.create_all(Bank.engine)

        self.Session = sessionmaker(bind=Bank.engine)

    @query
    def create_account(self, session):
        print("\nYour card has been created")
        card = Card(Bank._IIN_CODE)
        session.add(Card(number=card.number,
                         pin=card.pin,
                         balance=card.balance))

    @query
    def log_in(self, session):
        card_number = input("\nEnter your card number:\n")
        code = input("Enter your PIN:\n")
        # We need to create a new object so the object is no more related to the session which is closed at each request
        card = session.query(Card).filter(Card.number == card_number, Card.pin == code).first()
        if card is None:
            return None
        else:
            return Card(number=card.number, pin=card.pin, balance=card.balance)

    @query
    def get_account_by_number(self, session, card_number):
        account = session.query(Card).filter(Card.number == card_number).first()
        if account is None:
            raise CardNotFoundError
        return Card(number=card_number, pin=account.pin, balance=account.balance)

    @query
    def get_all_accounts(self, session):
        for account in session.query(Card).all():
            print(account)

    @query
    def get_balance(self, session, account):
        card = session.query(Card).filter(Card.number == account.number).first().balance
        return card

    @query
    def add_income(self, session, account, balance):
        card = session.query(Card).filter(Card.number == account.number).first()
        new_balance = card.balance + balance
        # update in db and the current object
        session.query(Card).filter(Card.number == account.number).update({Card.balance: new_balance})
        account.balance = new_balance

    @query
    def close_account(self, session, account):
        session.query(Card).filter(Card.number == account.number).delete()

    @query
    def transfer_money(self, session, account, amount, account_to_transfer):
        session.query(Card).filter(Card.number == account.number).update({Card.balance: account.balance - amount})
        session.query(Card).filter(Card.number == account_to_transfer.number).update({Card.balance: account_to_transfer.balance + amount})


class MenuBank:
    class ItemMenu:
        def __init__(self, description, action):
            self._description = description
            self._action = action

        def get_description(self):
            return self._description

        def execute(self):
            return self._action()

    def __init__(self, bank: Bank):
        self._bank = bank
        self._account_logged = None
        self.menu = {
            "1": MenuBank.ItemMenu(description="Create account", action=self.create_account),
            "2": MenuBank.ItemMenu(description="Log into account", action=self.login_account),
            "0": MenuBank.ItemMenu(description="Exit", action=self.exit)
        }
        self.menu_account = {
            "1": MenuBank.ItemMenu(description="Balance", action=self.display_balance),
            "2": MenuBank.ItemMenu(description="Add income", action=self.add_income),
            "3": MenuBank.ItemMenu(description="Do transfer", action=self.do_transfer),
            "4": MenuBank.ItemMenu(description="Close account", action=self.close_account),
            "5": MenuBank.ItemMenu(description="Log out", action=self.logout),
            "0": MenuBank.ItemMenu(description="Exit", action=self.exit)
        }
        self._display_menu(self.menu)

    def _display_menu(self, menu: dict):
        continue_menu = True
        while continue_menu:
            for k, item in menu.items():
                print(f"{k}. {item.get_description()}")

            while (choice := input()) not in menu.keys():
                pass
            continue_menu = menu[choice].execute()
            print()

    def exit(self):
        #self._bank.get_all_accounts()
        print("\nBye!")
        exit()

    # region MENU FUNCTIONS
    def create_account(self):
        self._bank.create_account()
        return True

    def login_account(self):
        account = self._bank.log_in()
        if account is not None:
            self._account_logged = account
            print("\nYou have successfully logged in!\n")
            self._display_menu(self.menu_account)
            return True
        else:
            print("Wrong card number or PIN")
            return True

    # endregion

    # region MENU ACCOUNT FUNCTIONS
    def display_balance(self):
        balance = self._bank.get_balance(self._account_logged)
        print(f"\nBalance: {balance}")
        return True

    def add_income(self):
        income = int(input("Enter income:\n"))
        self._bank.add_income(self._account_logged, income)
        print("Income was added!\n")
        return True

    def do_transfer(self):
        print("\nTransfer")
        account_transfer = input("Enter card number:\n")
        try:
            if Card.validate_card(account_transfer) == False:
                raise CardNumberError
            # raise CardNotFoundError
            account_to_transfer = self._bank.get_account_by_number(account_transfer)
            if account_to_transfer.number == self._account_logged.number:
                raise SameCardError
            else:
                amount = int(input("Enter how much money you want to transfer:\n"))
                reserve = self._bank.get_balance(self._account_logged)
                if amount > reserve:
                    raise MoneyTransferError
                else:
                    self._bank.transfer_money(self._account_logged, amount, account_to_transfer)
        except CardNotFoundError:
            print("Such a card does not exist.")
        except CardNumberError:
            print("Probably you made a mistake in the card number. Please try again!")
        except SameCardError:
            print("You can't transfer money to the same account!")
        except MoneyTransferError:
            print("Not enough money!")
        else:
            print("Success!")
        finally:
            return True

    def close_account(self):
        self._bank.close_account(self._account_logged)
        return True

    def logout(self):
        self._account_logged = None
        print("You have successfully logged out!")
        return False
    # endregion


if __name__ == "__main__":
    bank = Bank()
    MenuBank(bank)
