import click
from ..utils.data_utils import search_records
from ..utils.formatter import extended_table_view

# List Command
# Lists Record that meets the given criteria (if passed)

# You can search by any criteria you want, even combine criterias
# Unlike Add command that have an option -c --category that takes category type [Income | Expense]
# Here u can specify the category by passing a flags [--income | --expense] to list one of them

# No defaults (Yet)
# By calling the command with no options it will display all saved records

@click.command("list",
               help="List Records")
@click.option("--date", "-d",
              help="Search by Date criteria YYYY-MM-DD",
              required=False,
              type=str)
@click.option("--income", 'category',
              help="Search for Incomes",
              flag_value="Income",
              required=False)
@click.option("--expense", 'category',
              help="Search in Expenses",
              flag_value="Expense",
              required=False)
@click.option("--amount", "-a",
              help="Search by Amount of money",
              required=False,
              type=float)
@click.option("--message", "-m",
              help="Search by description Message",
              required=False,
              type=str)
@click.option("--id",
              help="Search by Record ID criteria.",
              required=False,
              type=str)
def _list(date, category, amount, message, id):
    """Searches for records that meets given criteria(s)

    Args:
        date (str: YYYY-MM-DD): Search by Records Date
        category (flag: [--income | --expense]): Search in Incomes OR Expenses
        amount (float): Search by Amount of Money
        message (str): Search by message description of a record (not part of message)
        id (str): Search by Record's Unique ID (outputs one record if exists) 
    """
    # Creating a query Dict to pack all criterias (if more than one)
    query = {}
    # Declaring a list for displaying criterias with results
    filters = []
    filter_text = ''
    # Checking what criterias were passed with the command 
    if date:
        query['date'] = date
        filters.append(f'Date: {date}')
    if category and isinstance(category, str):
        query['category'] = category
        filters.append(f'Category: {category}')
    if amount:
        query['amount'] = amount
        filters.append(f'Amount: {amount}')
    if message:
        query['message'] = message
        filters.append(f'Discription: {message}')
    if id:
        query['id'] = id
        filters.append(f'Record ID: {id}')

    # Writing filters in one line
    for _ in filters:
        filter_text += f"{_}, "
    # Getting search results of query     
    results = search_records(query)
    # If there is data fetched 
    if results:
        # Print it in a table view
        result_table = extended_table_view(results)
        search_result_text = click.style("Search Results: ", fg="green")
        # Printing filters (criterias) above the table
        click.echo(f"{search_result_text}\nFilters: {filter_text[:-2]}")
        click.echo(result_table)
    # If no data fetched    
    else:
        # display a mesage that no matching records found 
        click.secho("ERROR404:No records found matching the criteria.", fg="red")


