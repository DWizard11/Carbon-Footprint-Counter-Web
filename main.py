### 1. Importing Modules ###
from datetime import datetime, timedelta
import csv
import os
import random
import sqlite3
import uuid
from functools import wraps

from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash

### 2. Flask App Setup ###
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = "penguins"

### 3. Variable Definitions ###

## 3.1 CSV File Definition ##
global USER_CSV_DIR
USER_CSV_DIR = 'user_csv_files'
os.makedirs(USER_CSV_DIR, exist_ok=True)

## 3.2 Tips definiito 
tips = [
    "Switch off the lights when not in use", 
    "Keep air-conditioner at higher temperatures, or just use a fan", 
    "Limit the use of air travel", 
    "Unplug appliances that are not in use", 
    "Turn off electrical devices when not in use", 
    "Take shorter showers", 
    "Take the public transport or consider walking instead of using a car", 
    "Use LED lights instead of incandescent lights",
    "Limit the use of air travel", 
    "Air-dry your clothes instead of using a clothes dryer", 
    "Make use of natural light as much as possible"
       
       ]
global average_log
average_log = 732.9


today = datetime.now().strftime('%d %B %Y')
global selected_date 
selected_date = today 


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_logs(csvfile):
    total_footprint = 0
    logs = {}
    
    # file closes after with block 
    with open(csvfile, 'r') as file:
        log_diffs = {}
        reader = csv.reader(file)
        next(reader)  # Skip header

        log_csv = list(reader)

        for i in range(len(log_csv)):
            # Read the current line
            date = log_csv[i][0]
            activity = log_csv[i][1]
            footprint = log_csv[i][2]
            notes = log_csv[i][3]

            # Calculate total footprint
            total_footprint += int(footprint) if footprint else 0

            # Handle adding logs to dictionary
            if date not in logs:
                logs[date] = [[activity, footprint, notes]]
            else:
                logs[date].append([activity, footprint, notes])

    log_diff = abs(average_log - total_footprint)

    return (logs, total_footprint, log_diff)

def create_db(): 
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users(
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Password TEXT NOT NULL, 
            CSVFile TEXT NOT NULL
        );

    """)

    conn.commit() # commit changes to the database
    conn.close()
    
def read_db(): 
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM USERS;

    """)

    user_data = cursor.fetchall()
    print(user_data)
    conn.close()
    return user_data
    
@app.before_request
def before_request():
    protected_routes = ['home', 'add_item', 'delete_log', 'index']

    if 'user_id' not in session and request.endpoint in protected_routes:
        return redirect(url_for('login'))

@app.route("/")
def index(): 
    return redirect(url_for('login'))



@app.route("/login", methods=["GET", "POST"])
def login():
    logged_in = False
    if not os.path.isfile('./users.db'): 
        create_db()
        print("ITSHJJDJS RANNNN")
        
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Retrieve user data from the database
        user_data = read_db()
        
        # Check if username exists and password is correct
        for user in user_data:
            if username in user and check_password_hash(user[2], password):
                session["user_id"] = user
                print("IT RAN AAINN")
                logged_in = True
                return redirect(url_for('home'))
                
        if not logged_in: 
            print("NO TLOG IN")
            return render_template("login.html", message="Invalid username or password.")

    return render_template("login.html", message="")
    
@app.route('/home', methods=["POST", "GET"])
@login_required
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    
    if 'selected_date' not in session:
        session['selected_date'] = datetime.now().isoformat()
     
    selected_date_str = session.get('selected_date')

    # Check if the date is in the format that caused the error
    if selected_date_str:
        try:
            # Attempt to parse as ISO format
            selected_date = datetime.fromisoformat(selected_date_str)
        except ValueError:
            # Handle the specific format 'Mon, 19 Aug 2024 00:00:00 GMT'
            selected_date = datetime.strptime(selected_date_str, '%a, %d %b %Y %H:%M:%S %Z')
        formatted_date = selected_date.strftime('%d %B %Y')
        
    csvfile = os.path.join(USER_CSV_DIR, session["user_id"][3])

    if not os.path.isfile(csvfile):
        return render_template('index.html', message="User data file not found.")
    
    logs, total_footprint, log_diff = get_logs(csvfile)
    tip = random.choice(tips)
    
    print("HEHEHEHEHEHE", logs)
    return render_template('index.html', logs=logs, today=today, tip=tip, selected_date=selected_date, formatted_date=formatted_date, total_footprint=total_footprint, log_diff=log_diff, average_log=average_log)


@app.route('/add_item', methods=['GET', 'POST']) 
def add_item(): 
    csvfile = os.path.join(USER_CSV_DIR, session["user_id"][3])
    if request.method == 'POST':
        selected_date_str = session.get('selected_date')

        # Check if the date is in the format that caused the error
        if selected_date_str:
            try:
                # Attempt to parse as ISO format
                selected_date = datetime.fromisoformat(selected_date_str)
            except ValueError:
                # Handle the specific format 'Mon, 19 Aug 2024 00:00:00 GMT'
                selected_date = datetime.strptime(selected_date_str, '%a, %d %b %Y %H:%M:%S %Z')
            formatted_date = selected_date.strftime('%d %B %Y')
        
        activity = request.form['activity']
        footprint = request.form['footprint']
        notes = request.form['notes']
        
        # file closes after with block 
        with open(csvfile, 'a') as file: 
            writer = csv.writer(file)
            writer.writerow([formatted_date, activity, footprint, notes])
        
        return redirect(url_for('home'))
    else: 
        return render_template('add_item.html') 

@app.route('/add_date', methods=['GET'])
def add_date(): 
    selected_date_str = session.get('selected_date')

    # Check if the date is in the format that caused the error
    if selected_date_str:
        try:
            # Attempt to parse as ISO format
            selected_date = datetime.fromisoformat(selected_date_str)
        except ValueError:
            # Handle the specific format 'Mon, 19 Aug 2024 00:00:00 GMT'
            selected_date = datetime.strptime(selected_date_str, '%a, %d %b %Y %H:%M:%S %Z')
        
    selected_date = selected_date + timedelta(days=1)

    session['selected_date'] = selected_date.isoformat()
    
    return redirect(url_for('home'))

@app.route('/before_date', methods=['GET'])
def before_date(): 
    selected_date_str = session.get('selected_date')

    # Check if the date is in the format that caused the error
    if selected_date_str:
        try:
            # Attempt to parse as ISO format
            selected_date = datetime.fromisoformat(selected_date_str)
        except ValueError:
            # Handle the specific format 'Mon, 19 Aug 2024 00:00:00 GMT'
            selected_date = datetime.strptime(selected_date_str, '%a, %d %b %Y %H:%M:%S %Z')

    selected_date = selected_date - timedelta(days=1)
    session['selected_date'] = selected_date.isoformat()
    
    return redirect(url_for('home'))

@app.route('/delete_log', methods=['GET'])
def delete_log():
    csvfile = os.path.join(USER_CSV_DIR, session["user_id"][3])
    # file closes after with block 
    with open(csvfile, "r") as file: 
        reader = csv.reader(file)
        org_logs = []
        for line in reader: 
            org_logs.append(line)
    # file closes after with block 
    with open(csvfile, "w") as file:
        writer = csv.writer(file)
        writer.writerows(org_logs[:-1])

    return redirect(url_for('home'))


@app.route("/register", methods=["GET", "POST"])
def register():
    user_data = read_db()
    if request.method == "POST":
        # Validate form data
        username = request.form["username"]
        password = request.form["password"]
        repassword = request.form["repassword"]

        if not (username and password):
            return render_template("register.html", message="All fields are required.")
        for user in user_data: 
            if username in user:
                return render_template("register.html", message="Username already exists.")
        if repassword != password: 
            return render_template("register.html", message="Passwords do not match.")
                
        filename =  f"{username}_{uuid.uuid4().hex}.csv"
        filepath = os.path.join(USER_CSV_DIR, filename)

        # Saving user data to csv file
        with open(filepath, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Activity", "Footprint", "Notes"]) # Header 
            

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Store user data in the database
        # Your database insertion code goes here
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Users (Username, Password, CSVFile) 
            VALUES (?, ?, ?);
            
        """, (username, hashed_password, filename))

        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))
     
    return render_template("register.html", message="")



@app.route("/logout", methods=["POST"])
def logout():
    # Clear the session
    session.clear()
    return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# General posisble changes: 
# 1. Use random module for tips (daily tips) doen

# Main Functionality Checklist
# 1. Add login page done  
# 2. Setup account and SQL database 
# 3. Summariser (use alert somehow) done 
# 4. Add before date after date done

