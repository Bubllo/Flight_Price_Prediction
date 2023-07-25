from datetime import date, timedelta
from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

label_map = {
    'Airline': {
        'Air Asia': 0,
        'Air India': 1,
        'GoAir': 2,
        'IndiGo': 3,
        'Jet Airways': 4,
        'Jet Airways Business': 5,
        'Multiple carriers': 6,
        'Multiple carriers Premium economy': 7,
        'SpiceJet': 8,
        'Trujet': 9,
        'Vistara': 10,
        'Vistara Premium economy': 11
    },
    'Source': {
        'Banglore': 0,
        'Chennai': 1,
        'Delhi': 2,
        'Kolkata': 3,
        'Mumbai': 4
    },
    'Destination': {
        'Banglore': 0,
        'Cochin': 1,
        'Delhi': 2,
        'Hyderabad': 3,
        'Kolkata': 4,
        'New Delhi': 5
    },
    'Total_Stops': {
        '1 stop': 0,
        '2 stops': 1,
        '3 stops': 2,
        '4 stops': 3,
        'non-stop': 4
    },
    'Additional_Info': {
        '1 Long layover': 0,
        '1 Short layover': 1,
        '2 Long layover': 2,
        'Business class': 3,
        'Change airports': 4,
        'In-flight meal not included': 5,
        'No check-in baggage included': 6,
        'No info': 7,
        'Red-eye flight': 8
    }
}

@app.route('/')
def home():
    return render_template('form.html',  label_map = label_map)

@app.route('/submit', methods=['POST'])
def register():
    date_dep = request.form["Dep_Time"]
    Journey_Day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
    Journey_Month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
    Journey_Year = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").year)
    
    Dep_Time_Hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
    Dep_Time_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
     
    date_arr = request.form["Arrival_Time"]
    Arrival_time_Hour = int(pd.to_datetime(date_arr, format ="%H:%M").hour)
    Arrival_time_Minutes = int(pd.to_datetime(date_arr, format ="%H:%M").minute)
    
    Duration_hour = abs(Arrival_time_Hour - Dep_Time_Hour)
    Duration_minutes = abs(Arrival_time_Minutes - Dep_Time_min)

    Total_stops = label_map["Total_Stops"][request.form["Total_Stops"]]
    
    Airline = label_map["Airline"][request.form["Airline"]]
    Source = label_map["Source"][request.form["Source"]]
    Destination = label_map["Destination"][request.form["Destination"]]
    Additional_Info = label_map["Additional_Info"][request.form["Additional_Info"]]
    
    with open("./Flight_random_forest_model.pkl","rb") as file:
            mp = pickle.load(file)
            
    prediction=mp.predict([[
            Airline,
            Source,
            Destination,
            Total_stops,
            Additional_Info,
            Journey_Day,
            Journey_Month,
            Journey_Year,
            Dep_Time_Hour,
            Dep_Time_min,
            Arrival_time_Hour,
            Arrival_time_Minutes,
            Duration_hour,
            Duration_minutes,
        ]])

    output=round(prediction[0],2)

    return render_template('success.html',value= str(output))

if __name__ == '__main__':
    app.run(debug=True)