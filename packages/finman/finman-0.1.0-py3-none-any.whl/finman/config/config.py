from pathlib import Path
# File with constants e.g. pathes to JSON database and application folders

MAIN_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = MAIN_DIR.joinpath("database")

CONFIG_FILE=MAIN_DIR.joinpath("config", "config.json")
RECORDS_DATA_FILE=DATA_DIR.joinpath("records.json")
WALLETS_DATA_FILE=DATA_DIR.joinpath("wallets.json")
