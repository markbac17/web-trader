from app.position import Position
from app.account import Account
from app.trade import Trade
import app.view
from app.view import user_menu, login_username_pw, bad_input
from bcrypt import checkpw
from app.util import get_price
from datetime import datetime


def main_loop():
    while True:
        choice = user_menu()
        if choice is None: # incorrect selection
            bad_input('Please select option')
        elif choice == '4': # exit
            goodbye()
            break

        elif choice == '1':
            login_input = login_username_pw()
            verified_account = Account.login(login_input)
            if verified_account:
                db_password_hash = verified_account[2]
                password_verify = checkpw(login_input[1].encode(),
                    db_password_hash)
                if password_verify:
                    account = Account(account_id = verified_account[0])
                    account.username = verified_account[1]
                    account.balance = int(verified_account[3])
                    while True:
                        choice = main_menu()
                        if choice is None:
                            bad_input('Please select option')
                        elif choice == '1': # view account balance
                            display_balance(account.balance)
                        elif choice == '2': # deposit funds
                            account.balance += deposit()
                            Account.update_balance(account)
                        elif choice == '3': # buy stock
                            buy_stock = trade_stock()
                            account.buy(buy_stock[0], buy_stock[1])
                        elif choice == '4': #sell stock
                            buy_stock = trade_stock()
                            account.sell(buy_stock[0], buy_stock[1])
                        elif choice == '5': # view positions
                            display_positions(Account.get_positions(account))
                        elif choice == '6': # view trades
                            display_trade_history(Account.get_trades(account))
                        elif choice == '7': # lookup price of stock
                            ticker = view.lookup_ticker()
                            print("Ticker: {} is currently: ${}".format(ticker, get_price(ticker)))
                        elif choice == '8': # See API Keys
                            display_api(Account.retrieve_api_key(account))
                        elif choice == '9': # logout
                            goodbye()
                        else:
                            bad_input('Retry')
                else:
                    bad_input('Incorrect password')
            else:
                bad_input('Incorrect username')
        elif choice == '2': # login with api
            user_api_key = login_api_key()
            # print(user_api_key)
            user = Account.api_authenticate(user_api_key)
            display_user_from_api_key(user)
        elif choice == '3': # create new account
            account_details = create_account()
            account = Account()
            account.username = account_details[0]
            account.password_hash = account_details[1]
            account.balance = account_details[2]
            account.api_key = account.generate_api_key()
            Account.save(account)

def run():
    main_loop()
