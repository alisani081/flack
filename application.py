from flask import Flask, render_template, request, url_for, session, flash, redirect
from models import *
#from flask_socketio import SocketIO, emit

from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://alisani:37277079@localhost/flack"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = b'"\x0eV\xb4\x97\n\x1e\xcd\x81\x9f\x9c]~I\xa4\xdb'
#socketio = SocketIO(app)

db.init_app(app)

@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password')
       
        # Validate user inputs
        if len(username) < 1:
           error = "Username is required"
        elif len(password) < 1:
            error = "Password is required"

        if error is not None:
            return render_template("login.html", error=error)

        # Get user account        
        user = User.query.filter_by(username=username).all()        
        if not user:
            error = "Incorrect login details"
        else:            
            for u in user:
                user_pwd = u.password
                user_id = u.id
            if not check_password_hash(user_pwd, password):
                error = "Incorrect login details"
        
        if error is None:
            session.clear()
            session['user_id'] = user_id
            session['username'] = username

            flash("Logged in successfully!", "success")
            return redirect(url_for('index')) 
            
    if 'user_id' in session:
       return redirect(url_for('index'))       
            
    return render_template("login.html", error=error)

@app.route("/signup", methods=["POST", "GET"])
def signup():
    error = None
    if request.method == "POST":
        username = request.form.get('username').strip()
        password = request.form.get('password')
        
        if len(username) < 1 or len(password) < 1:
           error = "All fields are required"
           
        elif len(password) < 6:
            error = "Password: Minimum of 6 characters required"
        
        # Check if user already exist
        if User.query.filter_by(username=username).count() > 0:
            error = f"Sorry, '{username}' already exist"
        
        # Register new user
        if error is None:
            password = generate_password_hash(password)
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()

            flash("Account created successfully! Use your details to login now.", 'success')

            return redirect(url_for('login'))           
    
    return render_template("signup.html", error=error)

@app.route("/")
def index():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    return render_template("index.html")

@app.route("/create")
def create():
    return render_template("dashboard/create.html")

@app.route("/explore")
def explore():
    return render_template("dashboard/explore.html")

@app.route("/channel/<int:channel_id>")
def channel(channel_id):
    return render_template("channel.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('login'))