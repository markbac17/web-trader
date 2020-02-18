from app.position import Position
from app.account import Account
from app.trade import Trade
from app import view
from bcrypt import checkpw
from app.util import get_price
from datetime import datetime


def main_loop():
    while True:
        choice = view.user_menu()
        if choice is None: # incorrect selection
            view.bad_input('Please select option')
        
        elif choice == '4': # exit
            view.goodbye()
            break

        elif choice == '1':
            login_input = view.login_username_pw()
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

                        choice = view.main_menu()
                        if choice is None:
                            view.bad_input('Please select option')
                        
                        elif choice == '1': # view account balance
                            view.display_balance(account.balance)

                        elif choice == '2': # deposit funds
                            account.balance += view.deposit()
                            Account.update_balance(account)
                        
                        elif choice == '3': # buy stock
                            buy_stock = view.trade_stock()
                            account.buy(buy_stock[0], buy_stock[1])
                        
                        elif choice == '4': #sell stock
                            buy_stock = view.trade_stock()
                            account.sell(buy_stock[0], buy_stock[1])
                        
                        elif choice == '5': # view positions
                            view.display_positions(Account.get_positions(account))

                        elif choice == '6': # view trades
                            view.display_trade_history(Account.get_trades(account))
                        
                        elif choice == '7': # lookup price of stock
                            ticker = view.lookup_ticker()
                            print("Ticker: {} is currently: ${}".format(ticker, get_price(ticker)))
                        
                        elif choice == '8': # See API Keys
                            view.display_api(Account.retrieve_api_key(account))

                        elif choice == '9': # logout
                            view.goodbye()
                        
                        else:
                            view.bad_input('Retry')
                else:
                    view.bad_input('Incorrect password')

            else:
                view.bad_input('Incorrect username')
        elif choice == '2': # login with api
            user_api_key = view.login_api_key()
            # print(user_api_key)
            user = Account.api_authenticate(user_api_key)
            view.display_user_from_api_key(user)
        elif choice == '3': # create new account
            account_details = view.create_account()
            account = Account()
            account.username = account_details[0]
            account.password_hash = account_details[1]
            account.balance = account_details[2]
            account.api_key = account.generate_api_key()
            Account.save(account)

def run():
    main_loop()