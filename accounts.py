class Account:
    """
    A class to represent a bank account with login functionality.
    Attributes:
        name (str): The name of the account holder.
        account_pin (int): The unique PIN for login.
        balance (float): The current balance of the account.
    """
    def __init__(self, name: str, account_pin: int, balance: float = 100):
        self._account_name = name
        self._account_pin = account_pin 
        self._account_balance = balance

    def deposit(self, amount: float) -> bool:
        """Deposit money into the account if the amount is positive."""
        if amount > 0:
            self._account_balance += amount
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        """Withdraw money from the account if the amount is positive and sufficient funds exist."""
        if amount > 0 and amount <= self._account_balance:
            self._account_balance -= amount
            return True
        return False

    def get_balance(self) -> float:
        """Return the current balance of the account."""
        return self._account_balance

    def __str__(self) -> str:
        """Return a string representation of the account."""
        return f"Account Name: {self._account_name}, Account Balance: ${self._account_balance:.2f}"

class SavingsAccount(Account):
    """A subclass of Account that represents a savings account with a minimum balance."""
    MINIMUM = 100

    def __init__(self, name: str, account_pin: int):
        """Initialize the savings account with a minimum balance."""
        super().__init__(name, account_pin, self.MINIMUM)

    def withdraw(self, amount: float) -> bool:
        """Allow withdrawal only if it does not bring the balance below the minimum required."""
        if amount > 0 and self.get_balance() - amount >= self.MINIMUM:
            return super().withdraw(amount)
        return False

    def __str__(self) -> str:
        """Return a string representation of the savings account."""
        base_str = super().__str__()
        return f"SAVING ACCOUNT: {base_str}"
