import sqlite3
import datetime

class Trade:
    tablename = 'trades'
    dbpath = ''

    def __init__(self, **kwargs):
        self.trade_id = kwargs.get('trade_id')
        self.account_id = kwargs.get('account_id')
        self.ticker = kwargs.get('ticker')
        self.volume = kwargs.get('volume')
        self.price = kwargs.get('price')
        self.time = kwargs.get('time', datetime.datetime.now().timestamp())
        self.market_value = kwargs.get('market_value')

    def save(self):
        if self.trade_id is None:
            self._insert()
        else:
            self._update()

    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            sql = """
                INSERT INTO {} (account_id, ticker,
                volume, price, time, market_value)
                VALUES (?,?,?,?,?,?);
                  """.format(self.tablename)
            curs.execute(sql, (self.account_id, self.ticker, self.volume, self.price, self.time, self.market_value))

    def _update(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            sql = """
                UPDATE {} SET account_id=?, ticker=?,
                volume=?, price=?, time=?, market_value=?
                WHERE account_id=?;
                """.format(self.tablename)
            values = (self.account_id, self.ticker, self.volume, self.price, self.time, self.market_value)
            curs.execute(sql, values)

    def delete(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            sql = """
                    DELETE FROM {} WHERE account_id =?;
                  """.format(self.tablename)
            curs.execute(sql, self.account_id)

    @classmethod
    def select_all(cls, where_clause, values):
        """
            select all trades
        """
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            curs = conn.cursor()
            sql = f"""
                    SELECT * FROM {cls.tablename} {where_clause};
                  """
            curs.execute(sql, values)
            rows = curs.fetchall()
            return [cls(**row) for row in rows]

    @classmethod
    def select_one(cls, where_clause, values):
        """
            selects an entry from trades based on its primary key
        """
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            curs = conn.cursor()
            sql = f"""
                    SELECT * FROM {cls.tablename} WHERE account_id=?;
                  """
            curs.execute(sql, values)
            row =  curs.fetchone()
            return cls(**row)

    def __repr__(self):
        return 'Account ID: {}, Ticker: {}, Volume: {}, Price: {}, Time: {}, Market value: {}' \
            .format(self.account_id,self.ticker,self.volume,self.price,self.time,self.market_value)