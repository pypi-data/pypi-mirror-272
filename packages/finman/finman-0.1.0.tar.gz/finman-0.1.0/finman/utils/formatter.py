from typing import List, Any, Dict
from ..models import Record, Wallet
from tabulate import tabulate
import click

# Function for creating table view of a record an printing it
# Depends on Tabulate library
def table_view(record: Any) -> str:
    """Creating a Table view of a record

    Args:
        record (Record | List[Dict | Records | List] | Dict): Record object refers to a invoice record

    Raises:
        ValueError: The function do not accept objects other than Record

    Returns:
        str: String formatted table to be used in terminal
    """
    # Defining Table header
    header = ["Date", "Category", "Amount", "Description"]
    # Checking the inputed type
    if isinstance(record, Record):
        # Getting Record Data
        data = [record._data()]
        
        # Return it as a table in string format
        return tabulate(data, headers=header, tablefmt='rounded_grid')
    # If the input was a list
    if isinstance(record, List):
        # Based of list's data types
        # If list of dictionaries
        if isinstance(record[0], Dict):
            records = []
            for _ in record:
                # Convert the Dict to list of data
                records.append(Record._unjsonfy(_))
            
            return tabulate(records, headers=header, tablefmt='rounded_grid')
        # If the list of Records
        elif isinstance(record[0], Record):
            # Get records data
            data = []
            for _ in record:
                data.append(record._data())
                
            return tabulate(data, headers=header, tablefmt='rounded_grid')
        else:
            # Print error message if list not contains values listed above
            raise ValueError(f"table_view function does not accept list of {type(record)} as input value.")
    # if the inputed type was Dictionary
    elif isinstance(record, Dict):
        # Convert it to list of record's data and return it
        return tabulate([Record._unjsonfy(record)], header, tablefmt='rounded_grid')
    else:
        # Otherwise, throw an error
        raise ValueError(f"table_view function does not accept input value of {type(record)}.")


# Same as table view but with additional ID column
def extended_table_view(record: Any = None) -> str:
    """Creating a Table view of a record

    Args:
        record (Record | List[Dict | Records | List] | Dict): Record object refers to a invoice record

    Raises:
        ValueError: The function do not accept objects other than Record

    Returns:
        str: String formatted table to be used in terminal
    """
    header = ["ID", "Date", "Category", "Amount", "Description"]
    if isinstance(record, Record):
        data = [record._data()]
        return tabulate(data, headers=header, tablefmt='rounded_grid')
    elif isinstance(record, List):
        if isinstance(record[0], Dict):
            records = []
            for _ in record:
                records.append(Record._unjsonfy_extended(_))

            return tabulate(records, headers=header, tablefmt='rounded_grid')
        else:
            return tabulate(record, headers=header, tablefmt='rounded_grid')
    elif isinstance(record, Dict):
        return tabulate([Record._unjsonfy_extended(record)], header, tablefmt='rounded_grid')
    else:
        raise ValueError(f"table_view function does not accept input value of {type(record)}")
    
# Table that shows up when editing a record compairing the original and edited tables    
def updater_table(original_record: Record, updated_record: Record) -> str:
    """A Table that compares an original record with edited (new values) record

    Args:
        original_record (Record): Original record to be edited
        updated_record (Record): The new record with new values to be comaperd

    Returns:
        str: String format comparsion table 
    """
    header = ["ID", "Date", "Category", "Amount", "Description"]
    arrow = ["\U0001F53B" for _ in range(4)]
    arrow.insert(0, "\033[92m=\033[0m")
    data = [original_record._data_extended(), arrow, updated_record._data_extended()]
    return tabulate(data, header, tablefmt="rounded_grid")

# A simplify version of click.style() function for text decoration that based on it
# Accepts bold and italic as **kwargs
# For more customization use original click.style()
def format_str(str: str, color: str, **kwargs) -> str:
    """A simplify version of click.style() function for text decoration that based on it

    Args:
        str (str): Input String to be decorated
        color (str): ['red', 'blue', 'yellow', 'green', white', 'cyan', 'magenta]
        and its bright versions as 'color_bright'

    Returns:
        str: Decorated string
    """
    # Managing kwargs if passed
    if kwargs:
        # Bold
        if "bold" in kwargs.keys() and kwargs["bold"]:
            return click.style(str, fg=color, bold=True)
        # Italic
        if "italic" in kwargs.keys() and kwargs["italic"]:
            return click.style(str, fg=color, italic=True)

    return click.style(str, fg=color)


# Balance table string
def balance_table(wallet: Wallet | List) -> str:
    """Function for creating table view of a Wllet data (will be updated with more functionality)

    Args:
        wallet (Wallet | List): A wallet data in varius typs

    Returns:
        str: Table as a string with needed values
    """
    header = [format_str("Balance", "yellow", bold=True),
              format_str("Income(+)", color="green"),
              format_str("Expense(-)", color="red")]
    if isinstance(wallet, Wallet):
        wallet_name = wallet._data()[0]
        data = [wallet._data()[1:]]
        
        return tabulate(data, header, tablefmt="heavy_grid")
    
    elif isinstance(wallet, List):
        if isinstance(wallet[0], Wallet):
            for _ in (wallet):
                data = [_._data()[1:]]
                
                return tabulate(data, header, tablefmt="heavy_grid")
    else:
        data = wallet[1:]
        
        return tabulate(data, header, tablefmt="heavy_grid")
    
