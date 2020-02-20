from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from app.account import Account
from app.position import Position
from app.trade import Trade
from app import view
from bcrypt import checkpw
from app.util import get_price
from datetime import datetime
from app.util import get_price, hash_password, checkpw
import os

DIR = os.path.dirname(__file__)
DBFILENAME = 'trader.db'
DBPATH = os.path.join(DIR, 'data', DBFILENAME)

Account.dbpath = DBPATH
Position.dbpath = DBPATH
Trade.dbpath = DBPATH

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/create_account', methods=["GET", "POST"])
def create2():
    if request.method == "GET":
        return render_template("create_account.html")
    else:
        name = request.form.get('name')
        password = request.form.get('password')
        if name == "mark" and password == "1234":
            session['username'] = name
            return redirect("user_options")
        else:
            return render_template("main_login.html", message="Login Error")
        return "<h1>POST succeeded</h1>"

@app.route("/", methods=["GET"])
def home():
    if 'username' in session:
        return render_template("user_opts.html")
    else:
        return redirect("/login")

@app.route("/balance", methods=["GET"])
def balance():
    balance = session.get('account_balance')
    return render_template("balance.html", message=balance )

@app.route("/deposit", methods=["GET"])
def deposit():
    return render_template("deposit.html", message="Deposit Funds")

@app.route("/buy", methods=["GET"])
def buy():
    return render_template("buy.html", message="Buy Shares")

@app.route("/sell", methods=["GET"])
def sell():
    return render_template("sell.html", message="Sell Shares")

@app.route("/positions", methods=["GET"])
def positions():
    positions = Account.get_positions(session.get('pk'))
    if positions:
        pass
    else:
        positions = "No positions available in this account"
    return render_template("positions.html", message=positions)

@app.route("/trades", methods=["GET"])
def trades():
    trades = Account.get_trades(session.get('pk')
    if trades:
        pass
    else:
        trades = "No trades available in this account"
    return render_template("trades.html", message=trades)

@app.route("/price", methods=["GET"])
def price():
    return render_template("price.html", message="Lookup Share Price")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        login_input = []
        login_input.append(name)
        login_input.append(password)
        verified_account = Account.login(login_input)
        if verified_account:
            db_password_hash = verified_account[2]
            password_verify = checkpw(login_input[1].encode(), db_password_hash)
            if password_verify:
                account = Account(account_id = verified_account[0])
                account.username = verified_account[1]
                account.balance = int(verified_account[3])
                session['pk'] = verified_account[0]
                session['account_balance'] = verified_account[3]
        return render_template("user_opts.html", message="Welcome " + account.username)
    elif request.method == 'GET':
        return render_template('login.html', message="Login")

@app.route("/create", methods=["GET"])
def create():
    account_details = []
    account_details.append("mark")
    account_details.append("1234")
    account_details.append(1000)
    account = Account()
    account.username = account_details[0]
    account.password_hash = account_details[1]
    account.balance = account_details[2]
    account.api_key = account.generate_api_key()
    Account.save(account)
    return render_template("create_account.html", message="Create Account")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    return redirect("/login")

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
