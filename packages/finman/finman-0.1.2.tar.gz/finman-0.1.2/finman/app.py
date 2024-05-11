import click
from .cli import add, config, _list, edit, balance #, delete
from .utils.data_utils import ensure_data_files
import art


# The Base of CLI Application
# app() groups in itself many subcommands 
# Making the cli structure look like:
# App 
#   |_ balance
#   |_ add
#   |_ edit
#   |_ config
#   |_ search
##   |_delete 
# 
# Each command located in a separate {command}.py file 


@click.group(invoke_without_command=True) # Initing Click Group with the ability of calling the app without any subcommand
@click.pass_context # Getting access to applications context
def app(ctx):
    
    # This command checks database file existance on each command call
    # in case the files do not exist, it will create them
    ensure_data_files() 
    # If application called without invoking subcommands
    if ctx.invoked_subcommand is None:
        # It'll print Application name as green ASCII Art  
        click.secho(art.text2art("FINMAN", space=1), fg='green')
#         _____   ___   _   _   __  __      _      _   _ 
#        |  ___| |_ _| | \ | | |  \/  |    / \    | \ | |
#        | |_     | |  |  \| | | |\/| |   / _ \   |  \| |
#        |  _|    | |  | |\  | | |  | |  / ___ \  | |\  |
#        |_|     |___| |_| \_| |_|  |_| /_/   \_\ |_| \_|
#                                                               
    # Otherwise, it'll pass the execution to the proper subcommand 
    else:
        pass
    
# Adding subcommands to application group
app.add_command(add)
app.add_command(_list)
app.add_command(config)
app.add_command(edit)
app.add_command(balance)
# app.add_command(delete) # This command will be added in future


# P.S. About the ASCII Art: Inspired by Kali Linux Terminal Applications