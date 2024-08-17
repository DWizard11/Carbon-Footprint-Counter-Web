from flask import Flask, render_template, redirect, url_for, request
import csv
from datetime import datetime, timedelta
import random 
import os 


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
global average_log
average_log = 732.9


today = datetime.today().date()
global selected_date 
selected_date = today 

def get_logs(): 
    total_footprint = 0
    with open('logs.csv', 'r') as file: 
        logs = {}
        reader = csv.reader(file) 
        next(reader)  # Skip header
        log_csv = []

        for line in reader: 
            if not line[0]: 
                return logs
            log_csv.append(line)

        for i in range(len(log_csv)):
            date = datetime.strptime(log_csv[i][0], "%Y-%m-%d")
            activity = log_csv[i][1]
            footprint = log_csv[i][2]
            notes = log_csv[i][3]
            total_footprint += int(footprint)

            if i == len(log_csv) - 1:  # Last line
                if date not in logs: 
                    logs[date.date()] = [[activity, footprint, notes]]
                else: 
                    logs[date.date()].append([activity, footprint, notes])
                continue

            next_date = datetime.strptime(log_csv[i+1][0], "%Y-%m-%d")
            if date == next_date:
                if date not in logs: 
                    logs[date.date()] = [[activity, footprint, notes]]
                else: 
                    logs[date.date()].append([activity, footprint, notes])
            else:
                if date not in logs: 
                    logs[date.date()] = [[activity, footprint, notes]]
                else: 
                    logs[date.date()].append([activity, footprint, notes])

        print(logs)
        log_diff = abs(average_log - total_footprint)
        
        return (logs, total_footprint, log_diff)



@app.route('/', methods=["POST", "GET"])
def index():
    logs, total_footprint, log_diff = get_logs()
    tip = random.choice(tips)
    
    
    return render_template('index.html', logs=logs, today=today, tip=tip, selected_date=selected_date, total_footprint=total_footprint, log_diff=log_diff, average_log=average_log)

@app.route('/add_item', methods=['GET', 'POST']) 
def add_item(): 
    if request.method == 'POST':
        
        activity = request.form['activity']
        footprint = request.form['footprint']
        notes = request.form['notes']
    
        # file closes after with block 
        with open('logs.csv', 'a') as file: 
            writer = csv.writer(file)
           
            writer.writerow([datetime.strftime(today, '%Y-%m-%d'), activity, footprint, notes])
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
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# General posisble changes: 
# 1. Use random module for tips (daily tips) doen

# Main Functionality Checklist
# 1. Add login page 
# 2. Setup account and SQL database
# 3. Summariser (use alert somehow) done 
# 4. Add before date after date done

