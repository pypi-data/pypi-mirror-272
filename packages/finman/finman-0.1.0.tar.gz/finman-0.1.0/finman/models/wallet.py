from typing import List, Dict
from .record import Record
from .enums import Category

# Wallet class representing the base bank 
# Further versions will have ability of dealing with many wallets 
class Wallet:
    """
    Wallet class representing the base bank
    """ 
       
    def __init__(self, name: str, balance: float = 0.0, income: float = 0.0, expense: float = 0.0):
        """Intializes Wallet object by passing name [required]

        Args:
            name (str): Wallet Name 
            balance (float, optional): Base Balance  Defaults to 0.0.
            income (float, optional): Total Incomes Defaults to 0.0.
            expense (float, optional): Total Expenses Defaults to 0.0.
        """
        self.name = name 
        self.balance = balance
        self.income = income
        self.expense = expense
        
    
    # A function for getting wallets data in list format
    # Similar to Record._data()    
    def _data(self) -> List:
        """
        Returns:
            List: with wallets main data 
        """
        return [self.name, self.balance, self.income, self.expense]
    
    # Similar to Record._unjsonfy() method
    @staticmethod    
    def _unjsonfy(data: Dict) -> List:
        """Getting Dict of Wallet's data returns it in list format

        Args:
            data (Dict): Wallet's data 

        Raises:
            ValueError: If passed Dict misses some main Wallet data, it'll raise a ValueError

        Returns:
            List: Wallet's data in list format [name, balance, income, expense]
        """
        if isinstance(data, dict) and all(key in data for key in ['name', 'balance', 'income', 'expense']):
            return [data['name'], data['balance'], data['income'], data['expense']]
        else:
            raise ValueError("Invalid data format for unjsonfy method")
    
    
    # Similar to Record._jsonfy() method   
    def _jsonfy(self) -> Dict:
        """
        Returns:
            Dict: Returns Wallet's data in dictionary 
        """
        return {
            "name": self.name,
            "balance": self.balance,
            "income": self.income,
            "expense": self.expense
        }
        
    def update_data(self, record: Record) -> None:
        """Updating wallet's balance, income and expense based on given record

        Args:
            record (Record): Record to be added to the wallet
        """
        # Checking the category type for adding 
        # Income
        if record.category is Category.INCOME.en_text:
            self.balance += record.amount
            self.income += record.amount
        # Expense
        if record.category is Category.EXPENSE.en_text:
            self.balance -= record.amount
            self.expense -= record.amount
            
        
            
