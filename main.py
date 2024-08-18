from flask import Flask, render_template, redirect, url_for, request, session
import csv
from datetime import datetime, timedelta
import random 
import os 
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os.path


app = Flask(__name__)
app.secret_key = "penguins"

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


today = datetime.now().date()
global selected_date 
selected_date = today 


def get_logs():
    total_footprint = 0
    logs = {}
    
    # file closes after with block 
    with open('logs.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        log_csv = list(reader)

        for i in range(len(log_csv)):
            # Read the current line
            date = datetime.strptime(log_csv[i][0], "%Y-%m-%d").date()
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
        CREATE TABLE Users(
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Password TEXT NOT NULL
        );

    """)

    conn.commit() # commit changes to the database
    conn.close()
    

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
        # Your database query code goes here
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM USERS;
            
        """)
        
        user_data = cursor.fetchall()
        print(user_data)
        conn.close()
        
        # Check if username exists and password is correct
        for user in user_data:
            if username in user and check_password_hash(user[2], password):
                session["user_id"] = user[0]
                print("IT RAN AAINN")
                logged_in = True
                return redirect(url_for('home'))
                
        if not logged_in: 
            print("NO TLOG IN")
            return render_template("login.html", message="Invalid username or password.")

    return render_template("login.html")
    
@app.route('/home', methods=["POST", "GET"])
def home():
    fileEmpty = os.stat('logs.csv').st_size == 0
    if not fileEmpty:
        logs, total_footprint, log_diff = get_logs()
    else: 
        logs, total_footprint, log_diff = ({}, 0, 0)
    tip = random.choice(tips)
    
    
    return render_template('index.html', logs=logs, today=today, tip=tip, selected_date=selected_date, total_footprint=total_footprint, log_diff=log_diff, average_log=average_log)

@app.route('/add_item', methods=['GET', 'POST']) 
def add_item(): 
    fileEmpty = os.stat('logs.csv').st_size == 0
    if request.method == 'POST':
        global selected_date
        activity = request.form['activity']
        footprint = request.form['footprint']
        notes = request.form['notes']
        
        # file closes after with block 
        with open('logs.csv', 'a') as file: 
            headers = ['Date', 'Activity', 'Footprint', 'Notes']
            writer = csv.writer(file)
            if fileEmpty: 
                writer.writerow(headers)
            writer.writerow([selected_date, activity, footprint, notes])
        
        return redirect(url_for('index'))
    else: 
        return render_template('add_item.html') 

@app.route('/add_date', methods=['GET'])
def add_date(): 
    global selected_date 
    selected_date += timedelta(days=1)
    return redirect(url_for('index'))

@app.route('/before_date', methods=['GET'])
def before_date(): 
    global selected_date 
    selected_date -= timedelta(days=1)
    return redirect(url_for('index'))

@app.route('/delete_log', methods=['GET'])
def delete_log():
    # file closes after with block 
    with open("logs.csv", "r") as file: 
        reader = csv.reader(file)
        org_logs = []
        for line in reader: 
            org_logs.append(line)
    # file closes after with block 
    with open("logs.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerows(org_logs[:-1])

    return redirect(url_for('index'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Validate form data
        username = request.form["username"]
        password = request.form["password"]

        if not (username and password):
            return render_template("register.html", message="All fields are required.")

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Store user data in the database
        # Your database insertion code goes here
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Users (Username, Password) 
            VALUES (?, ?);
            
        """, (username, hashed_password))

        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))
     
    return render_template("register.html")



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
# 1. Add login page 
# 2. Setup account and SQL database 
# 3. Summariser (use alert somehow) done 
# 4. Add before date after date done

