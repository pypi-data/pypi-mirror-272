from enum import Enum

# Category class inherited from Enum calss 
# To make it easier managing the category type of a record 
# making each category accessible with many formats 

class Category(Enum):
    def __new__(cls, symbol, code, ru_text, en_text):
        obj = object.__new__(cls)
        obj._value_ = symbol 
        obj.code = code
        obj.ru_text = ru_text
        obj.en_text = en_text
        return obj

    INCOME = ("+", "1", "Доход", "Income")
    EXPENSE = ("-", "0", "Расход", "Expense")


