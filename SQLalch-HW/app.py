import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
from pprint import pprint

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################



# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>")




@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    new_dict = {}
    for row in results:
        new_dict[row.date] = row.prcp
    print(new_dict)

    session.close()


    return jsonify(new_dict)



@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    stats = session.query(Station.station).all()

    stationion = list(np.ravel(stats))

    session.close()
    
    return jsonify(stationion)

@app.route("/api/v1.0/tobs")
def about():
    session = Session(engine)
  
    one_yr = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    high_temp = session.query(Measurement.station, Measurement.tobs, Measurement.date).\
                filter(Measurement.station == 'USC00519281').\
                filter(Measurement.date >= one_yr).all()
    
    temp = list(np.ravel(high_temp))

    return jsonify(temp)

# @app.route("/api/v1.0/<start>")
# def about():
#     return 

# @app.route("/api/v1.0/<start>/<end>")
# def about():
#     return 


    

if __name__ == "__main__":
    app.run(debug=True)
