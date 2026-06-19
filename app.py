from flask import Flask, render_template, request, session, redirect, url_for
import pickle
import numpy as np
import pandas as pd
import csv
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "heartcare"
app.secret_key = "heartcare123"



@app.route("/")
def home():
    return render_template("login.html")

@app.route('/')
def index():
    return render_template('index.html')


# LOGIN
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    import csv
    with open("users.csv","r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0]==username and row[1]==password:
                session["user"] = username
                return render_template("index.html")

    return "Invalid login"

# SIGNUP
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        import csv
        with open("users.csv","a",newline="") as f:
            writer = csv.writer(f)
            writer.writerow([username,password])

        return redirect("/")   # go login page

    return render_template("signup.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# load model
model = pickle.load(open("heart_model.pkl", "rb"))


@app.route("/risk")
def risk():
    return render_template("risk.html")

@app.route("/remedies")
def remedies():
    return render_template("remedies.html")

@app.route("/emergency")
def emergency():
    return render_template("emergency.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route('/graph')
def graph():
    import random

    # Fake live sensor data (for demo)
    heart_rate = random.randint(72, 95)
    spo2 = random.randint(94, 100)
    temp = round(random.uniform(36.5, 37.5), 1)

    return render_template("graph.html",
                           heart_rate=heart_rate,
                           spo2=spo2,
                           temp=temp)

@app.route("/predict", methods=["POST"])
def predict():

    age = float(request.form["age"])
    sex = float(request.form["sex"])
    cp = float(request.form["cp"])
    bp = float(request.form["trestbps"])
    chol = float(request.form["chol"])
    sugar = float(request.form["fbs"])
    hr = float(request.form["thalach"])

    data = [[age, sex, cp, bp, chol, sugar, hr]]
    prediction = model.predict(data)
    return render_template("graph.html",
                       prediction_text=output,
                       heart_rate=int(request.form['thalach']),
                       temp=36.8,
                       spo2=98)

    # AI remedies logic
    if prediction[0] == 1:
        result = "⚠️ HIGH RISK of Heart Disease"
        remedies = [
            "Consult doctor immediately",
            "Avoid oily & junk food",
            "Do light exercise daily",
            "Reduce stress and take proper sleep",
            "Monitor BP regularly"
        ]
    else:
        result = "✅ LOW RISK - Healthy"
        remedies = [
            "Maintain regular exercise",
            "Drink enough water",
            "Eat fruits & vegetables",
            "Sleep 7-8 hours daily",
            "Continue healthy lifestyle"
        ]

    return render_template("risk.html", result=result, remedies=remedies)


@app.route("/send_alert", methods=["POST"])
def send_alert():
    name = request.form["name"]
    phone = request.form["phone"]

    message = f"🚨 Emergency alert sent to {name} ({phone})"

    return render_template("emergency.html", msg=message)
import random
from flask import jsonify

@app.route("/live-data")
def live_data():
    data = {
        "heart_rate": random.randint(70, 110),
        "temperature": round(random.uniform(36.0, 38.5), 1),
        "spo2": random.randint(94, 100),
        "bp": f"{random.randint(110,130)}/{random.randint(70,90)}"
    }
    return jsonify(data)
import random
from flask import jsonify

@app.route('/get_data')
def get_data():
    data = {
        "heart_rate": random.randint(70, 95),
        "bp": f"{random.randint(110,130)}/{random.randint(70,90)}",
        "temp": round(random.uniform(97, 99), 1)
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
