import os

from flask import Flask, render_template, request, url_for
#from flask_socketio import SocketIO, emit

app = Flask(__name__)
#app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
#socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/create")
def create():
    return render_template("dashboard/create.html")

@app.route("/view")
def view():
    return render_template("dashboard/view.html")

@app.route("/explore")
def explore():
    return render_template("dashboard/explore.html")

@app.route("/channel/<int:channel_id>")
def channel(channel_id):
    return render_template("channel.html")
