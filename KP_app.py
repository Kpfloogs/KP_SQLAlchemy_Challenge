import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine)

#defining classes to reflect
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)

@app.route("/")
def welcome():
     
     return(
        f"Below are all available api routes:<br/>"
        f"/api/v1.0/Percipitation<br/>"
        f"/api/v1.0/Stations<br/>"
        f"/api/v1.0/Temperature<br/>"
        f"/api/v1.0/Specific_Dates<br/>"
        f"/api/v1.0/Specific_Dates/<start>/<end>"

    )

@app.route("/api/v1.0/percipitation")
def percip():
    session = Session(engine)

    """Percipitation in Hawaii for the last 12 Months"""

    year_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-09-01').all()

    session.close()

    #displaying results in a dictionary
    year_percip = []
    for date, prcp in year_data:
        percip_dict = {}
        percip_dict["Date"] = date
        percip_dict["Percipitation"] = prcp
        year_percip.append(percip_dict)

    return jsonify(year_percip)

@app.route("/api/v1.0/Stations")
def stats():
    session = Session(engine)

    """A list of all weather stations in Hawaii"""

    stat_list = session.query(Station.station, Station.name).all()

    session.close()

    #displaying results in a list
    stats = list(np.ravel(stat_list))
    
    return jsonify(stats)

@app.route("/api/v1.0/Temperature")
def temp():
    session = Session(engine)

    """Temperatures observed by Station USC00519281: WAIHEE 837.5 for the previous year"""

    temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-27').all()

    session.close()
    
    #displaying results in a list
    temp = list(np.ravel(temp))
    
    return jsonify(temp)

@app.route("/api/v1.0/Specific_Dates/<start>")
def temp_stats(start=None):
    """Returning the minimum, average, and maximum temperatures for a specific date to the end of the date"""

    session = Session(engine)

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    #formatting the date
    start = dt.datetime.strptime(start, "%m%d%Y")

    results = session.query(*sel).\
        filter(Measurement.date >= start).all()

    session.close()
    date_temp = list(np.ravel(results))
    return jsonify(date_temp)


@app.route("/api/v1.0/Specific_Dates/<start2>/<end2>")
def range_stats(start2=None, end2=None):
    """Returning the minimum, average, and maximum temperatures for a range of dates to the end of the date"""
    
    session = Session(engine)

    #Select statement
    select = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    #formatting the dates
    start2 = dt.datetime.strptime(start2, "%m%d%Y")
    end2 = dt.datetime.strptime(end2, "%m%d%Y")
    
    two_dates = session.query(*select).\
        filter(Measurement.date >= start2).\
            filter(Measurement.date <= end2).all()

    session.close()

    series_temp = list(np.ravel(two_dates))

    return jsonify(series_temp)
  
    
if __name__ == '__main__':
    app.run(debug=True)








