# Import the dependencies.

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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurements = Base.classes.measurement
Stations = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    """Welcome to the Hawaii Climate API! Here is a list of all available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Temperature information from the start date(yyyy-mm-dd): /api/v1.0/<start><br/>"
        f"Temperature information from start to end dates(yyyy-mm-dd): /api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the query results from precipitation analysis
    
    """Precipitation in the last 12 months"""

    #Calculate the date one year from the last date in data set.
    first_date = dt.date(2017, 8 , 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    prcp_query = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date >= first_date).all()
    prcp_query

    session.close()

    data = [{'date': row.date, 'precipitation': row.prcp} for row in prcp_query]

    return jsonify(data)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a JSON list of stations from the dataset.

    station_activity = session.query(Measurements.station, func.count(Measurements.station)).\
    group_by(Measurements.station).order_by(func.count(Measurements.station).desc()).all()

    session.close()

    # Convert tuples into a list

    station_list = list(np.ravel(station_activity))

    return jsonify(station_list)

# Query the dates and temperature observations of the most-active station for the previous year of data.

@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)
   
    active_station_data = session.query(Measurements.date, Measurements.tobs).filter(Measurements.station == 'USC00519281')

    session.close()
    
    # Convert the list to Dictionary
    all_tobs = []

    for date,tobs in active_station_data:

        tobs_dict = {}

        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        all_tobs.append(tobs_dict)


    return jsonify(all_tobs)

# Return a JSON list of the minimum temperature, 
# the average temperature, and the maximum temperature for a specified start or start-end range.

@app.route("/api/v1.0/<start>")
def start(start):

    # Convert the start parameter to a datetime object
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()

    first_date = start_date - dt.timedelta(days=365)

    # Create our session (link) from Python to the DB
    session = Session(engine)

    date_statistics = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
                filter(Measurements.date >= first_date).all()
    
    session.close()

    # Convert data to a list of dictionaries and jsonify

    start_date_tobs = []

    for min, avg, max in date_statistics:

        tobs_dict = {}

        tobs_dict["min_temp"] = min
        tobs_dict["avg_temp"] = avg
        tobs_dict["max_temp"] = max

        start_date_tobs.append(tobs_dict
                               ) 
        
    return jsonify(start_date_tobs)

# Calculate statistics for start and end date

@app.route("/api/v1.0/<start>/<end>")
def date_range(start, end):
    # Convert the start and end parameters to datetime objects
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end_date = dt.datetime.strptime(end, "%Y-%m-%d").date()

    start = start_date - dt.timedelta(days=365)
    end = end_date - dt.timedelta(days=365)

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for date range statistics
    date_range_statistics = session.query(
        func.min(Measurements.tobs),
        func.avg(Measurements.tobs),
        func.max(Measurements.tobs)
    ).filter(Measurements.date >= start, Measurements.date <= end).all()

    session.close()

    # Convert the result to a dictionary for JSON response
    result_dict = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "date_range_statistics": date_range_statistics
    }

    return jsonify(result_dict)

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)