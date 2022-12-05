# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import hashlib
import datetime

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


@app.route('/insert_new_flight')
def insert_new_flight():
    if session.get('is_airline_staff'):
        airlineName = session['airline_name']
        # cursor used to send queries
        cursor = conn.cursor()
        query = 'SELECT AirlineName, FlightNumber, DepartureAirportName, ArrivalAirportName, ' \
                'DepartureDateandTime, ArrivalDateandTime, BasePrice, Status FROM flight ' \
                'WHERE AirlineName = "{}" AND DepartureDateandTime >= DATE(NOW()) AND ' \
                'DepartureDateandTime <= DATE(NOW() + INTERVAL 30 DAY);'.format(airlineName)
        cursor.execute(query)
        # stores the results in a variable
        data = cursor.fetchall()
        cursor.close()
        headings = ("Airline Name", "Flight Number", "Departure Airport", "Arrival Airport",
                    "Departure Date and Time", "Arrival Date and Time", "Base Price", "Status")
        return render_template('airline_staff_templates/airline_staff_insert.html', headings=headings, data=data)
    elif session.get('is_customer'):
        return render_template('customer_templates/customer_home.html')
    else:
        return redirect('/')

@app.route('/exec_insert_new_flight', methods=['GET', 'POST'])
def exec_insert_new_flight():
    if session.get('is_airline_staff'):
        airlineName = session['airline_name']
        # grabs information from the forms
        DepartureDateandTime = request.form['DepartureDateandTime']
        DepartureDateandTime = datetime.datetime.strptime(DepartureDateandTime, "%Y-%m-%dT%H:%M").strftime(
            '%Y-%m-%d %H:%M:%S')
        ArrivalDateandTime = request.form['ArrivalDateandTime']
        ArrivalDateandTime = DepartureDateandTime = datetime.datetime.strptime(ArrivalDateandTime, "%Y-%m-%dT%H:%M").strftime('%Y-%m-%d %H:%M:%S')
        BasePrice = request.form['BasePrice']
        DepartureAirportName = request.form['DepartureAirportName']
        ArrivalAirportName = request.form['ArrivalAirportName']
        IDNumber = request.form['IDNumber']
        Status = 'On-time'  # By default
        AirlineName = session['airline_name']  # By default

        # cursor used to send queries
        cursor = conn.cursor()
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
            FlightNumber = maxFlightNumber+1

        # This query checks to make sure one airplane isn't flying multiple flights at
        # the same time within the same airline
        query = 'SELECT * FROM flight WHERE IDNumber = %s AND DepartureDateandTime = %s AND AirlineName = %s'
        cursor.execute(query, (IDNumber, DepartureDateandTime, AirlineName))
        # stores the results in a variable
        data = cursor.fetchone()
        # Checking the departure and arrival airports exist and also the airplane
        query = 'SELECT * FROM airport WHERE AirportName = %s'
        cursor.execute(query, DepartureAirportName)
        # stores the results in a variable
        is_departure_airport = cursor.fetchone()
        query = 'SELECT * FROM airport WHERE AirportName = %s'
        cursor.execute(query, ArrivalAirportName)
        # stores the results in a variable
        is_arrival_airport = cursor.fetchone()
        query = 'SELECT * FROM airplane WHERE IDNumber = %s AND AirlineName = %s'
        cursor.execute(query, (IDNumber, airlineName))
        # stores the results in a variable
        is_airplane = cursor.fetchone()
        # use fetchall() if you are expecting more than 1 data row
        # Query all of the future flights
        query = 'SELECT AirlineName, FlightNumber, DepartureAirportName, ArrivalAirportName, ' \
                'DepartureDateandTime, ArrivalDateandTime, BasePrice, Status FROM flight ' \
                'WHERE AirlineName = "{}" AND DepartureDateandTime >= DATE(NOW()) AND ' \
                'DepartureDateandTime <= DATE(NOW() + INTERVAL 30 DAY);'.format(airlineName)
        headings = ("Airline Name", "Flight Number", "Departure Airport", "Arrival Airport",
                    "Departure Date and Time", "Arrival Date and Time", "Base Price", "Status")
        error = None
        context = None
        if data:
            cursor.execute(query)
            # stores the results in a variable
            futureFlights = cursor.fetchall()
            cursor.close()
            # If the previous query returns data, then user exists
            error = "This flight already exists!"
            return render_template('airline_staff_templates/airline_staff_insert.html', error=error,
                                   headings=headings, data=futureFlights)
        else:
            if not is_departure_airport:
                cursor.execute(query)
                # stores the results in a variable
                futureFlights = cursor.fetchall()
                cursor.close()
                error = "The {} Airport doesn't exist!".format(DepartureAirportName)
                return render_template('airline_staff_templates/airline_staff_insert.html', error=error,
                                       headings=headings, data=futureFlights)
            elif not is_arrival_airport:
                cursor.execute(query)
                # stores the results in a variable
                futureFlights = cursor.fetchall()
                cursor.close()
                error = "The {} Airport doesn't exist!".format(ArrivalAirportName)
                return render_template('airline_staff_templates/airline_staff_insert.html', error=error,
                                       headings=headings, data=futureFlights)
            elif not is_airplane:
                cursor.execute(query)
                # stores the results in a variable
                futureFlights = cursor.fetchall()
                cursor.close()
                error = "The airplane with ID number {} doesn't exist!".format(IDNumber)
                return render_template('airline_staff_templates/airline_staff_insert.html', error=error,
                                       headings=headings, data=futureFlights)
            else:
                ins = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(ins, (str(FlightNumber), DepartureDateandTime, ArrivalDateandTime, BasePrice, Status, DepartureAirportName,
                ArrivalAirportName, IDNumber, AirlineName))
                conn.commit()
                cursor.execute(query)
                # stores the results in a variable
                futureFlights = cursor.fetchall()
                cursor.close()
                message = "New flight successfully added!"
                return render_template('airline_staff_templates/airline_staff_insert.html', context=message,
                                       headings=headings, data=flightData)
    elif session.get('is_customer'):
        return render_template('customer_templates/customer_home.html')
    else:
        return redirect('/')


# Define route for airline staff to search for flights
@app.route('/search_flights_airline_staff')
def search_flights_airline_staff():
    if session.get('is_airline_staff'):
        return render_template('airline_staff_templates/search_flights_airline_staff.html')
    elif session.get('is_customer'):
        return render_template('customer_templates/customer_home.html')
    else:
        return redirect('/')


@app.route('/search_flights_airline_staff_query', methods=['GET', 'POST'])
def search_flights_airline_staff_query():
    if session.get('is_airline_staff'):
        airline_name = session['airline_name']
        # grabs information from the forms
        source_city = request.form['Source City/Airport Name']
        destination_city = request.form['Destination City/Airport Name']
        start_departure_date_and_time = request.form['StartDepartureDateandTime']
        start_departure_date_and_time = datetime.datetime.strptime(start_departure_date_and_time,
                                                                   "%Y-%m-%dT%H:%M").strftime('%Y-%m-%d %H:%M:%S')
        end_departure_date_and_time = request.form['EndDepartureDateandTime']
        has_end_date = False
        if end_departure_date_and_time != "":
            has_end_date = True
            end_departure_date_and_time = datetime.datetime.strptime(end_departure_date_and_time,
                                                                     "%Y-%m-%dT%H:%M").strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.cursor()
        # Checking the departure and arrival airports exist
        query = 'SELECT * FROM airport WHERE AirportName = %s'
        cursor.execute(query, source_city)
        # stores the results in a variable
        is_departure_airport = cursor.fetchone()
        query = 'SELECT * FROM airport WHERE AirportName = %s'
        cursor.execute(query, destination_city)
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
                    'ArrivalAirportName, DepartureDateandTime, ArrivalDateandTime ' \
                    'FROM flight WHERE ' \
                    'AirlineName = %s AND ' \
                    'DepartureAirportName = %s AND ' \
                    'ArrivalAirportName = %s AND ' \
                    'DepartureDateandTime >= %s AND ' \
                    'DepartureDateAndTime <= %s'
            cursor.execute(query, (airline_name, source_city, destination_city, start_departure_date_and_time, end_departure_date_and_time))
        else:
            # executes query
            query = 'SELECT AirlineName, FlightNumber, DepartureAirportName, ' \
                    'ArrivalAirportName, DepartureDateandTime, ArrivalDateandTime ' \
                    'FROM flight WHERE ' \
                    'AirlineName = %s AND ' \
                    'DepartureAirportName = %s AND ' \
                    'ArrivalAirportName = %s AND ' \
                    'DepartureDateandTime >= %s'
            cursor.execute(query, (airline_name, source_city, destination_city, start_departure_date_and_time))
        data = cursor.fetchall()
        if data:
            headings = ("Airline Name", "Flight Number", "Departure Airport",
                        "Arrival Airport", "Departure Date and Time", "Arrival Date and Time", "View Customers")
            return render_template('airline_staff_templates/search_flights_airline_staff.html', headings=headings, data=data)
        else:
            error = "No flights found for that search result"
            return render_template('airline_staff_templates/search_flights_airline_staff.html', error=error)
    elif session.get('is_customer'):
        return render_template('customer_templates/customer_home.html')
    else:
        return redirect('/')


@app.route('/view_flight_customers/<flightData>')
def view_flight_customers(flightData):
    if session.get('is_airline_staff'):
        flightData = eval(flightData)
        query = 'SELECT DISTINCT Name FROM Purchase Natural Join Customer, Ticket WHERE ' \
                'Ticket.TicketIDNumber = Purchase.TicketIDNumber AND Ticket.TicketIDNumber ' \
                'IN(SELECT TicketIDNumber FROM Flight Natural Join Ticket WHERE ' \
                'Flight.AirlineName = "{}" AND ' \
                'Flight.FlightNumber = "{}" AND ' \
                'Flight.DepartureDateandTime = "{}")'.format(flightData['AirlineName'],
                                                             flightData['FlightNumber'],
                                                             flightData['DepartureDateandTime'].strftime('%Y-%m-%d %H:%M:%S'))
        # cursor used to send queries
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        error = None
        if data:
            headings = ("Name",)
            return render_template('airline_staff_templates/airline_staff_view_flight_customers.html',
                                   headings=headings,
                                   data=data)
        else:
            error = "No customers found for that flight"
            return render_template('airline_staff_templates/airline_staff_view_flight_customers.html', error=error)
    elif session.get('is_customer'):
        return render_template('customer_templates/customer_home.html')
    else:
        return redirect('/')


# Define route for user to search for flights
@app.route('/search_flights')
def search_flights():
    return render_template('home_templates/search_for_flights.html', is_customer=session.get('is_customer'),
                           is_airline_staff=session.get('is_airline_staff'))


# Define route for user to search for flights
@app.route('/search_one_way')
def search_one_way():
    return render_template('home_templates/search_one_way.html', is_customer=session.get('is_customer'),
                           is_airline_staff=session.get('is_airline_staff'))


# Define route for user to search for flights
@app.route('/search_round_trip')
def search_round_trip():
    return render_template('home_templates/search_round_trip.html', is_customer=session.get('is_customer'),
                           is_airline_staff=session.get('is_airline_staff'))


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
                               is_airline_staff=session.get('is_airline_staff'), headings=headings, data=data)
    else:
        error = "No future one way flights found for that search result"
        return render_template('home_templates/search_one_way.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'), error=error)


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
                               is_airline_staff=session.get('is_airline_staff'), headings=headings,
                               data1=data1, data2=data2)
    else:
        error = "No future round trip flights found for that search result"
        return render_template('home_templates/search_round_trip.html', is_customer=session.get('is_customer'),
                               is_airline_staff=session.get('is_airline_staff'), error=error)


@app.route('/purchase_ticket/<row_data>')
def purchase_ticket(row_data):
    return render_template('customer_templates/purchase_ticket.html')


@app.route('/customer_home')
def customer_home():
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
                'WHERE AirlineName = "{}" AND DepartureDateandTime >= DATE(NOW()) AND ' \
                'DepartureDateandTime <= DATE(NOW() + INTERVAL 30 DAY);'.format(airlineName)
        cursor.execute(query)
        # stores the results in a variable
        data = cursor.fetchall()
        cursor.close()
        headings = ("Airline Name", "Flight Number", "Departure Airport", "Arrival Airport",
                    "Departure Date and Time", "Arrival Date and Time", "Base Price", "Status")
        return render_template('airline_staff_templates/airline_staff_home.html', username=username, headings=headings,
                               data=data)
    elif session.get('is_customer'):
        return render_template('customer_templates/customer_home.html')
    else:
        return redirect('/')


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
