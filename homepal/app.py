import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from datetime import datetime
from datetime import date

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///homepal.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")
#Add category
category = ["No Category", "Fruits", "Vegetables", "Legumes", "Meat", "Fish", "Sea Food", "Bread and Cereals", "Dairy Products", "Deserts and Sugary Foods", "Snacks", "Spices and Condiments", "Drinks", "Households and Cleaning", "Health Care Medications", "Personal Care"]

#Add units
units=["No unit", "Piece", "Pack", "Box", "Bag", "lb", "oz", "g", "kg", "bottle", "can", "L", "mL", "gal"]

#Add location
locations=["Not stored","Refrigerator", "Freezer", "Pantry", "Counter", "Top Cupboard", "Bottom Cupboard", "Larder", "Cellar"]

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT symbol, name, SUM(shares) as shares, price, Total FROM transactions  WHERE user_id = ? GROUP BY symbol HAVING (SUM(shares)) > 0", user_id)
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]
    return render_template("index.html", transactions=transactions, cash=cash)
@app.route("/products", methods=["GET", "POST"])
@login_required
def products():
    """Get Item."""
    if request.method == "GET":
        return render_template("products.html", category=category, units=units, locations=locations)
    else:

        # symbol = request.form.get("symbol")
        # if not symbol:
        #     return apology("Please enter symbol")
        # stock = lookup(symbol)

        # if stock == None:
        #     return apology("Symbol not found")
        # else:
        #     return render_template("quoted.html", name=stock["name"], price=stock["price"], symbol=stock["symbol"])
        user_id=session["user_id"]
        Category = request.form.get("category")
        product=request.form.get("product").upper()
        quantity=int(request.form.get("quantity"))
        unit=request.form.get("units")
        date_purchased=request.form.get("datepurchased")
        best_before=request.form.get("bestbefore")
        if not Category:
            return apology("Select Category")
        if not product:
            return apology("Enter Product Name")
        if not quantity:
            return apology("Enter Quantity")
        if not unit:
            return apology("Choose Unit")
        if not date_purchased:
            return apology("Choose Date Purchased")
        if not best_before:
            return apology("Choose Expiry Date or No expiry")
        if best_before == "Noexpirydate":
            location=request.form.get("locations")
            price=int(request.form.get("price"))
            expiring_in="--"
            db.execute("INSERT INTO consumption (user_id, category, product, quantity, datepurchased, bestbefore, location, price,days, unit) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user_id,Category, product, quantity, date_purchased, best_before, location, price, expiring_in, unit)
            return redirect("/consumption")

        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        expiring_in=(datetime.strptime(best_before, "%Y-%m-%d") - datetime.strptime(d1, "%Y-%m-%d")).days
        location=request.form.get("locations")
        price=int(request.form.get("price"))


        db.execute("INSERT INTO consumption (user_id, category, product, quantity, datepurchased, bestbefore, location, price,days, unit) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user_id,Category, product, quantity, date_purchased, best_before, location, price, expiring_in, unit)
        return redirect("/consumption")

@app.route("/consumption", methods=["GET", "POST"])
@login_required
def consumption():

    """Consumption of products"""
    # if request.method == "GET":
    #     return render_template("consumption.html")
    # else:
    #     symbol = request.form.get("symbol")
    #     shares = int(request.form.get("shares"))
    #     if not symbol:
    #         return apology("Please enter symbol")
    #     stock = lookup(symbol)
    #     if stock == None:
    #         return apology("Symbol not found")
    #     if shares < 1:
    #         return apology("Please enter a positive number")

    #     transaction_value = shares * stock["price"]

    #     user_id = session["user_id"]
    #     user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    #     user_cash = user_cash_db[0]["cash"]

    #     if user_cash >= transaction_value:
    #         updt_cash = user_cash - transaction_value
    #         db.execute("UPDATE users SET cash = ? where id = ?", updt_cash, user_id)
    #         date = datetime.datetime.now()

    #         db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date, total, name) VALUES (?, ?, ?, ?, ?, ?,?)", user_id, stock["symbol"], shares, stock["price"], date, shares*stock["price"], stock["name"])

    #         flash("Brought!")
    #         return redirect("/")
    #     else:
    user_id = session["user_id"]
    consumption = db.execute("SELECT product,category, quantity, days, location, unit FROM consumption  WHERE user_id = ? ORDER BY datepurchased", user_id)

    return render_template("consumption.html", consumption=consumption)







@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id=session["user_id"]
    transactions = db.execute("SELECT symbol, name, shares, price, date FROM transactions  WHERE user_id = ?", user_id)
    return render_template("history.html", transactions=transactions)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")







@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username=request.form.get("username")
        password=request.form.get("password")
        confirmation=request.form.get("confirmation")

        if not username:
            return apology("Please enter Username")
        if not password:
            return apology("Please enter Password")
        if not confirmation:
            return apology("Please enter Confirm Password")
        if password != confirmation:
            return apology("Passwords donot match")

        hash = generate_password_hash("password")

        try:
            new_user=db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("Username exists")
        # Remember which user has logged in
        session["user_id"] = new_user

        # Redirect user to home page
        return redirect("/")







@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_of_user = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)

        return render_template("sell.html", symbols_of_user=symbols_of_user)
    else:
        user_id = session["user_id"]
        stock_to_sell=request.form.get("symbols_of_user")
        shares = int(request.form.get("shares"))
        stock=lookup(stock_to_sell)
        if stock == None:
            return apology("Symbol not found")
        owned_shares=db.execute("SELECT SUM(shares) as shares FROM transactions WHERE user_id = ? AND symbol = ?", user_id, stock["symbol"])
        if not stock_to_sell:
            return apology("Please choose symbol")

        if shares < 1:
            return apology("Please enter a positive number")
        if owned_shares[0]["shares"] < shares:
            return apology("You don't own this number of stocks")



        transaction_value = shares * stock["price"]

        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]
        updt_cash = user_cash + transaction_value


        db.execute("UPDATE users SET cash = ? where id = ?", updt_cash, user_id)
        date = datetime.datetime.now()

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date, total, name) VALUES (?, ?, ?, ?, ?, ?,?)", user_id, stock["symbol"], (-1)*shares, stock["price"], date, (-1)*shares*stock["price"], stock["name"])

        flash("Sold!")
        return redirect("/")

@app.route("/deregister", methods=["POST"])
def deregister():

    # Forget registrant
    id = request.form.get("id")
    print(id)
    if id:
        db.execute("DELETE FROM registrants WHERE id = ?", id)
    return redirect("/consumption")






