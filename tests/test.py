from unittest import TestCase
from app.account import Account

from data.seed import seed
from data.schema import schema
from os import remove

Account.dbpath = "test.db"

class TestTrader(TestCase):
    dbpath = "test.db"

    def setUp(self):
        schema(dbpath=self.dbpath)
        seed(dbpath=self.dbpath)

    def tearDown(self):
        remove(self.dbpath)

    def testCreation(self):
        user = Account(account_id=1, username="test_user", balance=1)
        self.assertIsInstance(user, Account, "__init__ returns user")
        self.assertEqual("test_user", user.username)

    def testCreation_api_key(self):
        user = Account(account_id=1, username="test_user", balance=1, api_key='12345678901234567890')
        self.assertIsInstance(user, Account, "__init__ returns user")
        self.assertEqual("12345678901234567890", user.api_key)

    def testInsert(self):
        user = Account(account_id="1", username="test_user", password_hash='somehash', balance=1, api_key='12345678901234567890')
        user.save()
        saved_user = Account.retrieve_api_key(user)
        self.assertEqual(user.api_key, saved_user[4])
