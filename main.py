from flask import Flask, render_template, redirect, url_for, request
import csv
from datetime import date
import random 


app = Flask(__name__)
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

today = date.today()

def get_logs(): 
    # file closes after with block 
    with open('logs.csv', 'r') as file: 
        logs = []
        reader = csv.reader(file) 
        # skip the header row 
        next(reader) 
        # return the rest of the rows 
        for line in reader: 
            date = line[0]
            activity = line[1]
            footprint = line[2]
            notes = line[3]
            log = [date, activity, footprint, notes]
            logs.append(log)
        return logs 

@app.route('/', methods=["POST", "GET"])
def index():
    logs = get_logs()
    
    
    return render_template('index.html', logs=logs, today=today, tips=tips)

@app.route('/add_item', methods=['GET', 'POST']) 
def add_item(): 
    if request.method == 'POST':
        activity = request.form['activity']
        footprint = request.form['footprint']
        notes = request.form['notes']
    
        # file closes after with block 
        with open('logs.csv', 'a') as file: 
            writer = csv.writer(file)
           
            writer.writerow([today, activity, footprint, notes])
        return redirect(url_for('index'))
    else: 
        return render_template('add_item.html') 


    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# General posisble changes: 
# 1. Use random module for tips (daily tips) 

# Main Functionality Checklist
# 1. Add login page 
# 2. Setup account and SQL database
# 3. Summariser (use alert somehow) 
# 4. Add before date after date 

