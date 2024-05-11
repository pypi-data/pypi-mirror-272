import click
from ..utils.formatter import balance_table
from ..utils.data_utils import get_wallet_by_name # ,load_wallets # Will be added in future
from ..utils.config_utils import get_config_value
from ..config.config import WALLETS_DATA_FILE, CONFIG_FILE

# Balance Command 
# no arguments required (yet)
# Shows Wallet data in table view
# Balance, Total Income and Total Expense 



@click.command("balance",
               help="Displays your current Balance, Incomes and Exposes")
def balance():
    """Shows Balance, Total Income and Total Expense of default app wallet
    'Upcoming versions will have some options to work with more than one (default) wallet'
    """
    # Gets the default Wallet name from config.json applications configurations file
    wallet_name = get_config_value("default_wallet")
    # Prints Wallet's data in table view using balance_table() function by passing wallet's name
# ┏━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
# ┃   Balance ┃   Income(+) ┃   Expense(-) ┃
# ┣━━━━━━━━━━━╋━━━━━━━━━━━━━╋━━━━━━━━━━━━━━┫
# ┃         0 ┃           0 ┃            0 ┃
# ┗━━━━━━━━━━━┻━━━━━━━━━━━━━┻━━━━━━━━━━━━━━┛    
    click.echo(balance_table(get_wallet_by_name(wallet_name)))