#################################################
# Import dependencies
#################################################
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Home page
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
    	"Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you need to do some climate analysis on the area. Please use the below API routes to view climate data according to stations (location) and / or historical dates.<br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start_date<br>"
        	"Date must be formatted in date time YYYY-MM-DD<br>"
        "/api/v1.0/start_date/end_date<br>"
        	"Dates must be formatted in date time YYYY-MM-DD<br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
	"""Return precipitation data"""
	#Query by date
	results = session.query(Measurement.date, Measurement.prcp).all()
	#Convert list of tuples into normal list
	all_precipitation = []
	for date, prcp in results:
		precipitation_dict = {}
		precipitation_dict["date"] = date
		precipitation_dict["prcp"] = prcp
		all_precipitation.append(precipitation_dict)

	return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
	"""Return station data"""
	#Query by date
	results = session.query(Station.station, Station.name).all()

	return jsonify(results)

@app.route("/api/v1.0/tobs")
def temperature():
	"""Return temperature data"""

	# Calculate the date 1 year ago from the last data point in the database
	last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
	one_year = dt.date(2017,8,23) - dt.timedelta(days = 365)
	
	#Query by date
	results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year).all()

	all_temps = []
	for date, tobs in results:
		temp_dict = {}
		temp_dict["date"] = date
		temp_dict["tobs"] = tobs
		all_temps.append(temp_dict)

	return jsonify(all_temps)

@app.route("/api/v1.0/<start_date>")
def start_date_end_date(start_date = None):

	results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
	
	results_list = list(results)
	
	return jsonify(results_list)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date, end_date):

	results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
	
	results_list = list(results)
	
	return jsonify(results_list)

if __name__ == '__main__':
    app.run(debug=True)