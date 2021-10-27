import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///taste.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of tracker"""

    user_id = session["user_id"]

    records = db.execute(
        "SELECT restaurant, food, rate, region, style, time FROM tracker WHERE user_id = ? ORDER BY time DESC", user_id)

    return render_template("index.html", records=records)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology('Missing username')

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology('Missing password')

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology('Invalid username and/or password')

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")

        # Ensure user's input is not blank
        if not request.form.get("username"):
            return apology('Missing username')

        # Ensure the username does not already exist
        username_already_exists = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(username_already_exists) != 0:
            return apology('Username already exists')

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure user's input is not blank
        if not request.form.get("password"):
            return apology('Missing password')

        if not request.form.get("confirmation"):
            return apology('Missing confirmation')

        # Ensure if the passwords do not match
        if password != confirmation:
            return apology('Passwords do not match')

        # Insert the new user into database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username,
                   generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))

        # Bring the user to log in
        return render_template("login.html")
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Change password"""

    user_id = session["user_id"]
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")

        # Ensure user's input is not blank
        if not request.form.get("username"):
            return apology("missing username")

        # Ensure the username is correct
        username_data = db.execute("SELECT username FROM users WHERE id =?", user_id)
        if username != username_data[0]["username"]:
            return apology("invalid username")

        newpassword = request.form.get("newpassword")
        confirmation = request.form.get("confirmation")

        # Ensure user's input is not blank
        if not request.form.get("newpassword"):
            return apology("missing password")

        if not request.form.get("confirmation"):
            return apology("missing confirmation")

        # Ensure if the passwords do not match
        if newpassword != confirmation:
            return apology("passwords do not match")

        # Update the new password into database
        db.execute("UPDATE users SET hash = ? WHERE username = ?", generate_password_hash(
                   newpassword, method='pbkdf2:sha256', salt_length=8), username)

        # Bring the user to log in
        return render_template("login.html")
    else:
        return render_template("password.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add reviews"""
    if request.method == "POST":

        restaurant = request.form.get("restaurant")
        food = request.form.get("food")
        rate = request.form.get("rate")
        region = request.form.get("region")
        style = request.form.get("style")

        if not restaurant:
            return apology("missing restaurant")
        elif not food:
            return apology("missing food")
        elif not rate:
            return apology("missing rate")
        elif not region:
            return apology("missing region")
        elif not style:
            return apology("missing style")

        user_id = session["user_id"]

        db.execute("INSERT INTO tracker (user_id, restaurant, food, rate, region, style) VALUES(?, ?, ?, ?, ?, ?)",
                       user_id, restaurant, food, rate, region, style)

        return redirect("/")
    else:
        return render_template("add.html")


@app.route("/search_restaurant", methods=["GET", "POST"])
@login_required
def search_restaurant():
    """Search tracker by restaurant"""
    if request.method == "POST":

        restaurant = request.form.get("restaurant")

        if not restaurant:
            return apology("missing restaurant")

        user_id = session["user_id"]

        restaurants = db.execute("SELECT restaurant, food, rate, region, style, time FROM tracker WHERE user_id = ? AND restaurant LIKE ? ORDER BY rate DESC", user_id, "%" + restaurant + "%")

        return render_template("searched_restaurant.html", restaurants=restaurants)
    else:
        return render_template("search_restaurant.html")


@app.route("/search_food", methods=["GET", "POST"])
@login_required
def search_food():
    """Search tracker by food"""
    if request.method == "POST":

        food = request.form.get("food")

        if not food:
            return apology("missing food")

        user_id = session["user_id"]

        foods = db.execute("SELECT restaurant, food, rate, region, style, time FROM tracker WHERE user_id = ? AND food LIKE ? ORDER BY rate DESC", user_id, "%" + food + "%")

        return render_template("searched_food.html", foods=foods)
    else:
        return render_template("search_food.html")


@app.route("/search_rate", methods=["GET", "POST"])
@login_required
def search_rate():
    """Search tracker by rate"""
    if request.method == "POST":

        rate = request.form.get("rate")
        range = request.form.get("range")

        if not rate:
            return apology("missing rate")
        elif not range:
            return apology("missing range")

        user_id = session["user_id"]

        if range == ">":
            rates = db.execute("SELECT restaurant, food, rate, region, style, time FROM tracker WHERE user_id = ? AND rate > ? ORDER BY rate DESC", user_id, rate)

        elif range == ">=":
            rates = db.execute("SELECT restaurant, food, rate, region, style, time FROM tracker WHERE user_id = ? AND rate >= ? ORDER BY rate DESC", user_id, rate)

        elif range == "=":
            rates = db.execute("SELECT restaurant, food, rate, region, style, time FROM tracker WHERE user_id = ? AND rate = ? ORDER BY rate DESC", user_id, rate)

        elif range == "<=":
            rates = db.execute("SELECT restaurant, food, rate, region, style, time FROM tracker WHERE user_id = ? AND rate <= ? ORDER BY rate DESC", user_id, rate)

        elif range == "<":
            rates = db.execute("SELECT restaurant, food, rate, region, style, time FROM tracker WHERE user_id = ? AND rate < ? ORDER BY rate DESC", user_id, rate)

        return render_template("searched_rate.html", rates=rates)
    else:
        return render_template("search_rate.html")


@app.route("/search_region", methods=["GET", "POST"])
@login_required
def search_region():
    """Search tracker by region"""
    if request.method == "POST":

        region = request.form.get("region")

        if not region:
            return apology("missing region")

        user_id = session["user_id"]

        regions = db.execute("SELECT restaurant, food, rate, region, style, time FROM tracker WHERE user_id = ? AND region = ? ORDER BY rate DESC", user_id, region)

        return render_template("searched_region.html", regions=regions)
    else:
        return render_template("search_region.html")


@app.route("/search_style", methods=["GET", "POST"])
@login_required
def search_style():
    """Search tracker by style"""
    if request.method == "POST":

        style = request.form.get("style")

        if not style:
            return apology("missing style")

        user_id = session["user_id"]

        styles = db.execute("SELECT restaurant, food, rate, region, style, time FROM tracker WHERE user_id = ? AND style = ? ORDER BY rate DESC", user_id, style)

        return render_template("searched_style.html", styles=styles)
    else:
        return render_template("search_style.html")


@app.route("/random", methods=["GET", "POST"])
@login_required
def random():
    """Generate random choices from tracker"""
    if request.method == "POST":

        user_id = session["user_id"]

        random = db.execute("SELECT restaurant, food, rate, region, style FROM tracker WHERE user_id = ? ORDER BY random() LIMIT 1", user_id)

        return render_template("randomed.html", random=random)
    else:
        return render_template("random.html")