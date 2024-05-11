import click
from ..utils.data_utils import get_record_by_id, update_record
from ..utils.formatter import extended_table_view, updater_table
from ..models import Category, Record

# Edit command 
# Gives the ability to edit a Record stored in JSON Databse file 
# by passing it's Unique ID

@click.command("edit",
               help="Edit a Record fetched by it's ID.")
@click.option("--id", "_id",
              help="ID of Record to be edited.",
              type=str,
              required=True)
def edit(_id):
    """Edits a Record saved in JSON Databse file
    takes only one option [ID]

    Args:
        _id (str): Uniqe ID of Record to be edited
    """
    # Prompt the user for an ID if not passed 
    if not _id:
        _id =click.prompt('Enter ID of the Record you want to edit', type=str)
    
    # Fetching Record with given ID 
    record_data = get_record_by_id(_id) # The function will return a Dict
    # Checks if there is a record with given ID
    if not record_data:
        # Prints a log to terminal if Record not found
        click.secho(f"ERROR404: No record found with ID {_id}", fg="red")
    # If there is a Record
    else:
        # Stores it in a Record Object
        original_record = Record(record_data["date"],
                                 record_data["category"],
                                 record_data["amount"],
                                 record_data["message"],
                                 _id) # Passing the given ID to avoid generating new one
        # Prints a table with fetched Record
        click.echo(extended_table_view(record_data))
        # Starts prompting the user to take new data
        while True:
            # Every prompt will ask the required data and show the default (original) one
            date_ = click.prompt("Enter new record date", default=record_data["date"])
            amount_ = click.prompt("Enter new amount", default=record_data["amount"])
            category_ = click.prompt("Enter new Category",
                                        type=click.Choice([category.en_text for category in Category]),
                                        default=record_data['category'])
            message_ = click.prompt("Enter record description message", default=record_data["message"])
            # Creating an updated (edited) version of the Record with same ID
            # Store it in Record Object 
            updated_record = Record(date_, category_, amount_, message_, _id)
            # Printing a comparison table to show the difference between Original and Edited
            click.echo(updater_table(original_record, updated_record))
            # Styles a confirmation prompt
            confirmation_text = click.style("Update record?", fg='yellow', bold=True)
            # Asks for confirmation to edit the Record
            confirmation = click.confirm(confirmation_text, default=True)
            # If confirmation approved
            if confirmation:
                # Updates the Record with new data
                # by replacing the original_record with updated_record
                update_record(_id, updated_record)
                # Prints a succession log
                click.secho("Record updated successfully!", fg='green')
                # Breaks the loop
                break
            # End of command exectution
            
            # If confirmation declined 
            else:
                # Cancle changes and prints a related terminal message
                click.secho("Changes Canceled, Editing Aborted!", fg="red")
                # Breaks the loop
                break
            
# End of Command Execution        