import os
from app.account import Account
from app.position import Position
from app.trade import Trade
from app.controller import run
import bcrypt
import requests
# from app import ORM

DIR = os.path.dirname(__file__)
DBFILENAME = 'trader.db'
DBPATH = os.path.join(DIR, 'data', DBFILENAME)

print(DBPATH)

Account.dbpath = DBPATH
Position.dbpath = DBPATH
Trade.dbpath = DBPATH

run()
