#!/usr/bin/python3

from flask import Flask, request, Response, g
import sqlite3
import json

app = Flask(__name__)

DATABASE = "/var/www/python/weddingWebsite.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def str2bool(s):
    return str(s).lower() in ("true", "t", "y", "yes", "1")

@app.route('/getInfo', methods=["POST"])
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

@app.route('/updateInfo', methods=["POST"])
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

if __name__ == '__main__':
    app.run()
