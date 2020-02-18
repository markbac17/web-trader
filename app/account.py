import sqlite3
from app.util import get_price, hash_password, checkpw
from app.position import Position
from app.trade import Trade
from datetime import time
from random import randint
from app.view import transaction_error

class Account:

    tablename = 'accounts'
    dbpath = ''

    def __init__(self, **kwargs):
        self.account_id = kwargs.get('account_id')
        self.username = kwargs.get('username')
        self.password_hash = kwargs.get('password_hash')
        self.api_key = kwargs.get('api_key')
        self.balance = kwargs.get('balance')

    def save(self):
        if self.account_id is None:
            self._insert()
        else:
            self._update()

    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            sql = """
                    INSERT INTO {} (username, password_hash, balance, api_key)
                    VALUES (?,?,?,?);
                  """.format(self.tablename)
            curs.execute(sql, (self.username, hash_password(self.password_hash), self.balance, self.api_key))

    def _update(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            sql = """
                    UPDATE {} SET username=?, password_hash=?, balance=?, api_key=?
                    WHERE account_id=?;
                  """.format(self.tablename)
            values = (self.username, self.password_hash, self.balance, self.api_key, self.account_id)
            curs.execute(sql, values)

    def generate_api_key(self):
        return str(randint(10**19, 10**20-1))

    def retrieve_api_key(self):
        api_key = tuple(Account.select_one_where('WHERE account_id=?', (self.account_id,)))
        return api_key

    def get_balance(self):
        """ returns a list of Position objects """
        return Account.select_one_where('WHERE account_id=?', (self.account_id,))

    def update_balance(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            sql = """
                    UPDATE {} SET balance=?
                    WHERE account_id=?;
                  """.format(self.tablename)
            values = (self.balance, self.account_id)
            curs.execute(sql, values)

    @classmethod
    def api_authenticate(cls, user_api_key):
        return cls.select_one_where("WHERE api_key=?", (user_api_key,))

    @classmethod
    def login(cls, login_details):
        return cls.select_one_where("WHERE username=?", (login_details[0],))

    def buy(self, ticker, quantity):
        """
            BUY stock. checks if a stock exists in the user's positions and
            has sufficient shares. creates a new Trade and modifies the Position
            as well as adding to the user's balance. returns nothing
        """
        trade = Trade()
        current_price = get_price(ticker)
        mv = current_price * int(quantity)

        if self.balance < mv:
            transaction_error('Insufficient funds')
        else:
            trade.account_id = self.account_id
            trade.volume = quantity
            trade.ticker = ticker
            trade.price = current_price
            trade.market_value = mv

            self.balance -= mv
            self.update_balance()

            position = Position()
            position.account_id = self.account_id
            position.ticker = trade.ticker
            stored_position = Position.select_one_where('WHERE account_id=? and ticker=?',
                (position.account_id, position.ticker))

            if stored_position:
                position.position_id = stored_position.position_id
                position.num_shares = stored_position.num_shares
                position.num_shares += trade.volume
            else:
                position.num_shares = trade.volume
            trade.save()
            position.save()

    def sell(self, ticker, quantity):
        """
            SELL stock. checks if a stock exists in the user's positions and
            has sufficient shares. creates a new Trade and modifies the Position
            as well as adding to the user's balance. returns nothing
        """
        trade = Trade()
        current_price = get_price(ticker)
        mv = current_price * int(quantity)

        trade.account_id = self.account_id
        trade.volume = quantity
        trade.ticker = ticker
        trade.price = current_price
        trade.market_value = mv * -1

        self.balance += mv
        self.update_balance()

        position = Position()
        position.account_id = self.account_id
        position.ticker = trade.ticker
        stored_position = Position.select_one_where('WHERE account_id=? and ticker=?',
                                                (position.account_id, position.ticker))
        if stored_position:
            position.num_shares = stored_position.num_shares
            position.position_id = stored_position.position_id
            if stored_position.num_shares < trade.volume or stored_position.num_shares == 0:
                transaction_error('Not enough shares')
            else:
                trade.save()
                if stored_position:
                    position.num_shares = trade.volume
                else:
                    position.num_shares -= trade.volume
                position.save()
        else:
            transaction_error('Ticker {} is invalid'.format(trade.ticker))

    def get_positions(self):
        """
            returns a list of Position objects
        """
        return Position.select_all('WHERE account_id=?', self.account_id)

    def get_trades(self):
        """
            returns a list of Trade objects
        """
        return Trade.select_all('WHERE account_id=?', (self.account_id,))

    def get_position_for(self, ticker):
        return Position.select_one_where('WHERE account_pk=? AND ticker=?', (self.account_id, ticker))

    @classmethod
    def select_one_where(cls, where_clause, values):
        """
            selects an entry from our database based on its primary
        """
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            curs = conn.cursor()
            sql = f'SELECT * FROM {cls.tablename} {where_clause}'
            curs.execute(sql, values)
            row = curs.fetchone()
            return row

    def __repr__(self):
        return 'Account ID: {}, User name: {}, Password hash: {}, api_key: {}, Balance: {}'.format(self.account_id, self.username, self.password_hash, self.api_key, self.balance)
