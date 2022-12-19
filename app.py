import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask,jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


app=Flask(__name__)

@app.route("/")
def welcome():
    return (f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format YYYY-MM-DD.</p>")

# @app.route("/api/v1.0/precipitation")
# def welcome():
#     return 


# @app.route("/api/v1.0/stations")
# def welcome():
#     return 


# @app.route("/api/v1.0/tobs")
# def welcome():
#     return 

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None,end=None):
    data=[func.min(Measurement.tobs),
              func.max(Measurement.tobs),
              func.avg(Measurement.tobs)]

    if not end:
        temps=session.query(*data).filter(Measurement.date>=start).all()
        session.close()
        temps=list(np.ravel(temps))
        return jsonify(temps)

    temps=session.query(*data).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    session.close()
    temps=list(np.ravel(temps))

    return jsonify(temps)



if __name__=="__main__":
    app.run()