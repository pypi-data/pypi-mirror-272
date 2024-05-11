# Main data manipulation utilities and functions 
from typing import Dict, List
from pathlib import Path
import json
import os
from finman.config.config import DATA_DIR, RECORDS_DATA_FILE, WALLETS_DATA_FILE
from .config_utils import update_config
from .formatter import format_str
from finman.models import Record, Wallet
import click
import art
from time import sleep


# This function runs only if the wallets.json not exist
def first_run() -> Wallet:
    """Prompting wallet name from user on first run or when wallet.json file deleted

    Returns:
        Wallet: Wallet object representing the wallet for further record adding
    """
    # Priniting ASCII art app name 
    # Prompting a name for the wallet 
    # Initializing wallet object with given name
    click.secho("\nWelcome to ", fg="green")
    click.secho(art.text2art("FINMAN", space=1), fg="red")
    click.secho("Please enter a name for your wallet\n", fg="green")
    name = click.prompt(format_str("You can change it later", "green"), type=str, default="My_wallet")
    return Wallet(name=name)


def ensure_data_files() -> None:
    """Checking json databses within databse directorty, creates them if not exist
    """
    # Ensure the data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)  
    if not os.path.exists(RECORDS_DATA_FILE):
        with open(RECORDS_DATA_FILE, 'w') as file:
            # Create an empty dict for records
            json.dump({}, file)  
    if not os.path.exists(WALLETS_DATA_FILE):
        with open(WALLETS_DATA_FILE, 'w') as file:
            data = {}
            wallet = first_run()
            data[wallet.name] = wallet._jsonfy()
            sleep(0.5)
            update_config('default_wallet', wallet.name)
            json.dump(data, file, indent=4)


def load_wallets(filename: str) -> List:
    ensure_data_files()
    wallets = []
    with open(filename, 'r') as f:
        loaded_wallets = json.load(f)
        for name, wallet in loaded_wallets.items():
            wallets.append(wallet)
    return wallets


def get_wallet_by_name(wallet_name: str) -> Wallet:
    wallets = load_wallets(WALLETS_DATA_FILE)
    for _ in wallets:
        if _["name"] == wallet_name:
            wallet_data = Wallet._unjsonfy(_)
            return Wallet(wallet_data[0], wallet_data[1], wallet_data[2], wallet_data[3])
    return None

def update_wallet(wallet_name: str, record: Record) -> None:
    data = {}
    
    with open(WALLETS_DATA_FILE, 'r') as file:
        data = json.load(file)
    
    wallet = get_wallet_by_name(wallet_name)
    wallet.update_data(record)
    
    data[wallet.name] = wallet._jsonfy()
    
    with open(WALLETS_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)
        

def load_records(filename: str) -> List:
    ensure_data_files()
    records = []
    with open(filename, 'r') as f:
        loaded_data = json.load(f)
        for id, record in loaded_data.items():
            records.append(record)
    return records


def load_records_extended(filename: str) -> List:
    ensure_data_files()
    records = []
    with open(filename, 'r') as f:
        loaded_data = json.load(f)
        for id, record in loaded_data.items():
            record["id"] = id
            records.append(record)
    return records


def save_records(records):
    data = {}
    with open(RECORDS_DATA_FILE, 'r') as file:
            data = json.load(file)
    # Update the data with new records
    if isinstance(records, list):
        for record in records:
            data[record._id] = record._jsonify()

    if isinstance(records, Record):
        data[records._id] = records._jsonfy()
    
    # Write the updated data back to the file
    with open(RECORDS_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)



def search_records(query):
    all_records = load_records_extended(RECORDS_DATA_FILE)
    filtered_records = []
    for record in all_records:
        match = True
        if isinstance(record, dict):
            record_dict = record
        else:
            record_dict = record.__dict__
        for key, value in query.items():
            if key not in record_dict or str(record_dict.get(key)) != str(value):
                match = False
                break
        if match:
            filtered_records.append(record)
    return filtered_records


def get_record_by_id(_id: str) -> Dict:
    loaded_data = load_records_extended(RECORDS_DATA_FILE)
    for record in loaded_data:
        if record["id"] == _id:
            return record
    return None

def update_record(_id: str, updated_record: Record):
    data = {}
    with open(RECORDS_DATA_FILE, 'r') as file:
            data = json.load(file)
    
    data[_id] = updated_record._jsonfy()
    
    with open(RECORDS_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)
    