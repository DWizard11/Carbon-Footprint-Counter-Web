from flask import Flask, render_template, redirect, url_for, request
import csv
from datetime import date


app = Flask(__name__)
tips = ["Switch off the lights when not in use"]
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

    
    return render_template('index.html', today=today, tips=tips)

@app.route('/add_item', methods=['GET']) 
def add_item(): 

    return render_template('add_item.html') 

    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# General posisble changes: 
# 1. Use random module for tips? 
