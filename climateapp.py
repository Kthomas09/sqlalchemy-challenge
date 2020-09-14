# Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np
from flask import Flask, jsonify

# Connecting the sqlite file to climateapp.py
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Mapping classes to the sqlite schema
Base = automap_base()

# Reflecting tables in database
Base.prepare(engine, reflect=True)

# mapping each class in schema
measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

session = Session(engine)

# Home Page
@app.route("/")
def welcome():
    """List of API Routes."""
    
    return """<html><a href = "/api/v1.0/precipitation">/api/v1.0/precipitation</a>,
            <a href = "/api/v1.0/<start>">/api/v1.0/<start></a>,
            <a href = "/api/v1.0/<start>/<end>">/api/v1.0/<start>/<end></a>
            <a href = /api/v1.0/station">/api/v1.0/station</a></html>"""

session.close

# Precipitiation Page
@app.route("/api/v1.0/precipitation")
def precipitiation():
    session = Session(engine)
    max_date = dt.date(2012, 2, 28)
    last_year = max_date - dt.timedelta(days=365)
    
    past_temp = (session.query(measurement.date, measurement.prcp).filter(measurement.date <= max_date).filter(measurement.date >= last_year).order_by(measurement.date).all())
    
    rainfall = {date: prcp for date, prcp in past_temp}
    
    return jsonify(rainfall)

session.close()

# Start of vacation page
@app.route("/api/v1.0/<start>")
def start (start = None):
    session = Session(engine)
    tobs_only = (session.query(measurement.tobs).filter(measurement.date.between(start, "2012-03-05")).all())
    
    return jsonify(tobs_only)

session.close()

# Start and Ending of vacation
@app.route("/api/v1.0/<start>/<end>")
def start_end(start = None, end = None):
    session = Session(engine)
    tobs_only = (session.query(measurement.tobs).filter(measurement.date.between(start, end)).all())
    
    return jsonify(tobs_only)

session.close()

# Station page
@app.route("/api/v1.0/station")
def station():
    stations = session.query(station.name, station.station).all()
    stationls = list(np.ravel(stations))
    return jsonify(stationls)

session.close()

# App run statement
if __name__ == "__main__":
    app.run(debug=True)