# Configuration file utilities 
from typing import Dict
from ..config.config import CONFIG_FILE
import json
import click



# Fetching configuration file to Dict and returning it
def load_config() -> Dict:
    """Fetching configurations (config.json)

    Returns:
        Dict: congi.json in Dict format
    """
    # Checks configurations file existanse
    # If found
    try:
        # Open in Read mode
        with open(CONFIG_FILE, 'r') as file:
            # Load JSON file format and returns it
            config = json.load(file)
            return config
    # If file not found prints error meassage
    except FileNotFoundError:
        print("Error404: Configuration file 'config.json' not found.")
        

# Updating configuration file with custome configs
def update_config(config_param: str, config_value: str) -> None:
    """Changing Configuration parameter in config.json

    Args:
        config_param (str): The parameter to be changed
        config_value (str): New value
    """
    # Getting the configurations as a Dict
    config = load_config()
    # If the configuration parameter to be edited exists
    if config[config_param]:
        # It'll change it's value to the custom passed value
        config[config_param] = config_value
        # Writes changes to config.JSON
        with open(CONFIG_FILE, 'w') as file:
            json.dump(config, file, indent=4)
    # Otherwise, it will prints that the passed configuration parameter not found
    else:
        click.secho(f"{config_param} not found in configuration file.", fg='red')
        
        # Getting a specific config parameter value       
def get_config_value(config_param: str) -> str:
    """Fetching configuration's parameter value

    Args:
        config_param (str): The configuration parameter 

    Returns:
        str: It's value
    """
    # Loading configurations file 
    config = load_config()
    # If there is a configuration parameter u asking for 
    if config[config_param]:
        # It'll return it's value
        return config[config_param]
    # Otherwise, prints error message
    else:
        click.secho(f"{config_param} not found in configuration file.", fg='red')

