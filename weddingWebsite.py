#!/usr/bin/python3

from flask import Flask, request, Response, g, render_template, url_for, redirect, flash, abort
from flask_login import LoginManager, UserMixin, login_required, login_user
from uritools import urisplit, urijoin
import sqlite3
import json

app = Flask(__name__)
app.secret_key = "Secret key, change later"
login_manager = LoginManager()
login_manager.login_view = "login"
DATABASE = "/var/www/python/weddingWebsite.db"

class User(UserMixin):
    pass

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        c = db.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS `GuestList` (
            `FirstName`     TEXT NOT NULL,
            `LastName`      TEXT NOT NULL,
            `NumGuests`     INTEGER NOT NULL DEFAULT 0,
            `Vegetarian`    INTEGER NOT NULL DEFAULT 0,
            `PresentForDay1`        INTEGER NOT NULL DEFAULT 0,
            `PresentForDay2`        INTEGER NOT NULL DEFAULT 0
            );
            """);
        c.execute(""" CREATE UNIQUE INDEX IF NOT EXISTS `GuestNameIndex`
            ON `GuestList` (
            `FirstName`     ASC,
            `LastName`      ASC
            );
            """);
        c.close()
    return db

def str2bool(s):
    return str(s).lower() in ("true", "t", "y", "yes", "1")


def is_safe_url(target):
    ref_url = urisplit(request.host_url)
    test_url = urisplit(urijoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
            ref_url.host == test_url.host

@login_manager.user_loader
def user_loader(access_code):
    if access_code != "SAMPLE":
        return None

    user = User()
    user.id = access_code
    return user

@login_manager.request_loader
def request_loader(request):
    access_code = request.form.get("accessCode")
    if access_code is None:
        return None
    if access_code != "SAMPLE":
        return None

    user = User()
    user.id = access_code
    user.is_authenticated = True
    return user

@app.route("/getInfo", methods=["POST"])
@login_required
def get_guest_info():
    firstName = request.form["firstName"]
    lastName = request.form["lastName"]
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM GuestList WHERE FirstName = ? AND LastName = ?",
            (firstName, lastName))
    returnData = {}
    row = c.fetchone()
    if row is None:
        returnData["error"] = "Guest not found."
        response = Response(json.dumps(returnData), 404,
                mimetype="application/json")
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    returnData["firstName"] = row["FirstName"]
    returnData["lastName"] = row["LastName"]
    returnData["numGuests"] = int(row["NumGuests"])
    returnData["vegetarian"] = bool(int(row["Vegetarian"]))
    returnData["presentForDay1"] = bool(int(row["PresentForDay1"]))
    returnData["presentForDay2"] = bool(int(row["PresentForDay2"]))
    c.close()
    response = Response(json.dumps(returnData), mimetype="application/json")
    return response

@app.route("/updateInfo", methods=["POST"])
@login_required
def update_guest_info():
    firstName = request.form["firstName"]
    lastName = request.form["lastName"]
    numGuests = request.form["numGuests"]
    vegetarian = str2bool(request.form["vegetarian"])
    presentForDay1 = str2bool(request.form["presentForDay1"])
    presentForDay2 = str2bool(request.form["presentForDay2"])
    db = get_db()
    c = db.cursor()
    c.execute("UPDATE GuestList SET NumGuests = ?, Vegetarian = ?, "
            "PresentForDay1 = ?, PresentForDay2 = ? WHERE FirstName = ? "
            "AND LastName = ? LIMIT 1",
            (numGuests, vegetarian, presentForDay1, presentForDay2, firstName,
                lastName))
    returnData = {}
    response = Response(json.dumps(returnData), mimetype="application/json")
    return response

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.errorhandler(400)
def invalid_request(error):
    returnData = {}
    returnData["error"] = "Invalid request."
    response = Response(json.dumps(returnData), 400,
            mimetype="application/json")
    return response

@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        accessCode = request.form["accessCode"]
        if accessCode == "SAMPLE":
            user = User()
            user.id = accessCode
            login_user(user)
            nextPage = request.args.get('next')
            if nextPage and not is_safe_url(nextPage):
                return abort(400)
            return redirect(nextPage or url_for("index"))
        else:
            flash("Invalid access code.")
            return render_template("login.html")

@app.route("/")
@app.route("/index.html")
@login_required
def index():
    return render_template("index.html")

@app.route("/details.html")
@login_required
def details():
    return render_template("details.html")

@app.route("/registry.html")
@login_required
def registry():
    return render_template("registry.html")

@app.route("/rsvp.html")
@login_required
def rsvp():
    return render_template("rsvp.html")

@app.route("/faq.html")
@login_required
def faq():
    return render_template("faq.html")

login_manager.init_app(app)

if __name__ == '__main__':
    app.run()
