##Imports 

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#define what happned when user hits index route 

@app.route("/")
def welcome():
    """List all available api routes."""
    
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation and dates"""
    # Convert the query results to a dictionary using date as the key and prcp as the value. 
    # Return the JSON representation of your dictionary.

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_dates = list(np.ravel(results))

    return jsonify(all_dates)


@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    results = session.query(Station.name).all()
    
    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    """Query the dates and temperature observations of the most active station for the last year of data.
     Return a JSON list of temperature observations (TOBS) for the previous year."""
    results = session.query(Measurement.date, Measurement.tobs).filter(Station.station == "USC00519281").filter(Measurement.date >= '2016-08-23').all()
    session.close()

    active_st = list(np.ravel(results))

    return jsonify (active_st)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start range."""
    print("enter the start date after the / in the url")
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()

    stats_start = list(np.ravel(results))

    return jsonify(stats_start)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start range."""
    print("enter the start date after the / in the url")
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date < end).all()
    session.close()

    stats_start_end = list(np.ravel(results))

    return jsonify(stats_start_end)

#################################
if __name__ == "__main__":
    app.run(debug=True)



