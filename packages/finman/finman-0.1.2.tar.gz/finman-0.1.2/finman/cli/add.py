import click
from rich.prompt import Prompt
from ..utils.model_utils import DATE_NOW
from ..utils.formatter import table_view
from ..utils.data_utils import save_records, get_wallet_by_name, update_wallet
from ..utils.config_utils import get_config_value
from ..models import Record, Category, Wallet

# Add Command 
# used for adding a Record to JSON DataBase and updating Wallet's data accordingly
# U can add a record by specifing at least two things which are Category and Amount of Money

# Category does have a default value, it is an Expense Category [-]

# While amount doesn't have a directly default value, but u still can add a Record with 0.0 amount of money

# The discription will be prompted too, but the default will be ''
# so by pressing enter u can add an empty description message

# Default date value is datetime.now() 'Todays Date'


@click.command("add",
               help="Add a new record")
@click.option("--date", "-d",
              help="Record date YYYY-MM-DD",
              required=False,
              type=str,
              default=DATE_NOW) # Todays date
@click.option("--category", "-c", 
              help="Record category", 
              required=False, 
              default="-",                  # Default value of category is Expense
              show_default=True,
              type=click.Choice([category.value for category in Category]), # choose from Category(Enum) object values
              prompt="Record Category")
@click.option("--amount", "-a",
              help="Amount of money",
              required=False,
              type=float,
              default=0.0)                  # Amount's default is 0.0
@click.option("--message", "-m",
              help="Description message of a record",
              required=False,
              type=str,
              default='',
              prompt="Add record description")
# This option will be added in the future for managing many wallet's records
# @click.option("--wallet", "-w",
#               help="Defines wallet (to be added...)",
#               required=False,
#               type=str,
#               default=get_config_value('default_wallet'))
def add(date, category, amount, message):
    """Adds a Record, stores it in JSon DataBase and updates Wallet's data

    Args:
        date (str: YYYY-MM-DD): Records date, default to Today's Date
        category (str: [+ | -]): Income | Expense:Default 
        amount (float): Amount of Money
        message (str): A short description message about the Record
    """
    # Starting an inifint loop to gather all info about the record
    # in case if some options not passed directly with the command
    while True:  
        # Main one is : Amount of money, to avoid 0.0$ Record
        if not amount:
            amount = Prompt.ask("Amount of money :dollar:")
        
        # Initializing a Record Object with passed data    
        record = Record(date, Category(category).en_text, amount, message)
        # Printing the record in table view to show the data clearly [example below]
        click.echo(f"{table_view(record)}\n")
        # Styling a confirmation prompt
        confirmation_text = click.style("Save this record?", fg='yellow', bold=True)
        # Prompting confirmation for saving Records Data
        
        # Default = [YES]
        # press Enter to go 
        # or type [no] to aboard
        confirmation = click.confirm(confirmation_text, default=True)
        # If Confirmed
        if confirmation:
            # Saving record to JSON Database
            save_records(record)
            # Updating Wallet's data based on saved record
            update_wallet(get_config_value("default_wallet"), record)
            # Styling a Record ID to display it  
            record_id = click.style(f'{record._id}', bold=True, fg="cyan")
            saved_message_text = click.style('Saved Successfully!', fg='green')
            # Displaying successful record saving message
            click.secho(f"Record {record_id} {saved_message_text}", fg='green')
            
            #Breaking loop
            break
# End of command execution
        # In case the confiramtion declined
        else:
            # Prompt the user asking him if he want to add Record again
            try_again_text = click.style("Do you want to enter the record again?", fg='yellow')
            try_again = click.confirm(try_again_text, default=False)
            
            # Default = NO
            # press Enter to aboard and end command execution
            # or type [yes] to procced with adding record again
            
            # if Declined [pressed enter | typed no]
            if not try_again:
                # Displaying message about cancelation
                click.secho("Record entry has been cancelled.", fg='red')
                break
            #End of command execution
            
            # If agreed [typed yes]
            else:
                # The application will prompt the user with questions to gather information about Record 
                date = click.prompt("Enter records date", default=DATE_NOW)
                category = click.prompt("You Got or Paid",
                                        type=click.Choice([category.value for category in Category]),
                                        default="-",
                                        show_default=False)
                amount = Prompt.ask("How much money :dollar:")
                message = click.prompt("Record Description", default='')
            # In this case you can exit either by pressing [Ctrl+C] or by answering the next confirmation question with [NO]
   
   # Example of Record's table view             
# ╭────────────┬────────────┬──────────┬───────────────╮
# │ Date       │ Category   │   Amount │ Description   │
# ├────────────┼────────────┼──────────┼───────────────┤
# │ 2024-05-09 │ Income     │     5000 │ Pop-corn      │
# ╰────────────┴────────────┴──────────┴───────────────╯

# Save this record? [Y/n]: 
# Record 663cda40 Saved Successfully!

# P.S.: Yes, this is the minimal price of pop-corn in Syria, tbh, it's only ~0.3 $ LOL