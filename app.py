from flask import Flask, jsonify

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

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
#################################################
@app.route("/api/v1.0/precipitation")

def precipitation():

    """Return a list of rain fall for prior year"""

#    * Query for the dates and precipitation observations from the last year.

#          
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    last_year= session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-24').filter(Measurement.date <= '2017-08-23').order_by(Measurement.date).all()
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    prcp_data= session.query(Measurement.date, Measurement.prcp.label("precipitation")).\
        filter(Measurement.date >= '2016-08-24').filter(Measurement.date <= '2017-08-23').order_by(Measurement.date).all()

# Create a list of dicts with `date` and `prcp` as the keys and values

    rain_totals = []

    for result in rain:

        row = {}

        row["date"] = prcp_data[0]

        row["prcp"] = prcp_data[1]

        rain_totals.append(row)



    return jsonify(rain_totals)
   

#################################################

@app.route("/api/v1.0/stations")

def stations():

    active_station = session.query(Measurement.station, func.count(Measurement.station)).\
              group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    #  Unravel active_station into a 1D array and convert to a list
    stations = list(np.ravel(active_station))

    return jsonify(stations)

#################################################

@app.route("/api/v1.0/tobs")

def tobs():

    """Return a list of temperatures for prior year"""

#    * Query for the dates and temperature observations from the last year.

#           * Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.

#           * Return the json representation of your dictionary.

    last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    temp_12month = session.query(Measurement.date, Measurement.tobs).\
             filter(Measurement.date > '2016-08-24').\
             filter(Measurement.station == 'USC00519281').\
             order_by(Measurement.date).all()


# Create a list of dicts with `date` and `tobs` as the keys and values

    temperature_totals = []

    for result in temp_12month:

        row = {}

        row["date"] = temp_12month[0]

        row["tobs"] = temp_12month[1]

        temperature_totals.append(row)


    return jsonify(temperature_totals)

#################################################

@app.route("/api/v1.0/<start>")

def trip1(start):



 # go back one year from start date and go to end of data for Min/Avg/Max temp   

    start_date= dt.datetime.strptime(start, '%Y-%m-%d')

    last_year = dt.timedelta(days=365)

    start = start_date-last_year

    end =  dt.date(2017, 8, 23)

    trip_data = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\

        filter(Measurements.date >= start).filter(Measurements.date <= end).all()

    trip = list(np.ravel(trip_data))

    return jsonify(trip)

#################################################

@app.route("/api/v1.0/<start>/<end>")

def trip2(start,end):

  # go back one year from start/end date and get Min/Avg/Max temp     

    start_date= dt.datetime.strptime(start, '%Y-%m-%d')

    end_date= dt.datetime.strptime(end,'%Y-%m-%d')

    last_year = dt.timedelta(days=365)

    start = start_date-last_year

    end = end_date-last_year

    trip_data = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\

        filter(Measurements.date >= start).filter(Measurements.date <= end).all()

    trip = list(np.ravel(trip_data))

    return jsonify(trip)
#################################################
if __name__ == "__main__":

    app.run(debug=True)
