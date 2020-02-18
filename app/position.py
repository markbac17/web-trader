import sqlite3
import os


class Position:
    tablename = 'positions'
    dbpath = ''

    def __init__(self, **kwargs):
        self.position_id = kwargs.get('position_id')
        self.account_id = kwargs.get('account_id')
        self.ticker = kwargs.get('ticker')
        self.num_shares = kwargs.get('num_shares')

    def save(self):
        if self.position_id is None:
            self._insert()
        else:
            self._update()

    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            sql = """
                    INSERT INTO {} (account_id, ticker, num_shares)
                    VALUES (?,?,?);
                 """.format(self.tablename)
            curs.execute(sql, (self.account_id, self.ticker, self.num_shares))

    def _update(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            sql = """
                    UPDATE {} SET num_shares=?
                    WHERE position_id=?;
                 """.format(self.tablename)
            values = (self.num_shares, self.position_id)
            curs.execute(sql, values)

    def delete(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            sql = """
                    DELETE FROM {} WHERE position_id =?;
                 """.format(self.tablename)
            curs.execute(sql, self.account_id)

    @classmethod
    def select_all(cls, where_clause, values):
        """select all entries from our database based on account_id
        """
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            curs = conn.cursor()
            sql = "SELECT * FROM {cls.tablename} {where_clause};"
            # print(sql, values)
            curs.execute(sql, (values,))
            positions = curs.fetchall()
            return [cls(**position) for position in positions]
                # return cls(**rows)

    @classmethod
    def select_one_where(cls, where_clause, values):
        """
            selects an entry from our database based on its primary key and ticker
        """
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            curs = conn.cursor()
            sql = "SELECT * FROM {cls.tablename} {where_clause};"
            curs.execute(sql, (values))
            position = curs.fetchone()
            if position is None:
                return False
            else:
                return cls(**position)

    def __repr__(self):
        return 'Position id: {}, Account ID: {}, Ticker: {}, Shares: {}'.format(self.position_id, self.account_id, self.ticker, self.num_shares)
