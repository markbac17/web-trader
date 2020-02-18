import os

def user_menu():
    print('Welcome to Terminal Trader.\n')
    print('User logon\n')
    print('1. Login with username')
    print('2. Login with API key')
    print('3. Create account')
    print('4. Exit\n')
    choice = input('Select option: ')
    os.system('clear')
    return choice

def login_username_pw():
    print('\nLogon with username & password\n')
    username = input('Enter username: ')
    password = input('Enter password: ')
    os.system('clear')
    return username, password

def login_api_key():
    print('\nLogon with API key\n')
    user_api_key = input('API key: ')
    os.system('clear')
    return user_api_key

def display_user_from_api_key(user):
    os.system('clear')
    if user:
        print('Account #:{}, User: {}, pw hash: {}, balance: {}, api key: {}'
            .format(user[0], user[1], user[2], user[3], user[4]))
    else:
        print(user)

def create_account():
    os.system('clear')
    print('\nCreate new account\n')
    username = input('Create user name: ')
    password = input('Create password: ')
    balance = input('Enter amount to deposit: ')
    return username, password, balance

def main_menu():
    print('Terminal Trader user options:\n' )
    print('1. View balance')
    print('2. Deposit')
    print('3. Buy')
    print('4. Sell')
    print('5. View positions')
    print('6. View trades')
    print('7. Lookup stock price')
    print('8. Lookup API key')
    print('9. Logout\n')
    choice = input('Enter choice: ')
    os.system('clear')
    return choice

def display_balance(balance):
    os.system('clear')
    print('\nAccount balance is: ${}\n'.format(balance))

def deposit():
    print('\nDeposit funds\n')
    balance = input('Enter amount to deposit: ')
    os.system('clear')
    return float(balance)

def display_trade_history(trade_history):
    print()
    for item in trade_history:
        print(item)
    print()

def display_positions(positions):
    print()
    for item in positions:
        print(item)
    print()

def display_api(api_key):
    print('\nAPI key is: {}\n'.format(api_key[4]))

def trade_stock():
    print()
    ticker = input('Enter stock ticker: ')
    quantity = input('Enter quantity: ')
    return ticker.upper(), int(quantity)

def lookup_ticker():
    print('\nLookup ticker\n')
    ticker = input('Lookup ticker: ')
    return ticker.upper()

def transaction_error(err_message):
    print(err_message)

def goodbye():
    print('\nThank you for using Terminal Trader')
    exit()

def bad_input(error_message):
    os.system('clear')
    print('\n{}. Retry!\n'.format(error_message))