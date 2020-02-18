from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from app.account import Account

app = Flask(__name__)
app.secret_key = "this should be a random string"

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
    return render_template("balance.html", message="View Balance")

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
    return render_template("positions.html", message="View Positions")

@app.route("/trades", methods=["GET"])
def trades():
    return render_template("trades.html", message="View Trades")

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
        return render_template("user_opts.html", message=login_input)
    elif request.method == 'GET':
        return render_template('login.html', message="Login")

@app.route("/create", methods=["GET"])
def create():
    return render_template("create_account.html", message="Create Account")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    return redirect("/login")

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if 'login' in request.form:
#             return render_template("user_opts.html")
#         if 'create' in request.form:
#             return render_template("create_account.html")
#         else:
#             return "<h1>Bad</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
