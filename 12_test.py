class BankAccount:

    def __init__(self, name, account_number, pin, balance=0):
        self.name = name
        self.account_number = account_number
        self.__pin = str(pin)
        self.__balance = balance
        self.failed_attempts = 0
        self.account_locked = False
        self.transactions = []

    def authenticate(self, pin):

        if self.account_locked:
            print("Account is locked.")
            return False

        if str(pin) == self.__pin:
            self.failed_attempts = 0
            return True

        self.failed_attempts += 1

        remaining = 3 - self.failed_attempts

        if self.failed_attempts >= 3:
            self.account_locked = True
            print("Account locked due to multiple failed attempts.")
        else:
            print(f"Invalid PIN. Attempts left: {remaining}")

        return False

    def deposit(self, amount):

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        self.__balance += amount
        self.transactions.append(f"Deposit: ₹{amount}")

        print(f"₹{amount} deposited successfully.")

    def withdraw(self, amount, pin):

        if not self.authenticate(pin):
            return

        if amount <= 0:
            print("Invalid amount.")
            return

        if amount > self.__balance:
            print("Insufficient balance.")
            return

        self.__balance -= amount
        self.transactions.append(f"Withdrawal: ₹{amount}")

        print(f"₹{amount} withdrawn successfully.")

    def show_balance(self, pin):

        if not self.authenticate(pin):
            return

        print(f"Current Balance: ₹{self.__balance}")

    def mini_statement(self, pin):

        if not self.authenticate(pin):
            return

        print("\n------ MINI STATEMENT ------")

        if len(self.transactions) == 0:
            print("No transactions found")
        else:
            for txn in self.transactions:
                print(txn)

        print("----------------------------")

account = BankAccount(
        "Saravanan",
        "SB10001",
        "1234",
        10000
    )

account.deposit(5000)

account.withdraw(3000, "1234")

account.show_balance("1234")

account.mini_statement("1234")