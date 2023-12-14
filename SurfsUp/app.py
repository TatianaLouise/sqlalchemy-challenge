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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
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
    

    # Query the dates and temperature observations of the most-active station for the previous year of data.

   


    # 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)