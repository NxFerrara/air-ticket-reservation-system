# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import hashlib

# Initialize the app from Flask
app = Flask(__name__)

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=8889,  # change this every time if you are a Windows user
                       user='root',
                       password='root',  # change this every time if you are Windows user
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
        cursor.execute(ins, (name, email, password, building_number, street, city, state,
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
        cursor.execute(ins, (username, password, first_name, last_name, date_of_birth, airline_name))
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
        return redirect(url_for('airline_staff_home'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('airline_staff_templates/airline_staff_login.html', error=error)


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


@app.route('/delete_flight', methods=['GET', 'POST'])
def delete_flight():
    # grabs information from the forms
    ticketid_number = request.form['TicketIDNumber']
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM purchase WHERE TicketIDNumber = %s'
    cursor.execute(query,ticketid_number)
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    results = []
    if data:
        query1 = 'DELETE FROM purchase WHERE TicketIDNumber = %s'
        cursor.execute(query1, ticketid_number)
        conn.commit()
        email = session['email']
        # cursor used to send queries
        # executes query
        query = 'SELECT TicketIDNumber FROM purchase WHERE EmailAddress = %s'
        cursor.execute(query,email)
        data = cursor.fetchall()
        if len(data) == 1:
            ticketid = data[0].get("TicketIDNumber")
            query2 = 'SELECT FlightNumber FROM ticket WHERE TicketIDNumber = %s'
            cursor.execute(query2,ticketid)
            data1 = cursor.fetchone()
            flightnumber = data1.get("FlightNumber")
            query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM flight WHERE FlightNumber = %s'
            cursor.execute(query3, flightnumber)
            results = cursor.fetchall()
            results[0].update({"TicketIDNumber": ticketid})
        elif len(data) > 1:
            ticketids= []
            for items in data:
                ticketids.append(items['TicketIDNumber'])
            tupleticketids = tuple(ticketids)
            query2 = 'SELECT FlightNumber FROM ticket WHERE TicketIDNumber IN {}'.format(str(tupleticketids))
            cursor.execute(query2)
            data1 = cursor.fetchall()
            flightnumbers = []
            for item in data1:
                flightnumbers.append(item['FlightNumber'])
            tupleflightnumbers = tuple(flightnumbers)
            query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM flight WHERE FlightNumber IN {}'.format(str(tupleflightnumbers))
            cursor.execute(query3)
            results = cursor.fetchall()
            i = 0
            for item in results:
                item.update({"TicketIDNumber": tupleticketids[i]})
                i+=1
        headings = ("Airline Name", "Flight Number", "Departure Date and Time", "Arrival Date and Time", "Status", "TicketIDNumber")
        return render_template('customer_templates/customer_flights.html', email=email, headings=headings, data=results)
    else:
        # returns an error message to the html page
        email = session['email']
        # cursor used to send queries
        # executes query
        query = 'SELECT TicketIDNumber FROM purchase WHERE EmailAddress = %s'
        cursor.execute(query,email)
        data = cursor.fetchall()
        results = []
        if len(data) == 1:
            ticketid = data[0].get("TicketIDNumber")
            query2 = 'SELECT FlightNumber FROM ticket WHERE TicketIDNumber = %s'
            cursor.execute(query2,ticketid)
            data1 = cursor.fetchone()
            flightnumber = data1.get("FlightNumber")
            query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM flight WHERE FlightNumber = %s'
            cursor.execute(query3, flightnumber)
            results = cursor.fetchall()
            results[0].update({"TicketIDNumber": ticketid})
        elif len(data) > 1:
            ticketids= []
            for items in data:
                ticketids.append(items['TicketIDNumber'])
            tupleticketids = tuple(ticketids)
            query2 = 'SELECT FlightNumber FROM ticket WHERE TicketIDNumber IN {}'.format(str(tupleticketids))
            cursor.execute(query2)
            data1 = cursor.fetchall()
            flightnumbers = []
            for item in data1:
                flightnumbers.append(item['FlightNumber'])
            tupleflightnumbers = tuple(flightnumbers)
            query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM flight WHERE FlightNumber IN {}'.format(str(tupleflightnumbers))
            cursor.execute(query3)
            results = cursor.fetchall()
            i = 0
            for item in results:
                item.update({"TicketIDNumber": tupleticketids[i]})
                i+=1
        headings = ("Airline Name", "Flight Number", "Departure Date and Time", "Arrival Date and Time", "Status", "TicketIDNumber")
        error = 'Invalid TicketIDNumber'
        return render_template('customer_templates/customer_flights.html', email=email, headings =headings, data = results, error=error)



@app.route('/view_my_flights')
def view_my_flights():
    email = session['email']
    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT TicketIDNumber FROM purchase WHERE EmailAddress = %s'
    cursor.execute(query,email)
    data = cursor.fetchall()
    results = []
    if len(data) == 1:
        ticketid = data[0].get("TicketIDNumber")
        query2 = 'SELECT FlightNumber FROM ticket WHERE TicketIDNumber = %s'
        cursor.execute(query2,ticketid)
        data1 = cursor.fetchone()
        flightnumber = data1.get("FlightNumber")
        query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM flight WHERE FlightNumber = %s'
        cursor.execute(query3, flightnumber)
        results = cursor.fetchall()
        results[0].update({"TicketIDNumber": ticketid})
    elif len(data) > 1:
        ticketids= []
        for items in data:
            ticketids.append(items['TicketIDNumber'])
        tupleticketids = tuple(ticketids)
        query2 = 'SELECT FlightNumber FROM ticket WHERE TicketIDNumber IN {}'.format(str(tupleticketids))
        cursor.execute(query2)
        data1 = cursor.fetchall()
        flightnumbers = []
        for item in data1:
            flightnumbers.append(item['FlightNumber'])
        tupleflightnumbers = tuple(flightnumbers)
        query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM flight WHERE FlightNumber IN {}'.format(str(tupleflightnumbers))
        cursor.execute(query3)
        results = cursor.fetchall()
        i = 0
        for item in results:
            item.update({"TicketIDNumber": tupleticketids[i]})
            i+=1
    headings = ("Airline Name", "Flight Number", "Departure Date and Time", "Arrival Date and Time", "Status", "TicketIDNumber")
    return render_template('customer_templates/customer_flights.html', email=email, headings=headings, data=results)


@app.route('/airline_staff_home')
def airline_staff_home():
    username = session['username']
    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM flight'
    cursor.execute(query)
    # stores the results in a variable
    data = cursor.fetchall()
    cursor.close()
    headings = ("Airline Name", "Flight Number", "Departure Date and Time", "Arrival Date and Time", "Status")
    return render_template('airline_staff_templates/airline_staff_home.html', username=username, headings=headings,
                           data=data)


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
