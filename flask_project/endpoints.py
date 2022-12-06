# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pymysql.cursors
import hashlib

# Initialize the app from Flask
app = Flask(__name__)

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=3306,  # change this every time if you are a Windows user
                       user='root',
                       password='',  # change this every time if you are Windows user
                       db='air_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


# Define route for index
@app.route('/')
def index():
    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM flight'
    cursor.execute(query)
    # stores the results in a variable
    data = cursor.fetchall()
    cursor.close()
    headings = ("Airline Name", "Flight Number", "Departure Date and Time", "Arrival Date and Time", "Status")
    return render_template('home_templates/index.html', headings=headings, data=data)


# Define route for register
@app.route('/register')
def register():
    return render_template('home_templates/register.html')


# Define route for customer register
@app.route('/customer_register')
def customer_register():
    return render_template('customer_templates/customer_register.html')


# Define route for airline staff register
@app.route('/airline_staff_register')
def airline_staff_register():
    return render_template('airline_staff_templates/airline_staff_register.html')


# Authenticates the customer register
@app.route('/customer_register_auth', methods=['GET', 'POST'])
def customer_register_auth():
    # grabs information from the forms
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    building_number = request.form['building_number']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone_number = request.form['phone_number']
    passport_number = request.form['passport_number']
    passport_expiration = request.form['passport_expiration']
    passport_country = request.form['passport_country']
    date_of_birth = request.form['date_of_birth']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM customer WHERE EmailAddress = %s'
    cursor.execute(query, email)
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    context = None
    if data:
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('customer_templates/customer_register.html', error=error)
    else:
        ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (name, email, md5(password), building_number, street, city, state,
                             phone_number, passport_number, passport_expiration, passport_country,
                             date_of_birth))
        conn.commit()
        cursor.close()
        message = "User successfully registered!"
        return render_template('customer_templates/customer_register.html', context=message)


# Authenticates the airline staff register
@app.route('/airline_staff_register_auth', methods=['GET', 'POST'])
def airline_staff_register_auth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    airline_name = request.form['airline_name']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM airlinestaff WHERE Username = %s'
    cursor.execute(query, username)
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    context = None
    if data:
        # If the previous query returns data, then user exists
        error = "This staff member already exists"
        return render_template('airline_staff_templates/airline_staff_register.html', error=error)
    else:
        ins = 'INSERT INTO airlinestaff VALUES(%s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, md5(password), first_name, last_name, date_of_birth, airline_name))
        conn.commit()
        cursor.close()
        message = "Staff member successfully registered!"
        return render_template('airline_staff_templates/airline_staff_register.html', context=message)


# Define route for login
@app.route('/login')
def login():
    return render_template('home_templates/login.html')


# Define route for customer login
@app.route('/customer_login')
def customer_login():
    return render_template('customer_templates/customer_login.html')


# Define route for airline staff login
@app.route('/airline_staff_login')
def airline_staff_login():
    return render_template('airline_staff_templates/airline_staff_login.html')


# Authenticates the customer login
@app.route('/customer_login_auth', methods=['GET', 'POST'])
def customer_login_auth():
    # grabs information from the forms
    email = request.form['email']
    password = request.form['password']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM customer WHERE EmailAddress = %s and Password = %s'
    cursor.execute(query, (email, md5(password)))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if data:
        # creates a session for the user
        # session is a built in
        session['email'] = email
        session['is_customer'] = True
        return redirect(url_for('customer_home'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('customer_templates/customer_login.html', error=error)


# Authenticates the airline staff login
@app.route('/airline_staff_login_auth', methods=['GET', 'POST'])
def airline_staff_login_auth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM airlinestaff WHERE Username = %s and Password = %s'
    cursor.execute(query, (username, md5(password)))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if data:
        # creates a session for the user
        # session is a built in
        session['username'] = username
        session['is_airline_staff'] = True
        session['airline_name'] = data['AirlineName']
        return redirect(url_for('airline_staff_home'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('airline_staff_templates/airline_staff_login.html', error=error)


@app.route('/airline_staff_home')
def airline_staff_home():
    if session.get('is_airline_staff'):
        username = session['username']
        airlineName = session['airline_name']
        # cursor used to send queries
        cursor = conn.cursor()
        # executes query
        query = 'SELECT AirlineName, FlightNumber, DepartureAirportName, ArrivalAirportName, ' \
                'DepartureDateandTime, ArrivalDateandTime, BasePrice, Status FROM flight ' \
                'WHERE AirlineName = %s AND DepartureDateandTime >= DATE(NOW()) AND ' \
                'DepartureDateandTime <= DATE(NOW() + INTERVAL 30 DAY);'
        cursor.execute(query, (airlineName,))
        # stores the results in a variable
        data = cursor.fetchall()
        cursor.close()
        headings = ("Airline Name", "Flight Number", "Departure Airport", "Arrival Airport",
                    "Departure Date and Time", "Arrival Date and Time", "Base Price", "Status")
        return render_template('airline_staff_templates/airline_staff_home.html', username=username, headings=headings,
                               data=data)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


@app.route('/insert_new_flight')
def insert_new_flight():
    if session.get('is_airline_staff'):
        airlineName = session['airline_name']
        # cursor used to send queries
        cursor = conn.cursor()
        query = 'SELECT AirlineName, FlightNumber, DepartureAirportName, ArrivalAirportName, ' \
                'DepartureDateandTime, ArrivalDateandTime, BasePrice, Status FROM flight ' \
                'WHERE AirlineName = %s AND DepartureDateandTime >= DATE(NOW()) AND ' \
                'DepartureDateandTime <= DATE(NOW() + INTERVAL 30 DAY);'
        cursor.execute(query, (airlineName,))
        # stores the results in a variable
        data = cursor.fetchall()
        cursor.close()
        headings = ("Airline Name", "Flight Number", "Departure Airport", "Arrival Airport",
                    "Departure Date and Time", "Arrival Date and Time", "Base Price", "Status")
        return render_template('airline_staff_templates/airline_staff_insert.html', headings=headings, data=data)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


@app.route('/exec_insert_new_flight', methods=['GET', 'POST'])
def exec_insert_new_flight():
    if session.get('is_airline_staff'):
        airlineName = session['airline_name']
        # grabs information from the forms
        DepartureDateandTime = request.form['DepartureDateandTime']
        ArrivalDateandTime = request.form['ArrivalDateandTime']
        BasePrice = request.form['BasePrice']
        DepartureAirportName = request.form['DepartureAirportName']
        ArrivalAirportName = request.form['ArrivalAirportName']
        IDNumber = request.form['IDNumber']
        Status = 'On-time'  # By default
        AirlineName = session['airline_name']  # By default
        DepartureDateandTime = datetime.strptime(DepartureDateandTime, "%Y-%m-%dT%H:%M")
        ArrivalDateandTime = datetime.strptime(ArrivalDateandTime, "%Y-%m-%dT%H:%M")
        departure_is_after = DepartureDateandTime > datetime.today()
        arrival_is_after = ArrivalDateandTime > DepartureDateandTime
        # Query all of the future flights
        futureFlightsQuery = 'SELECT AirlineName, FlightNumber, DepartureAirportName, ArrivalAirportName, ' \
                             'DepartureDateandTime, ArrivalDateandTime, BasePrice, Status FROM flight ' \
                             'WHERE AirlineName = %s AND DepartureDateandTime >= DATE(NOW()) AND ' \
                             'DepartureDateandTime <= DATE(NOW() + INTERVAL 30 DAY);'
        headings = ("Airline Name", "Flight Number", "Departure Airport", "Arrival Airport",
                    "Departure Date and Time", "Arrival Date and Time", "Base Price", "Status")
        # cursor used to send queries
        cursor = conn.cursor()
        if not departure_is_after:
            cursor.execute(futureFlightsQuery, (airlineName,))
            # stores the results in a variable
            futureFlights = cursor.fetchall()
            cursor.close()
            error = "The Departure Date and Time must be after the current Date and Time"
            return render_template('airline_staff_templates/airline_staff_insert.html', error=error,
                                   headings=headings, data=futureFlights)
        if not arrival_is_after:
            cursor.execute(futureFlightsQuery, (airlineName,))
            # stores the results in a variable
            futureFlights = cursor.fetchall()
            cursor.close()
            error = "The Arrival Date and Time must be after the Departure Date and Time"
            return render_template('airline_staff_templates/airline_staff_insert.html', error=error,
                                   headings=headings, data=futureFlights)
        ArrivalDateandTime = ArrivalDateandTime.strftime('%Y-%m-%d %H:%M:%S')
        DepartureDateandTime = DepartureDateandTime.strftime('%Y-%m-%d %H:%M:%S')
        # executes query
        query = 'SELECT FlightNumber FROM flight WHERE DepartureDateandTime = %s AND AirlineName = %s'
        cursor.execute(query, (DepartureDateandTime, AirlineName))
        # stores the results in a variable
        flightData = cursor.fetchall()
        maxFlightNumber = -1
        for item in flightData:
            value = item['FlightNumber']
            if int(value) > maxFlightNumber:
                maxFlightNumber = int(value)
        if maxFlightNumber == -1:
            FlightNumber = 1
        else:
            FlightNumber = maxFlightNumber + 1

        # This query checks to make sure one airplane isn't flying multiple flights at
        # the same time within the same airline
        query = 'SELECT * FROM flight WHERE IDNumber = %s AND DepartureDateandTime = %s AND AirlineName = %s'
        cursor.execute(query, (IDNumber, DepartureDateandTime, AirlineName))
        # stores the results in a variable
        data = cursor.fetchone()
        # Checking the departure and arrival airports exist and also the airplane
        query = 'SELECT * FROM airport WHERE AirportName = %s'
        cursor.execute(query, (DepartureAirportName,))
        # stores the results in a variable
        is_departure_airport = cursor.fetchone()
        query = 'SELECT * FROM airport WHERE AirportName = %s'
        cursor.execute(query, (ArrivalAirportName,))
        # stores the results in a variable
        is_arrival_airport = cursor.fetchone()
        query = 'SELECT * FROM airplane WHERE IDNumber = %s AND AirlineName = %s'
        cursor.execute(query, (IDNumber, airlineName))
        # stores the results in a variable
        is_airplane = cursor.fetchone()
        # use fetchall() if you are expecting more than 1 data row
        error = None
        context = None
        if data:
            cursor.execute(futureFlightsQuery, (airlineName,))
            # stores the results in a variable
            futureFlights = cursor.fetchall()
            cursor.close()
            # If the previous query returns data, then user exists
            error = "This flight already exists!"
            return render_template('airline_staff_templates/airline_staff_insert.html', error=error,
                                   headings=headings, data=futureFlights)
        else:
            if not is_departure_airport:
                cursor.execute(futureFlightsQuery, (airlineName,))
                # stores the results in a variable
                futureFlights = cursor.fetchall()
                cursor.close()
                error = "The {} Airport doesn't exist!".format(DepartureAirportName)
                return render_template('airline_staff_templates/airline_staff_insert.html', error=error,
                                       headings=headings, data=futureFlights)
            elif not is_arrival_airport:
                cursor.execute(futureFlightsQuery, (airlineName,))
                # stores the results in a variable
                futureFlights = cursor.fetchall()
                cursor.close()
                error = "The {} Airport doesn't exist!".format(ArrivalAirportName)
                return render_template('airline_staff_templates/airline_staff_insert.html', error=error,
                                       headings=headings, data=futureFlights)
            elif not is_airplane:
                cursor.execute(futureFlightsQuery, (airlineName,))
                # stores the results in a variable
                futureFlights = cursor.fetchall()
                cursor.close()
                error = "The airplane with ID number {} doesn't exist!".format(IDNumber)
                return render_template('airline_staff_templates/airline_staff_insert.html', error=error,
                                       headings=headings, data=futureFlights)
            else:
                ins = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(ins, (
                str(FlightNumber), DepartureDateandTime, ArrivalDateandTime, BasePrice, Status, DepartureAirportName,
                ArrivalAirportName, IDNumber, AirlineName))
                conn.commit()
                cursor.execute(futureFlightsQuery)
                # stores the results in a variable
                futureFlights = cursor.fetchall()
                cursor.close()
                message = "New flight successfully added!"
                return render_template('airline_staff_templates/airline_staff_insert.html', context=message,
                                       headings=headings, data=futureFlights)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


# Define route for airline staff to search for flights
@app.route('/search_flights_airline_staff')
def search_flights_airline_staff():
    if session.get('is_airline_staff'):
        return render_template('airline_staff_templates/search_flights_airline_staff.html')
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


@app.route('/search_flights_airline_staff_query', methods=['GET', 'POST'])
def search_flights_airline_staff_query():
    if session.get('is_airline_staff'):
        airline_name = session['airline_name']
        # grabs information from the forms
        source_city = request.form['Source City/Airport Name']
        destination_city = request.form['Destination City/Airport Name']
        start_departure_date_and_time = request.form['StartDepartureDateandTime']
        start_departure_date_and_time = datetime.strptime(start_departure_date_and_time,
                                                                   "%Y-%m-%dT%H:%M").strftime('%Y-%m-%d %H:%M:%S')
        end_departure_date_and_time = request.form['EndDepartureDateandTime']
        has_end_date = False
        if end_departure_date_and_time != "":
            has_end_date = True
            end_departure_date_and_time = datetime.strptime(end_departure_date_and_time,
                                                                     "%Y-%m-%dT%H:%M").strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.cursor()
        # Checking the departure and arrival airports exist
        query = 'SELECT * FROM airport WHERE AirportName = %s'
        cursor.execute(query, (source_city,))
        # stores the results in a variable
        is_departure_airport = cursor.fetchone()
        query = 'SELECT * FROM airport WHERE AirportName = %s'
        cursor.execute(query, (destination_city,))
        # stores the results in a variable
        is_arrival_airport = cursor.fetchone()
        # cursor used to send queries
        error = None
        if not is_departure_airport:
            error = "The {} Airport doesn't exist!".format(source_city)
            return render_template('airline_staff_templates/search_flights_airline_staff.html', error=error)
        if not is_arrival_airport:
            error = "The {} Airport doesn't exist!".format(destination_city)
            return render_template('airline_staff_templates/search_flights_airline_staff.html', error=error)
        if has_end_date:
            # executes query
            query = 'SELECT AirlineName, FlightNumber, DepartureAirportName, ' \
                    'ArrivalAirportName, DepartureDateandTime, ArrivalDateandTime, BasePrice, Status ' \
                    'FROM flight WHERE ' \
                    'AirlineName = %s AND ' \
                    'DepartureAirportName = %s AND ' \
                    'ArrivalAirportName = %s AND ' \
                    'DepartureDateandTime >= %s AND ' \
                    'DepartureDateAndTime <= %s'
            cursor.execute(query, (
            airline_name, source_city, destination_city, start_departure_date_and_time, end_departure_date_and_time))
        else:
            # executes query
            query = 'SELECT AirlineName, FlightNumber, DepartureAirportName, ' \
                    'ArrivalAirportName, DepartureDateandTime, ArrivalDateandTime, BasePrice, Status ' \
                    'FROM flight WHERE ' \
                    'AirlineName = %s AND ' \
                    'DepartureAirportName = %s AND ' \
                    'ArrivalAirportName = %s AND ' \
                    'DepartureDateandTime >= %s'
            cursor.execute(query, (airline_name, source_city, destination_city, start_departure_date_and_time))
        data = cursor.fetchall()
        if data:
            headings = ("Airline Name", "Flight Number", "Departure Airport",
                        "Arrival Airport", "Departure Date and Time", "Arrival Date and Time", "Base Price", "Status")
            return render_template('airline_staff_templates/search_flights_airline_staff.html', headings=headings,
                                   data=data)
        else:
            error = "No flights found for that search result"
            return render_template('airline_staff_templates/search_flights_airline_staff.html', error=error)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


@app.route('/view_flight_customers/<flightData>')
def view_flight_customers(flightData):
    if session.get('is_airline_staff'):
        flightData = eval(flightData)
        query = 'SELECT DISTINCT Name FROM Purchase Natural Join Customer, Ticket WHERE ' \
                'Ticket.TicketIDNumber = Purchase.TicketIDNumber AND Ticket.TicketIDNumber ' \
                'IN(SELECT TicketIDNumber FROM Flight Natural Join Ticket WHERE ' \
                'Flight.AirlineName = %s AND ' \
                'Flight.FlightNumber = %s AND ' \
                'Flight.DepartureDateandTime = %s)'
        # cursor used to send queries
        cursor = conn.cursor()
        cursor.execute(query, (flightData['AirlineName'], flightData['FlightNumber'],
                               flightData['DepartureDateandTime'].strftime('%Y-%m-%d %H:%M:%S')))
        data = cursor.fetchall()
        message = None
        if data:
            headings = ("Name",)
            return render_template('airline_staff_templates/airline_staff_view_flight_customers.html',
                                   headings=headings,
                                   data=data)
        else:
            message = "No customers found for that flight"
            return render_template('airline_staff_templates/airline_staff_view_flight_customers.html', message=message)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


@app.route('/change_flight_status/<flightData>')
def change_flight_status(flightData):
    if session.get('is_airline_staff'):
        flightData = eval(flightData)
        return render_template('airline_staff_templates/change_flight_status.html', flightData=flightData)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


@app.route('/exec_change_flight_status/<flightData>', methods=['GET', 'POST'])
def exec_change_flight_status(flightData):
    if session.get('is_airline_staff'):
        airline_name = session['airline_name']
        changedStatus = request.form['Status']
        flightData = eval(flightData)
        flightNumber = flightData['FlightNumber']
        departureDateandTime = flightData['DepartureDateandTime']
        oldStatus = flightData['Status']
        if changedStatus != oldStatus:
            update = 'UPDATE flight SET Status = %s WHERE FlightNumber = %s AND ' \
                     'DepartureDateandTime = %s AND AirlineName = %s;'
            cursor = conn.cursor()
            cursor.execute(update, (changedStatus, flightNumber, departureDateandTime, airline_name))
            conn.commit()
            cursor.close()
            message = "The {} Flight {} departing on {} " \
                      "has successfully changed status from {} to {}".format(airline_name, flightNumber,
                                                                             departureDateandTime, oldStatus,
                                                                             changedStatus)
        else:
            message = "The {} Flight {} departing on {} already has the status {}".format(airline_name, flightNumber,
                                                                                          departureDateandTime,
                                                                                          changedStatus)
        return render_template('airline_staff_templates/search_flights_airline_staff.html', message=message)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


@app.route('/view_ratings/<flightData>')
def view_ratings(flightData):
    if session.get('is_airline_staff'):
        flightData = eval(flightData)
        flight_heading = ("Airline Name", "Flight Number", "Departure Airport",
                        "Arrival Airport", "Departure Date and Time", "Arrival Date and Time", "Base Price", "Status")
        avg_rating_query = 'SELECT AVG(Rating) AS avg_rating FROM Flight Natural Join Rate WHERE ' \
                           'Flight.AirlineName = %s AND ' \
                           'Flight.FlightNumber = %s AND ' \
                           'Flight.DepartureDateandTime = %s'
        rating_query = 'SELECT Rating, Comment FROM Flight Natural Join Rate WHERE ' \
                       'Flight.AirlineName = %s AND ' \
                       'Flight.FlightNumber = %s AND ' \
                       'Flight.DepartureDateandTime = %s'
        # cursor used to send queries
        cursor = conn.cursor()
        cursor.execute(rating_query, (flightData['AirlineName'], flightData['FlightNumber'],
                                      flightData['DepartureDateandTime'].strftime('%Y-%m-%d %H:%M:%S')))
        rating_data = cursor.fetchall()
        cursor.execute(avg_rating_query, (flightData['AirlineName'], flightData['FlightNumber'],
                                          flightData['DepartureDateandTime'].strftime('%Y-%m-%d %H:%M:%S')))
        avg_rating_data = cursor.fetchone()
        if rating_data:
            avg_rating_data = int(avg_rating_data['avg_rating'] * 10) / 10
            headings = ('Rating','Comment')
            return render_template('airline_staff_templates/airline_staff_view_rating.html',
                                   headings=headings,
                                   data=rating_data,avg_rating = avg_rating_data,flight_headings =flight_heading, flight_data = flightData)
        else:
            message = "No ratings found for that flight"
            return render_template('airline_staff_templates/airline_staff_view_rating.html', message=message, flight_headings =flight_heading, flight_data = flightData)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


@app.route('/insert_new_airplane', methods=['GET', 'POST'])
def insert_new_airplane():
    cursor = conn.cursor()
    # executes query
    query = 'SELECT IDNumber,NumberofSeats,ManufacturingCompany, Age, NumberofEconomyClassSeats, ' \
            'NumberofBusinessClassSeats, NumberofFirstClassSeats  FROM airplane WHERE AirlineName = %s'
    cursor.execute(query, (session['airline_name'],))
    # stores the results in a variable
    data = cursor.fetchall()
    cursor.close()
    headings = ("ID Number", "Number of Seats", "Manufacturing Company", "Age", "Number of Economy Class Seats",
                "Number of Business Class Seats", "Number of First Class Seats")
    return render_template('airline_staff_templates/insert_new_airplane.html', headings=headings, data=data)


@app.route('/exec_insert_new_airplane', methods=['GET', 'POST'])
def exec_insert_new_airplane():
    if session.get('is_airline_staff'):
        IDNumber = request.form['IDNumber']
        ManufacturingCompany = request.form['ManufacturingCompany']
        Age = request.form['Age']
        AirlineName = session['airline_name']
        NumberofEconomyClassSeats = request.form['NumberofEconomyClassSeats']
        NumberofBusinessClassSeats = request.form['NumberofBusinessClassSeats']
        NumberofFirstClassSeats = request.form['NumberofFirstClassSeats']
        NumberofSeats = int(NumberofFirstClassSeats) + int(NumberofBusinessClassSeats) + int(NumberofEconomyClassSeats)

        cursor = conn.cursor()
        query = 'SELECT * FROM airplane WHERE IDNumber = %s AND AirlineName = %s'
        cursor.execute(query, (IDNumber, AirlineName))
        data = cursor.fetchone()
        if data:
            # If the previous query returns data, then user exists
            error = "This airplane already exists!"
            # executes query
            query = 'SELECT IDNumber,NumberofSeats,ManufacturingCompany, Age, NumberofEconomyClassSeats, ' \
                    'NumberofBusinessClassSeats, NumberofFirstClassSeats  FROM airplane WHERE AirlineName = %s'
            cursor.execute(query, (session['airline_name'],))
            # stores the results in a variable
            data = cursor.fetchall()
            headings = ("ID Number", "Number of Seats", "Manufacturing Company", "Age", "Number of Economy Class Seats",
                        "Number of Business Class Seats", "Number of First Class Seats")
            return render_template('airline_staff_templates/insert_new_airplane.html', headings=headings, data=data,
                                   error=error)
        else:
            ins = 'INSERT INTO airplane VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(ins, (IDNumber, NumberofSeats, ManufacturingCompany, Age, AirlineName,
                                 NumberofEconomyClassSeats, NumberofBusinessClassSeats, NumberofFirstClassSeats))
            conn.commit()
            # executes query
            query = 'SELECT IDNumber, NumberofSeats, ManufacturingCompany, Age, NumberofEconomyClassSeats, ' \
                    'NumberofBusinessClassSeats, NumberofFirstClassSeats FROM airplane WHERE AirlineName = %s'
            cursor.execute(query, (session['airline_name'],))
            # stores the results in a variable
            data = cursor.fetchall()
            headings = ("ID Number", "Number of Seats", "Manufacturing Company", "Age", "Number of Economy Class Seats",
                        "Number of Business Class Seats", "Number of First Class Seats")
            cursor.close()
            message = "New airplane successfully added!"
            return render_template('airline_staff_templates/insert_new_airplane.html', headings=headings, data=data,
                                   context=message)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


@app.route('/insert_new_airport')
def insert_new_airport():
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM airport'
    cursor.execute(query)
    # stores the results in a variable
    data = cursor.fetchall()
    cursor.close()
    headings = ("Airport Name", "City", "Country", "AirportType")
    return render_template('airline_staff_templates/insert_new_airport.html', headings=headings, data=data)


@app.route('/exec_insert_new_airport', methods=['GET', 'POST'])
def exec_insert_new_airport():
    if session.get('is_airline_staff'):
        AirportName = request.form['AirportName']
        City = request.form['City']
        Country = request.form['Country']
        AirportType = request.form['AirportType']
        cursor = conn.cursor()
        query = 'SELECT * FROM airport WHERE AirportName = %s'
        cursor.execute(query, (AirportName))
        data = cursor.fetchone()
        if data:
            error = "This airport already exists!"
            query = 'SELECT *  FROM airport'
            cursor.execute(query)
            data = cursor.fetchall()
            headings = ("Airport Name", "City", "Country", "AirportType")
            return render_template('airline_staff_templates/insert_new_airport.html', headings=headings, data=data,
                                   error=error)
        else:
            ins = 'INSERT INTO airport VALUES(%s, %s, %s, %s)'
            cursor.execute(ins, (AirportName, City, Country, AirportType))
            conn.commit()
            query = 'SELECT *  FROM airport'
            cursor.execute(query)
            data = cursor.fetchall()
            headings = ("Airport Name", "City", "Country", "AirportType")
            cursor.close()
            message = "New airport successfully added!"
            return render_template('airline_staff_templates/insert_new_airport.html', headings=headings, data=data,
                                   context=message)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


@app.route('/ticket_stats')
def ticket_stats():
    if session.get('is_airline_staff'):
        airline_name = session['airline_name']
        lastMonthQuery = "SELECT SUM(sold_price) as revenue FROM purchase NATURAL JOIN ticket WHERE " \
                         "AirlineName = %s AND PurchaseDateandTime >= DATE(NOW() - INTERVAL 1 MONTH);"
        lastYearQuery = "SELECT SUM(sold_price) as revenue FROM purchase NATURAL JOIN ticket WHERE " \
                        "AirlineName = %s AND PurchaseDateandTime >= DATE(NOW() - INTERVAL 1 YEAR);"
        cursor = conn.cursor()
        # executes query
        cursor.execute(lastMonthQuery, (airline_name,))
        # stores the results in a variable
        lastMonthResults = cursor.fetchone()
        # executes query
        cursor.execute(lastYearQuery, (airline_name,))
        # stores the results in a variable
        lastYearResults = cursor.fetchone()
        cursor.close()
        lastMonthRevenue = lastMonthResults['revenue']
        lastYearRevenue = lastYearResults['revenue']
        lastMonthRevenue = "$0.00" if not lastMonthRevenue else "$"+str(round(lastMonthRevenue,2))
        lastYearRevenue = "$0.00" if not lastYearRevenue else "$"+str(round(lastYearRevenue,2))
        return render_template('airline_staff_templates/ticket_stats.html', lastMonthRevenue=lastMonthRevenue,
                               lastYearRevenue=lastYearRevenue)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


@app.route('/exec_ticket_stats/<revenueData>', methods=['GET', 'POST'])
def exec_ticket_stats(revenueData):
    if session.get('is_airline_staff'):
        lastMonthRevenue, lastYearRevenue = eval(revenueData)
        airline_name = session['airline_name']
        # grabs information from the forms
        start_date_and_time = datetime.strptime(request.form['StartDateandTime'],
                                                         "%Y-%m-%dT%H:%M").strftime('%Y-%m-%d %H:%M:%S')
        end_date_and_time = request.form['EndDateandTime']
        has_end_date = False
        if end_date_and_time != "":
            has_end_date = True
            end_date_and_time = datetime.strptime(end_date_and_time,
                                                           "%Y-%m-%dT%H:%M").strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.cursor()
        if has_end_date:
            # executes query
            query = 'SELECT YEAR(PurchaseDateandTime) as PurchaseYear, MONTH(PurchaseDateandTime) as PurchaseMonth, ' \
                    'COUNT(TicketIDNumber) AS TicketCount, SUM(sold_price) as Revenue ' \
                    'FROM purchase NATURAL JOIN ticket WHERE ' \
                    'AirlineName = %s AND PurchaseDateandTime >= %s AND PurchaseDateandTime <= %s ' \
                    'GROUP BY YEAR(PurchaseDateandTime), MONTH(PurchaseDateandTime) ' \
                    'ORDER BY YEAR(PurchaseDateandTime), MONTH(PurchaseDateandTime);'
            cursor.execute(query, (airline_name, start_date_and_time, end_date_and_time))
        else:
            # executes query
            query = 'SELECT YEAR(PurchaseDateandTime) as PurchaseYear, MONTH(PurchaseDateandTime) as PurchaseMonth, ' \
                    'COUNT(TicketIDNumber) AS TicketCount, SUM(sold_price) as Revenue ' \
                    'FROM purchase NATURAL JOIN ticket WHERE ' \
                    'AirlineName = %s AND PurchaseDateandTime >= %s' \
                    'GROUP BY YEAR(PurchaseDateandTime), MONTH(PurchaseDateandTime) ' \
                    'ORDER BY YEAR(PurchaseDateandTime), MONTH(PurchaseDateandTime);'
            cursor.execute(query, (airline_name, start_date_and_time))
        data = cursor.fetchall()
        if data:
            totalRevenue = 0
            totalTicketsSold = 0
            for row in data:
                revenue = row['Revenue']
                ticketsSold = row['TicketCount']
                row['Revenue'] = "$"+str(round(revenue, 2))
                totalRevenue += revenue
                totalTicketsSold += ticketsSold
            totalRevenue = "$"+str(round(totalRevenue,2))
            headings = ("Year", "Month", "Tickets Sold", "Revenue")
            return render_template('airline_staff_templates/ticket_stats.html', lastMonthRevenue=lastMonthRevenue,
                                   lastYearRevenue=lastYearRevenue, totalRevenue=totalRevenue,
                                   totalTicketsSold=totalTicketsSold, headings=headings, data=data)
        else:
            error = "No Tickets sold during that period"
            return render_template('airline_staff_templates/ticket_stats.html', lastMonthRevenue=lastMonthRevenue,
                                   lastYearRevenue=lastYearRevenue, error=error)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


@app.route('/customer_stats')
def customer_stats():
    if session.get('is_airline_staff'):
        airline_name = session['airline_name']
        lastYearQuery = "SELECT Name, EmailAddress, COUNT(purchase.TicketIDNumber) as TicketCount " \
                        "FROM customer NATURAL JOIN purchase, ticket " \
                        "WHERE ticket.TicketIDNumber = purchase.TicketIDNumber AND AirlineName = %s " \
                        "AND PurchaseDateandTime >= DATE(NOW() - INTERVAL 1 YEAR) GROUP BY EmailAddress;"
        cursor = conn.cursor()
        # executes query
        cursor.execute(lastYearQuery, (airline_name,))
        # stores the results in a variable
        lastYearResults = cursor.fetchall()
        maxIndices = []
        maxTicketCount = 0
        for i,row in enumerate(lastYearResults):
            ticketCount = row['TicketCount']
            if ticketCount > maxTicketCount:
                maxIndices = [i]
                maxTicketCount = ticketCount
            elif ticketCount == maxTicketCount:
                maxIndices.append(i)
        lastYearResults = [lastYearResults[i] for i in maxIndices]
        headings1 = ["Name", "Email Address", "# Flights"]
        customerQuery = "SELECT DISTINCT Name, EmailAddress, BuildingNumber, Street, City, State, PhoneNumber, " \
                        "PassportNumber, PassportExpiration, PassportCountry, DateofBirth " \
                        "FROM customer NATURAL JOIN purchase, ticket " \
                        "WHERE ticket.TicketIDNumber = purchase.TicketIDNumber AND AirlineName = %s;"
        headings2 = ["Name", "EmailAddress", "BuildingNumber", "Street", "City", "State", "PhoneNumber",
                     "PassportNumber", "PassportExpiration", "PassportCountry", "DateofBirth"]
        cursor.execute(customerQuery, (airline_name,))
        # stores the results in a variable
        customerResults = cursor.fetchall()
        cursor.close()
        return render_template('airline_staff_templates/customer_stats.html', headings1=headings1,
                               data1=lastYearResults, headings2=headings2, data2=customerResults)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


@app.route('/exec_customer_stats/<customerData>', methods=['GET', 'POST'])
def exec_customer_stats(customerData):
    if session.get('is_airline_staff'):
        customerData = eval(customerData)
        customerEmail = customerData['EmailAddress']
        customerName = customerData['Name']
        airline_name = session['airline_name']
        # executes query
        flightsQuery = 'SELECT AirlineName, FlightNumber, DepartureAirportName, ArrivalAirportName, ' \
                'DepartureDateandTime, ArrivalDateandTime, BasePrice, Status ' \
                'FROM ticket NATURAL JOIN flight, customer, purchase ' \
                'WHERE ticket.TicketIDNumber = purchase.TicketIDNumber ' \
                'AND purchase.EmailAddress = customer.EmailAddress ' \
                'AND customer.EmailAddress = %s AND AirlineName = %s;'
        cursor = conn.cursor()
        cursor.execute(flightsQuery, (customerEmail, airline_name))
        flightsResults = cursor.fetchall()
        cursor.close()
        if flightsResults:
            headings = ("AirlineName", "FlightNumber", "DepartureAirportName", "ArrivalAirportName",
                        "DepartureDateandTime", "ArrivalDateandTime", "BasePrice", "Status")
            return render_template('airline_staff_templates/customer_stats_flights.html', headings=headings,
                                   data=flightsResults, customerEmail=customerEmail, customerName=customerName)
        else:
            error = "{} ({}) has taken no flights with {}".format(customerName, customerEmail, airline_name)
            return render_template('airline_staff_templates/customer_stats_flights.html', error=error)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


# Define route for user to search for flights
@app.route('/search_flights')
def search_flights():
    return render_template('home_templates/search_for_flights.html', is_customer=session.get('is_customer'),
                           is_airline_staff=session.get('is_airline_staff'))


@app.route('/search_one_way')
def search_one_way():
    return render_template('home_templates/search_one_way.html', is_customer=session.get('is_customer'),
                           is_airline_staff=session.get('is_airline_staff'))


# Define route for user to search for flights
@app.route('/search_round_trip')
def search_round_trip():
    return render_template('home_templates/search_round_trip.html', is_customer=session.get('is_customer'))


# Define route for querying for one way flights
@app.route('/search_one_way_query', methods=['GET', 'POST'])
def search_one_way_query():
    # grabs information from the forms
    source_city = request.form['Source City/Airport Name']
    destination_city = request.form['Destination City/Airport Name']
    departure_date_and_time = request.form['Departure Date and Time']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT AirlineName, FlightNumber, DepartureAirportName, ' \
            'ArrivalAirportName, DepartureDateandTime, ArrivalDateandTime ' \
            'FROM flight WHERE ' \
            'DepartureAirportName = %s AND ' \
            'ArrivalAirportName = %s AND ' \
            'DepartureDateandTime = %s AND ' \
            'DepartureDateAndTime >= DATE(NOW())'
    cursor.execute(query, (source_city, destination_city, departure_date_and_time))
    # stores the results in a variable
    data = cursor.fetchall()
    error = None
    if data:
        headings = ("Airline Name", "Flight Number", "Departure Airport",
                    "Arrival Airport", "Departure Date and Time", "Arrival Date and Time", "Purchase")
        return render_template('home_templates/search_one_way.html', is_customer=session.get('is_customer'),
                               headings=headings, data=data)
    else:
        error = "No future one way flights found for that search result"
        return render_template('home_templates/search_one_way.html', is_customer=session.get('is_customer'),
                               error=error)


# Define route for querying for round trip flights
@app.route('/search_round_trip_query', methods=['GET', 'POST'])
def search_round_trip_query():
    # grabs information from the forms
    source_city = request.form['Source City/Airport Name']
    destination_city = request.form['Destination City/Airport Name']
    departure_date_and_time = request.form['Departure Date and Time']
    return_date_and_time = request.form['Return Date and Time']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT AirlineName, FlightNumber, DepartureAirportName, ' \
            'ArrivalAirportName, DepartureDateandTime, ArrivalDateandTime ' \
            'FROM flight WHERE ' \
            'DepartureAirportName = %s AND ' \
            'ArrivalAirportName = %s AND ' \
            'DepartureDateandTime = %s AND ' \
            'DepartureDateAndTime >= DATE(NOW())'
    cursor.execute(query, (source_city, destination_city, departure_date_and_time))
    data1 = cursor.fetchall()
    cursor.execute(query, (destination_city, source_city, return_date_and_time))
    data2 = cursor.fetchall()
    error = None
    if data1 and data2:
        headings = ("Airline Name", "Flight Number", "Departure Airport",
                    "Arrival Airport", "Departure Date and Time", "Arrival Date and Time")
        return render_template('home_templates/search_round_trip.html', is_customer=session.get('is_customer'),
                               headings=headings, data1=data1, data2=data2)
    else:
        error = "No future round trip flights found for that search result"
        return render_template('home_templates/search_round_trip.html', is_customer=session.get('is_customer'),
                               error=error)


@app.route('/purchase_ticket/<row_data>')
def purchase_ticket(row_data):
    return render_template('customer_templates/purchase_ticket.html')


# Define route for customer home page
@app.route('/customer_home')
def customer_home():
    if session.get('is_customer'):
        email = session['email']
        # cursor used to send queries
        cursor = conn.cursor()
        # executes query
        query = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM flight'
        cursor.execute(query)
        # stores the results in a variable
        data = cursor.fetchall()
        cursor.close()
        headings = ("Airline Name", "Flight Number", "Departure Date and Time", "Arrival Date and Time", "Status")
        return render_template('customer_templates/customer_home.html', email=email, headings=headings, data=data)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


# Define route for customer to view previous flights
@app.route('/customer_view_previous_flights')
def customer_view_previous_flights():
    if session.get('is_customer'):
        email = session['email']
        # cursor used to send queries
        cursor = conn.cursor()
        # executes query
        # All previous flights for which this customer bought tickets
        # AND already flew on, so they can't rate mid flight for instance
        query = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, ' \
                'Status, Class, ticket.TicketIDNumber FROM ticket NATURAL JOIN flight, purchase ' \
                'WHERE purchase.TicketIDNumber = ticket.TicketIDNumber AND EmailAddress = %s ' \
                'AND ArrivalDateandTime < DATE(NOW())'
        cursor.execute(query, email)
        data = cursor.fetchall()
        headings = ("Airline Name", "Flight Number", "Departure Date and Time", "Arrival Date and Time", "Status",
                    "Class", "TicketIDNumber")
        return render_template('customer_templates/customer_view_previous_flights.html', email=email,
                               headings=headings, data=data)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


# Define route for customer to rate and comment on previous flights
@app.route('/customer_rate_and_comment', methods=['GET', 'POST'])
def customer_rate_and_comment():
    if session.get('is_customer'):
        email = session['email']
        rating = request.form['Rating']
        comment = request.form['Comment']
        ticket_id_number = request.form['TicketIDNumber']
        cursor = conn.cursor()
        query = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ticket.TicketIDNumber ' \
                'FROM ticket NATURAL JOIN flight, purchase ' \
                'WHERE purchase.TicketIDNumber = ticket.TicketIDNumber AND ticket.TicketIDNumber = %s ' \
                'AND EmailAddress = %s AND ArrivalDateandTime < DATE(NOW())'
        cursor.execute(query, (ticket_id_number, email))
        data = cursor.fetchone()
        message = "Successfully made a rating and comment for the flight!"
        error = None
        if data:
            flight_number = data['FlightNumber']
            departure_date_and_time = data['DepartureDateandTime']
            airline_name = data['AirlineName']
            query = 'SELECT * FROM rate WHERE FlightNumber = %s AND DepartureDateandTime = %s ' \
                    'AND AirlineName = %s AND EmailAddress = %s'
            cursor.execute(query, (flight_number, departure_date_and_time, airline_name, email))
            data = cursor.fetchall()
            if not data:
                query = 'INSERT INTO rate VALUES(%s,%s,%s,%s,%s,%s)'
                cursor.execute(query, (rating, comment, flight_number, departure_date_and_time, airline_name, email))
                conn.commit()
            else:
                message = None
                error = "Customer already commented and rated that flight"
        else:
            message = None
            error = "Entered an invalid ticket ID"
        query = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, ' \
                'Status, Class, ticket.TicketIDNumber FROM ticket NATURAL JOIN flight, purchase ' \
                'WHERE purchase.TicketIDNumber = ticket.TicketIDNumber AND EmailAddress = %s ' \
                'AND ArrivalDateandTime < DATE(NOW())'
        cursor.execute(query, email)
        data = cursor.fetchall()
        headings = ("Airline Name", "Flight Number", "Departure Date and Time", "Arrival Date and Time", "Status",
                    "Class", "TicketIDNumber")
        return render_template('customer_templates/customer_view_previous_flights.html', email=email,
                               headings=headings, data=data, error=error, context=message)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


# Define route for customer to view upcoming flights they purchased
@app.route('/customer_view_upcoming_flights')
def customer_view_upcoming_flights():
    if session.get('is_customer'):
        email = session['email']
        # cursor used to send queries
        cursor = conn.cursor()
        # executes query
        query = 'SELECT TicketIDNumber FROM purchase WHERE EmailAddress = %s'
        cursor.execute(query,email)
        data = cursor.fetchall()
        results = []
        now = datetime.now()
        dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
        if len(data) == 1:
            ticket_id = data[0].get("TicketIDNumber")
            query2 = 'SELECT FlightNumber FROM ticket WHERE TicketIDNumber = %s AND DepartureDateandTime >= %s'
            cursor.execute(query2, (ticket_id, dt_string))
            data1 = cursor.fetchone()
            if data1:
                flight_number = data1.get("FlightNumber")
                query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM ' \
                         'flight WHERE FlightNumber = %s AND DepartureDateandTime >= %s'
                cursor.execute(query3, (flight_number,dt_string))
                results = cursor.fetchall()
                results[0].update({"TicketIDNumber": ticket_id})
        elif len(data) > 1:
            ticket_ids = []
            for items in data:
                ticket_ids.append(items['TicketIDNumber'])
            tuple_ticket_ids = tuple(ticket_ids)
            query2 = 'SELECT FlightNumber, TicketIDNumber FROM ticket WHERE DepartureDateandTime >= %s AND ' \
                     'TicketIDNumber IN {}'.format(str(tuple_ticket_ids))
            cursor.execute(query2, dt_string)
            data1 = cursor.fetchall()
            if len(data1) == 1:
                ticket_id = data1[0].get("TicketIDNumber")
                flight_number = data1[0].get("FlightNumber")
                query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM ' \
                         'flight WHERE FlightNumber = %s AND DepartureDateandTime >= %s'
                cursor.execute(query3, (flight_number, dt_string))
                results = cursor.fetchall()
                results[0].update({"TicketIDNumber": ticket_id})
            elif len(data1) > 1:
                flight_numbers = []
                ticket_ids = []
                for items in data1:
                    ticket_ids.append(items['TicketIDNumber'])
                for item in data1:
                    flight_numbers.append(item['FlightNumber'])
                tuple_flight_numbers = tuple(flight_numbers)
                query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM ' \
                         'flight WHERE DepartureDateandTime >= %s AND FlightNumber IN {}'.format(str(tuple_flight_numbers))
                cursor.execute(query3, dt_string)
                results = cursor.fetchall()
                i = 0
                for item in results:
                    item.update({"TicketIDNumber": tuple_ticket_ids[i]})
                    i += 1
        headings = ("Airline Name", "Flight Number", "Departure Date and Time", "Arrival Date and Time", "Status",
                    "TicketIDNumber")
        return render_template('customer_templates/customer_view_upcoming_flights.html', email=email,
                               headings=headings, data=results)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


# Define route for customer to cancel a flight that is more than 24 hours out
@app.route('/customer_cancel_trip', methods=['GET', 'POST'])
def customer_cancel_trip():
    if session.get('is_customer'):
        email = session['email']
        # grabs information from the forms
        ticket_id_number = request.form['TicketIDNumber']
        can_delete = True
        time_now = datetime.now()
        date_time_string = time_now.strftime('%Y-%m-%d %H:%M:%S')
        time_later = time_now + timedelta(24)
        later_string = time_later.strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.cursor()
        # executes query
        query = 'SELECT * FROM purchase WHERE TicketIDNumber = %s'
        cursor.execute(query, ticket_id_number)
        # stores the results in a variable
        data = cursor.fetchone()
        if not data:
            can_delete = False
        error = None
        query = 'SELECT * From ticket where TicketIDNumber = %s AND DepartureDateandTime > %s'
        cursor.execute(query, (ticket_id_number, later_string))
        data = cursor.fetchone()
        if not data:
            can_delete = False
        results = []
        if can_delete:
            query1 = 'DELETE FROM purchase WHERE TicketIDNumber = %s'
            cursor.execute(query1, ticket_id_number)
            conn.commit()
            query = 'SELECT TicketIDNumber FROM purchase WHERE EmailAddress = %s'
            cursor.execute(query,email)
            data = cursor.fetchall()
            if len(data) == 1:
                ticket_id = data[0].get("TicketIDNumber")
                query2 = 'SELECT FlightNumber FROM ticket WHERE TicketIDNumber = %s AND DepartureDateandTime >= %s'
                cursor.execute(query2,(ticket_id, date_time_string))
                data1 = cursor.fetchone()
                if data1:
                    flight_number = data1.get("FlightNumber")
                    query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status ' \
                             'FROM flight WHERE FlightNumber = %s'
                    cursor.execute(query3, flight_number)
                    results = cursor.fetchall()
                    results[0].update({"TicketIDNumber": ticket_id})
            elif len(data) > 1:
                ticket_ids = []
                for items in data:
                    ticket_ids.append(items['TicketIDNumber'])
                tuple_ticket_ids = tuple(ticket_ids)
                query2 = 'SELECT FlightNumber, TicketIDNumber FROM ticket WHERE DepartureDateandTime >= %s AND ' \
                         'TicketIDNumber IN {}'.format(str(tuple_ticket_ids))
                cursor.execute(query2, date_time_string)
                data1 = cursor.fetchall()
                if len(data1) == 1:
                    ticket_id = data1[0].get("TicketIDNumber")
                    flight_number = data1[0].get("FlightNumber")
                    query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status ' \
                             'FROM flight WHERE FlightNumber = %s'
                    cursor.execute(query3, flight_number)
                    results = cursor.fetchall()
                    results[0].update({"TicketIDNumber": ticket_id})
                elif len(data1) > 1:
                    flight_numbers = []
                    ticket_ids= []
                    for items in data1:
                        ticket_ids.append(items['TicketIDNumber'])
                    for item in data1:
                        flight_numbers.append(item['FlightNumber'])
                    tuple_flight_numbers = tuple(flight_numbers)
                    query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status ' \
                             'FROM flight WHERE FlightNumber IN {}'.format(str(tuple_flight_numbers))
                    cursor.execute(query3)
                    results = cursor.fetchall()
                    i = 0
                    for item in results:
                        item.update({"TicketIDNumber": tuple_ticket_ids[i]})
                        i += 1
            headings = ("Airline Name", "Flight Number", "Departure Date and Time", "Arrival Date and Time", "Status",
                        "TicketIDNumber")
            message = "Successfully cancelled trip!"
            return render_template('customer_templates/customer_view_upcoming_flights.html', email=email,
                                   headings=headings, data=results, context=message)
        else:
            query = 'SELECT TicketIDNumber FROM purchase WHERE EmailAddress = %s'
            cursor.execute(query, email)
            data = cursor.fetchall()
            if len(data) == 1:
                ticket_id = data[0].get("TicketIDNumber")
                query2 = 'SELECT FlightNumber FROM ticket WHERE TicketIDNumber = %s AND DepartureDateandTime < %s'
                cursor.execute(query2, (ticket_id, date_time_string))
                data1 = cursor.fetchone()
                if data1:
                    flight_number = data1.get("FlightNumber")
                    query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status ' \
                             'FROM flight WHERE FlightNumber = %s'
                    cursor.execute(query3, flight_number)
                    results = cursor.fetchall()
                    results[0].update({"TicketIDNumber": ticket_id})
            elif len(data) > 1:
                ticket_ids = []
                for items in data:
                    ticket_ids.append(items['TicketIDNumber'])
                tuple_ticket_ids = tuple(ticket_ids)
                query2 = 'SELECT FlightNumber, TicketIDNumber FROM ticket WHERE DepartureDateandTime >= %s AND ' \
                         'TicketIDNumber IN {}'.format(str(tuple_ticket_ids))
                cursor.execute(query2, date_time_string)
                data1 = cursor.fetchall()
                if len(data1) == 1:
                    ticket_id = data1[0].get("TicketIDNumber")
                    flight_number = data1[0].get("FlightNumber")
                    query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status ' \
                             'FROM flight WHERE FlightNumber = %s'
                    cursor.execute(query3, flight_number)
                    results = cursor.fetchall()
                    results[0].update({"TicketIDNumber": ticket_id})
                elif len(data1) > 1:
                    flight_numbers = []
                    ticket_ids = []
                    for items in data1:
                        ticket_ids.append(items['TicketIDNumber'])
                    for item in data1:
                        flight_numbers.append(item['FlightNumber'])
                    tuple_flight_numbers = tuple(flight_numbers)
                    query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status ' \
                             'FROM flight WHERE FlightNumber IN {}'.format(str(tuple_flight_numbers))
                    cursor.execute(query3)
                    results = cursor.fetchall()
                    i = 0
                    for item in results:
                        item.update({"TicketIDNumber": tuple_ticket_ids[i]})
                        i += 1
            headings = ("Airline Name", "Flight Number", "Departure Date and Time", "Arrival Date and Time", "Status",
                        "TicketIDNumber")
            error = "Cannot cancel trip, please check ticket ID number!"
            return render_template('customer_templates/customer_view_upcoming_flights.html', email=email,
                                   headings=headings, data=results, error=error)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


# Define route for customer to purchase tickets
@app.route('/customer_purchase_ticket/<row_data>', methods=['GET', 'POST'])
def customer_purchase_ticket(row_data):
    if session.get('is_customer'):
        return render_template('customer_templates/customer_purchase_ticket.html')
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


# Define route for customer to track their spending with a default view of the past 6 months
@app.route('/customer_track_spending')
def customer_track_spending():
    if session.get('is_customer'):
        email = session['email']
        cursor = conn.cursor()
        time_now = datetime.now()
        date_time_string = time_now.strftime('%Y-%m-%d %H:%M:%S')
        default_time = time_now - relativedelta(months=6)
        default_string = default_time.strftime('%Y-%m-%d %H:%M:%S')
        start = default_time.strftime('%Y-%m-%d')
        end = time_now.strftime('%Y-%m-%d')
        default_total_time = time_now - relativedelta(months=12)
        default_total_string = default_total_time.strftime('%Y-%m-%d')
        query = 'SELECT sold_price, PurchaseDateandTime FROM purchase where EmailAddress = %s AND ' \
                'PurchaseDateandTime > %s'
        cursor.execute(query, (email,default_string))
        data = cursor.fetchall()
        monthly_spending = [{"January": 0, "February": 0, "March": 0, "April": 0, "May": 0, "June": 0, "July": 0,
                             "August": 0, "September": 0, "October": 0, "November": 0, "December": 0}]
        total = 0
        if data:
            for item in data:
                date_time = item.get("PurchaseDateandTime")
                money_spent = round(item.get("sold_price"), 2)
                month_string = date_time.strftime("%m")
                if month_string == "01":
                    monthly_spending[0]["January"] += money_spent
                elif month_string == "02":
                    monthly_spending[0]["February"] += money_spent
                elif month_string == "03":
                    monthly_spending[0]["March"] += money_spent
                elif month_string == "04":
                    monthly_spending[0]["April"] += money_spent
                elif month_string == "05":
                    monthly_spending[0]["May"] += money_spent
                elif month_string == "06":
                    monthly_spending[0]["June"] += money_spent
                elif month_string == "07":
                    monthly_spending[0]["July"] += money_spent
                elif month_string == "08":
                    monthly_spending[0]["August"] += money_spent
                elif month_string == "09":
                    monthly_spending[0]["September"] += money_spent
                elif month_string == "10":
                    monthly_spending[0]["October"] += money_spent
                elif month_string == "11":
                    monthly_spending[0]["November"] += money_spent
                elif month_string == "12":
                    monthly_spending[0]["December"] += money_spent
            monthly_spending[0]["January"] = round(monthly_spending[0]["January"], 2)
            monthly_spending[0]["February"] = round(monthly_spending[0]["February"], 2)
            monthly_spending[0]["March"] = round(monthly_spending[0]["March"], 2)
            monthly_spending[0]["April"] = round(monthly_spending[0]["April"], 2)
            monthly_spending[0]["May"] = round(monthly_spending[0]["May"], 2)
            monthly_spending[0]["June"] = round(monthly_spending[0]["June"], 2)
            monthly_spending[0]["July"] = round(monthly_spending[0]["July"], 2)
            monthly_spending[0]["August"] = round(monthly_spending[0]["August"], 2)
            monthly_spending[0]["September"] = round(monthly_spending[0]["September"], 2)
            monthly_spending[0]["October"] = round(monthly_spending[0]["October"], 2)
            monthly_spending[0]["November"] = round(monthly_spending[0]["November"], 2)
            monthly_spending[0]["December"] = round(monthly_spending[0]["December"], 2)
            query = 'SELECT sold_price, PurchaseDateandTime FROM purchase where EmailAddress = %s AND ' \
                    'PurchaseDateandTime > %s'
            cursor.execute(query, (email, default_total_string))
            data = cursor.fetchall()
            for item in data:
                total += round(item.get("sold_price"), 2)
            total = round(total, 2)
            cursor.close()
            headings = ("January", "February", "March", "April", "May", "June", "July", "August", "September",
                        "October", "November", "December")
            return render_template('customer_templates/customer_track_spending.html', email=email, headings=headings,
                                   data=monthly_spending, start=start, end=end, start_year=default_total_string,
                                   end_year=end, total=total)

        else:
            cursor.close()
            headings = ("January", "February", "March", "April", "May", "June", "July", "August", "September",
                        "October", "November", "December")
            return render_template('customer_templates/customer_track_spending.html', email=email, headings=headings,
                                   data=monthly_spending, start=start, end=end, start_year=default_total_string,
                                   end_year=end, total=total)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


# Define route for customer to track their spending with a custom range of dates
@app.route('/customer_track_spending_custom', methods=['GET', 'POST'])
def customer_track_spending_custom():
    if session.get('is_customer'):
        email = session['email']
        cursor = conn.cursor()
        time_now = datetime.now()
        date_time_string = time_now.strftime('%Y-%m-%d %H:%M:%S')
        default_time = time_now - relativedelta(months=6)
        default_string = default_time.strftime('%Y-%m-%d %H:%M:%S')
        start_date = request.form['start_date']
        start_list = start_date.split('-')
        start_list = list(map(int, start_list))
        end_date = request.form['end_date']
        end_list = end_date.split('-')
        end_list = list(map(int, end_list))
        start_datetime = datetime(start_list[0], start_list[1], start_list[2])
        end_datetime = datetime(end_list[0], end_list[1], end_list[2])
        valid_date = True
        if end_datetime > time_now:
            valid_date = False
        start_string = start_datetime.strftime('%Y-%m-%d %H:%M:%S')
        end_string = end_datetime.strftime('%Y-%m-%d %H:%M:%S')
        query = 'SELECT sold_price, PurchaseDateandTime FROM purchase where EmailAddress = %s AND ' \
                'PurchaseDateandTime > %s and PurchaseDateandTime < %s'
        cursor.execute(query, (email, start_string, end_string))
        data = cursor.fetchall()
        monthly_spending = [{"January": 0, "February": 0, "March": 0, "April": 0, "May": 0, "June": 0, "July": 0,
                             "August": 0, "September": 0, "October": 0, "November": 0, "December": 0}]
        total_spending = 0
        if data and valid_date:
            for item in data:
                date_time = item.get("PurchaseDateandTime")
                money_spent = round(item.get("sold_price"), 2)
                month_string = date_time.strftime("%m")
                if month_string == "01":
                    monthly_spending[0]["January"] += money_spent
                    total_spending += money_spent
                elif month_string == "02":
                    monthly_spending[0]["February"] += money_spent
                    total_spending += money_spent
                elif month_string == "03":
                    monthly_spending[0]["March"] += money_spent
                    total_spending += money_spent
                elif month_string == "04":
                    monthly_spending[0]["April"] += money_spent
                    total_spending += money_spent
                elif month_string == "05":
                    monthly_spending[0]["May"] += money_spent
                    total_spending += money_spent
                elif month_string == "06":
                    monthly_spending[0]["June"] += money_spent
                    total_spending += money_spent
                elif month_string == "07":
                    monthly_spending[0]["July"] += money_spent
                    total_spending += money_spent
                elif month_string == "08":
                    monthly_spending[0]["August"] += money_spent
                    total_spending += money_spent
                elif month_string == "09":
                    monthly_spending[0]["September"] += money_spent
                    total_spending += money_spent
                elif month_string == "10":
                    monthly_spending[0]["October"] += money_spent
                    total_spending += money_spent
                elif month_string == "11":
                    monthly_spending[0]["November"] += money_spent
                    total_spending += money_spent
                elif month_string == "12":
                    monthly_spending[0]["December"] += money_spent
                    total_spending += money_spent
            monthly_spending[0]["January"] = round(monthly_spending[0]["January"], 2)
            monthly_spending[0]["February"] = round(monthly_spending[0]["February"], 2)
            monthly_spending[0]["March"] = round(monthly_spending[0]["March"], 2)
            monthly_spending[0]["April"] = round(monthly_spending[0]["April"], 2)
            monthly_spending[0]["May"] = round(monthly_spending[0]["May"], 2)
            monthly_spending[0]["June"] = round(monthly_spending[0]["June"], 2)
            monthly_spending[0]["July"] = round(monthly_spending[0]["July"], 2)
            monthly_spending[0]["August"] = round(monthly_spending[0]["August"], 2)
            monthly_spending[0]["September"] = round(monthly_spending[0]["September"], 2)
            monthly_spending[0]["October"] = round(monthly_spending[0]["October"], 2)
            monthly_spending[0]["November"] = round(monthly_spending[0]["November"], 2)
            monthly_spending[0]["December"] = round(monthly_spending[0]["December"], 2)
            total_spending = round(total_spending, 2)
            cursor.close()
            headings = ("January", "February", "March", "April", "May", "June", "July", "August", "September",
                        "October", "November", "December")
            return render_template('customer_templates/customer_track_spending.html', email=email, headings=headings,
                                   data=monthly_spending, start=start_date, end=end_date, start_year=start_date,
                                   end_year=end_date, total=total_spending)
        elif data:
            cursor.close()
            error = "Invalid Range of Dates!"
            headings = ("January", "February", "March", "April", "May", "June", "July", "August", "September",
                        "October", "November", "December")
            return render_template('customer_templates/customer_track_spending.html', email=email, headings=headings,
                                   data=monthly_spending, error=error, start=start_date, end=end_date,
                                   start_year=start_date, end_year=end_date, total=total_spending)
        else:
            cursor.close()
            headings = ("January", "February", "March", "April", "May", "June", "July", "August", "September",
                        "October", "November", "December")
            return render_template('customer_templates/customer_track_spending.html', email=email, headings=headings,
                                   data=monthly_spending, start=start_date, end=end_date, start_year=start_date,
                                   end_year=end_date, total=total_spending)
    else:
        return render_template('home_templates/unauthorized_access.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'))


@app.route('/customer_logout')
def customer_logout():
    session.pop('email')
    session.pop('is_customer')
    return redirect('/')


@app.route('/airline_staff_logout')
def airline_staff_logout():
    session.pop('username')
    session.pop('is_airline_staff')
    return redirect('/')


def md5(password):
    result = hashlib.md5(password.encode())
    return result.hexdigest()


app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
    
      



