from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

####################################################
# Database Setup

engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False})

# reflect an existing database into a new model
base = automap_base()


# reflect the tables
base.prepare(engine, reflect=True)

# View all of the classes that automap found
base.classes.keys()

# Save references to each table
measurement = base.classes.measurement

station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

####################################################

# Set up Flask 
app = Flask(__name__)

one_year_data = '2016-08-23'


@app.route("/")
def home():
    return (
    f"Welcome to the Hawaii Weather API!<br/>"
    f"The following Routes are available: <br>"
    f"/api/v1.0/precipitation - returns percipitation data for the dates between 8/23/2016 and 8/23/2017 <br>"
    f"/api/v1.0/stations - returns a list of weather stations <br>"
    )




#/api/v1.0/precipitation
#Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def percipitation():
    twl_month_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_data).all()
    return jsonify(twl_month_data)


#/api/v1.0/stations
#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    total_stations = session.query(station.station, station.name).all()
    return jsonify(total_stations)


#/api/v1.0/tobs
#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    active_station = session.query(measurement.date, measurement.station, measurement.tobs).filter(measurement.date >= one_year_data).all()
    return jsonify(active_station)

        


#/api/v1.0/<start> and /api/v1.0/<start>/<end>
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<date>")
def startDateOnly(date):
    day_temp_results = session.query(func.min(measurement.tobs),func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= date).all()
    return jsonify(day_temp_results)
    
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    multi_day_temp = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    return jsonify(multi_day_temp)


if __name__ == "__main__":
    app.run(debug=True)