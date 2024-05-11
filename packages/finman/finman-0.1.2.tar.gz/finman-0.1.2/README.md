# FinanceManager - finman
(PRE-RELEASE)

     _____   ___   _   _   __  __      _      _   _ 
    |  ___| |_ _| | \ | | |  \/  |    / \    | \ | |
    | |_     | |  |  \| | | |\/| |   / _ \   |  \| |
    |  _|    | |  | |\  | | |  | |  / ___ \  | |\  |
    |_|     |___| |_| \_| |_|  |_| /_/   \_\ |_| \_|

# Personal Finance Managing CLI Application 

This project is a CLI application for managing personal finances. It includes features for tracking income, expenses, and overall balance.

## Installation

#### **Recommanded to use pipx for installation to avoid dependency conflicts**

It will install the application in an isolated environment, avoiding any potential dependency conflicts 
with your systems python packages.

```bash
pipx install finman
```
If pipx is not installed, follow the [Official pipx Installation Guide](https://pipx.pypa.io/stable/#install-pipx)

Note: pipx should be added in your PATH, for the application to be accessable globaly 

## Usage

To invoke the command use:
 - `finman` if installed using pipx 
 - `python __main__.py` if used basic install (git clone...), it's CLI's Entry Point.

###     Manage your financial records with FINMAN within your Terminal 
- Monitor your balance, total income and expense
```bash
finman balance # Returns budget data 
```
- Add a record specifying the amount of money and category (Income / Expense)
```bash
finman add -a '500' -c - -m Fruits # Adds and 500 expense for Freuits 
# -c takes operation symbol as an argument (+ / -) 
```
- Edit an existing saved records
```bash
finman edit --id 687sdf7 # Starts editing Record with ID 687sdf7
```
- List all records or find a spicific one by adding filters 
```bash
finman list # Lists all records
finman list --income -a 200 # Lists all incomes with amount 200
```

### For more Information about each command, see 
```bash
finman [command] --help
```

## Author
- Idris Taha
- Email: dri.taha24@gmail.com
- Telegram: @idristaha

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
