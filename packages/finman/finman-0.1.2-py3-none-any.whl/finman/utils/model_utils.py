from datetime import datetime

DATE_NOW = datetime.now().strftime("%Y-%m-%d")

def generate_hex_id() -> str:
    # Get the current date and time
    now = datetime.now()
    # Convert datetime to a timestamp (number of seconds since epoch)
    timestamp = int(now.timestamp())
    # Convert the timestamp to hexadecimal
    hex_id = hex(timestamp)[2:]  # [2:] to strip the '0x' prefix
    return hex_id


     

