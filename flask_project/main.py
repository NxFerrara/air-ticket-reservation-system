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
    # use fetchall() if you arex expecting more than 1 data row
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

@app.route('/track_spending',methods=['GET', 'POST'])
def track_spending():
    email = session['email']
    cursor=conn.cursor()
    now = datetime.now()
    dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
    default_time = now - relativedelta(months = 6)
    default_string = default_time.strftime('%Y-%m-%d %H:%M:%S')
    start_date = request.form['start_date']
    start_list = start_date.split('-')
    print(start_list)
    start_list = list(map(int,start_list))
    print(start_list)
    end_date = request.form['end_date']
    end_list = end_date.split('-')
    end_list = list(map(int,end_list))
    start_datetime = datetime(start_list[0],start_list[1],start_list[2])
    end_datetime = datetime(end_list[0],end_list[1],end_list[2])
    valid_date = True
    if end_datetime > now:
        valid_date = False
    start_string = start_datetime.strftime('%Y-%m-%d %H:%M:%S')
    end_string = end_datetime.strftime('%Y-%m-%d %H:%M:%S')
    query = 'SELECT sold_price, PurchaseDateandTime FROM purchase where EmailAddress = %s AND PurchaseDateandTime > %s and PurchaseDateandTime < %s'
    cursor.execute(query, (email,start_string, end_string))
    data = cursor.fetchall()
    print(data)
    monthly_spending = [{"January":0, "February": 0, "March":0, "April": 0, "May": 0, "June":0, "July":0, "August":0,
                        "September":0, "October":0, "November":0, "December":0}]
    if (data) and (valid_date):
        for item in data:
            date_time = item.get("PurchaseDateandTime")
            money_spent = round(item.get("sold_price"),2)
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
        monthly_spending[0]["January"] = round(monthly_spending[0]["January"],2)
        monthly_spending[0]["February"] = round(monthly_spending[0]["February"],2)
        monthly_spending[0]["March"] = round(monthly_spending[0]["March"],2)
        monthly_spending[0]["April"] = round(monthly_spending[0]["April"],2)
        monthly_spending[0]["May"] = round(monthly_spending[0]["May"],2)
        monthly_spending[0]["June"] = round(monthly_spending[0]["June"],2)
        monthly_spending[0]["July"] = round(monthly_spending[0]["July"],2)
        monthly_spending[0]["August"] = round(monthly_spending[0]["August"],2)
        monthly_spending[0]["September"] = round(monthly_spending[0]["September"],2)
        monthly_spending[0]["October"] = round(monthly_spending[0]["October"],2)
        monthly_spending[0]["November"] = round(monthly_spending[0]["November"],2)
        monthly_spending[0]["December"] = round(monthly_spending[0]["December"],2)
        cursor.close()
        headings = ("January", "February", "March", "April", "May", "June", "July","August", "September", "October",
                    "November","December")
        return render_template('customer_templates/customer_spending.html', email=email, headings=headings, data=monthly_spending, start = start_date, end = end_date)
    elif (data):
        cursor.close()
        error = "Invalid Date"
        headings = ("January", "February", "March", "April", "May", "June", "July","August", "September", "October",
                    "November","December")
        return render_template('customer_templates/customer_spending.html', email=email, headings=headings, data=monthly_spending, error = error, start = start_date, end = end_date)
    else:
        cursor.close()
        headings = ("January", "February", "March", "April", "May", "June", "July","August", "September", "October",
                    "November","December")
        return render_template('customer_templates/customer_spending.html', email=email, headings=headings, data=monthly_spending, start = start_date, end = end_date)



@app.route('/customer_spending')
def customer_spending():
    email = session['email']
    cursor=conn.cursor()
    now = datetime.now()
    dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
    default_time = now - relativedelta(months = 6)
    default_string = default_time.strftime('%Y-%m-%d %H:%M:%S')
    end = now.strftime('%Y-%m-%d')
    start = default_time.strftime('%Y-%m-%d')
    query = 'SELECT sold_price, PurchaseDateandTime FROM purchase where EmailAddress = %s AND PurchaseDateandTime > %s'
    cursor.execute(query, (email,default_string))
    data = cursor.fetchall()
    print(data)
    monthly_spending = [{"January":0, "February": 0, "March":0, "April": 0, "May": 0, "June":0, "July":0, "August":0,
                        "September":0, "October":0, "November":0, "December":0}]
    if data:
        for item in data:
            date_time = item.get("PurchaseDateandTime")
            money_spent = round(item.get("sold_price"),2)
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
        monthly_spending[0]["January"] = round(monthly_spending[0]["January"],2)
        monthly_spending[0]["February"] = round(monthly_spending[0]["February"],2)
        monthly_spending[0]["March"] = round(monthly_spending[0]["March"],2)
        monthly_spending[0]["April"] = round(monthly_spending[0]["April"],2)
        monthly_spending[0]["May"] = round(monthly_spending[0]["May"],2)
        monthly_spending[0]["June"] = round(monthly_spending[0]["June"],2)
        monthly_spending[0]["July"] = round(monthly_spending[0]["July"],2)
        monthly_spending[0]["August"] = round(monthly_spending[0]["August"],2)
        monthly_spending[0]["September"] = round(monthly_spending[0]["September"],2)
        monthly_spending[0]["October"] = round(monthly_spending[0]["October"],2)
        monthly_spending[0]["November"] = round(monthly_spending[0]["November"],2)
        monthly_spending[0]["December"] = round(monthly_spending[0]["December"],2)
        cursor.close()
        headings = ("January", "February", "March", "April", "May", "June", "July","August", "September", "October",
                    "November","December")
        return render_template('customer_templates/customer_spending.html', email=email, headings=headings, data=monthly_spending, start = start, end = end)

    else:
        cursor.close()
        headings = ("January", "February", "March", "April", "May", "June", "July","August", "September", "October",
                    "November","December")
        return render_template('customer_templates/customer_spending.html', email=email, headings=headings, data=monthly_spending, start = start, end = end)





@app.route('/delete_flight', methods=['GET', 'POST'])
def delete_flight():
    # grabs information from the forms
    can_delete = True
    email = session['email']
    ticketid_number = request.form['TicketIDNumber']
    now = datetime.now()
    dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
    later_time = now + timedelta(24)
    later_string = later_time.strftime('%Y-%m-%d %H:%M:%S')
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM purchase WHERE TicketIDNumber = %s'
    cursor.execute(query,ticketid_number)
    # stores the results in a variable
    data = cursor.fetchone()
    if not data:
        can_delete = False
    # use fetchall() if you are expecting more than 1 data row
    error = None
    query = 'SELECT * From ticket where TicketIDNumber = %s AND DepartureDateandTime > %s'
    cursor.execute(query,(ticketid_number,later_string))
    data = cursor.fetchone()
    if not data:
        can_delete = False
    results = []
    if can_delete:
        query1 = 'DELETE FROM purchase WHERE TicketIDNumber = %s'
        cursor.execute(query1, ticketid_number)
        conn.commit()
        query = 'SELECT TicketIDNumber FROM purchase WHERE EmailAddress = %s'
        cursor.execute(query,email)
        data = cursor.fetchall()
        if len(data) == 1:
            ticketid = data[0].get("TicketIDNumber")
            query2 = 'SELECT FlightNumber FROM ticket WHERE TicketIDNumber = %s AND DepartureDateandTime >= %s'
            cursor.execute(query2,(ticketid, dt_string))
            data1 = cursor.fetchone()
            if data1:
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
            query2 = 'SELECT FlightNumber, TicketIDNumber FROM ticket WHERE DepartureDateandTime >= %s AND TicketIDNumber IN {}'.format(str(tupleticketids))
            cursor.execute(query2, dt_string)
            data1 = cursor.fetchall()
            if len(data1) == 1:
                ticketid = data1[0].get("TicketIDNumber")
                flightnumber = data1[0].get("FlightNumber")
                query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM flight WHERE FlightNumber = %s'
                cursor.execute(query3, flightnumber)
                results = cursor.fetchall()
                results[0].update({"TicketIDNumber": ticketid})
            elif len(data1) > 1:
                flightnumbers = []
                ticketids= []
                for items in data1:
                    ticketids.append(items['TicketIDNumber'])
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
        return render_template('customer_templates/customer_future_flights.html', email=email, headings=headings, data=results)
    else:
        query = 'SELECT TicketIDNumber FROM purchase WHERE EmailAddress = %s'
        cursor.execute(query,email)
        data = cursor.fetchall()
        if len(data) == 1:
            ticketid = data[0].get("TicketIDNumber")
            query2 = 'SELECT FlightNumber FROM ticket WHERE TicketIDNumber = %s AND DepartureDateandTime >= %s'
            cursor.execute(query2,(ticketid, dt_string))
            data1 = cursor.fetchone()
            if data1:
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
            query2 = 'SELECT FlightNumber, TicketIDNumber FROM ticket WHERE DepartureDateandTime >= %s AND TicketIDNumber IN {}'.format(str(tupleticketids))
            cursor.execute(query2, dt_string)
            data1 = cursor.fetchall()
            if len(data1) == 1:
                ticketid = data1[0].get("TicketIDNumber")
                flightnumber = data1[0].get("FlightNumber")
                query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM flight WHERE FlightNumber = %s'
                cursor.execute(query3, flightnumber)
                results = cursor.fetchall()
                results[0].update({"TicketIDNumber": ticketid})
            elif len(data1) > 1:
                flightnumbers = []
                ticketids= []
                for items in data1:
                    ticketids.append(items['TicketIDNumber'])
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
        error = "Flight cannot be deleted"
        return render_template('customer_templates/customer_future_flights.html', email=email, headings=headings, data=results, error = error)


@app.route('/rate_and_comment_on_flight', methods=['GET', 'POST'])
def rate_and_comment_on_flight():
    can_rate = True
    now = datetime.now()
    dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
    results = []
    email = session['email']
    comment = request.form['Comment']
    rating = request.form['Rating']
    TicketIDNumber = request.form['TicketIDNumber']
    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT TicketIDNumber FROM purchase WHERE TicketIDNumber = %s and EmailAddress = %s'
    cursor.execute(query,(TicketIDNumber, email))
    data = cursor.fetchall()
    if not data:
        can_rate = False
    query = 'SELECT FlightNumber,DepartureDateandTime, AirlineName FROM ticket WHERE TicketIDNumber = %s AND DepartureDateandTime < %s'
    cursor.execute(query,(TicketIDNumber,dt_string))
    data = cursor.fetchall()
    if data:
        flight_number = data[0].get("FlightNumber")
        query = 'SELECT * FROM rate WHERE EmailAddress = %s AND FlightNumber = %s'
        cursor.execute(query,(email,flight_number))
        rating = cursor.fetchone()
        if rating:
            can_rate = False
    if can_rate:
        email = session['email']
        flight_number = data[0].get("FlightNumber")
        Departure_Date_and_Time = data[0].get("DepartureDateandTime")
        Airline_Name = data[0].get("AirlineName")
        query = 'INSERT INTO rate VALUES(%s,%s,%s,%s,%s,%s)'
        cursor.execute(query,(rating,comment,flight_number,Departure_Date_and_Time,Airline_Name,email))
        conn.commit()
        # cursor used to send queries
        query = 'SELECT TicketIDNumber FROM purchase WHERE EmailAddress = %s'
        cursor.execute(query,email)
        data = cursor.fetchall()
        if len(data) == 1:
            ticketid = data[0].get("TicketIDNumber")
            query2 = 'SELECT FlightNumber FROM ticket WHERE TicketIDNumber = %s & DepartureDateandTime < %s'
            cursor.execute(query2,ticketid,dt_string)
            data1 = cursor.fetchone()
            if data1:
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
            query2 = 'SELECT FlightNumber, TicketIDNumber FROM ticket WHERE DepartureDateandTime < %s AND TicketIDNumber IN {}'.format(str(tupleticketids))
            cursor.execute(query2, dt_string)
            data1 = cursor.fetchall()
            if len(data1) == 1:
                ticketid = data1[0].get("TicketIDNumber")
                flightnumber = data1[0].get("FlightNumber")
                query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM flight WHERE FlightNumber = %s'
                cursor.execute(query3, flightnumber)
                results = cursor.fetchall()
                results[0].update({"TicketIDNumber": ticketid})
            elif len(data1) > 1:
                flightnumbers = []
                ticketids= []
                for items in data1:
                    ticketids.append(items['TicketIDNumber'])
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
        message = "Flight successfully rated"
        headings = ("Airline Name", "Flight Number", "Departure Date and Time", "Arrival Date and Time", "Status", "TicketIDNumber")
        return render_template('customer_templates/customer_previous_flights.html', email=email, headings=headings, data=results, context = message)
    else:
        query = 'SELECT TicketIDNumber FROM purchase WHERE EmailAddress = %s'
        cursor.execute(query,email)
        data = cursor.fetchall()
        if len(data) == 1:
            ticketid = data[0].get("TicketIDNumber")
            query2 = 'SELECT FlightNumber FROM ticket WHERE TicketIDNumber = %s AND DepartureDateandTime < %s'
            cursor.execute(query2,(ticketid, dt_string))
            data1 = cursor.fetchone()
            if data1:
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
            query2 = 'SELECT FlightNumber, TicketIDNumber FROM ticket WHERE DepartureDateandTime < %s AND TicketIDNumber IN {}'.format(str(tupleticketids))
            cursor.execute(query2, dt_string)
            data1 = cursor.fetchall()
            if len(data1) == 1:
                ticketid = data1[0].get("TicketIDNumber")
                flightnumber = data1[0].get("FlightNumber")
                query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM flight WHERE FlightNumber = %s'
                cursor.execute(query3, flightnumber)
                results = cursor.fetchall()
                results[0].update({"TicketIDNumber": ticketid})
            elif len(data1) > 1:
                flightnumbers = []
                ticketids= []
                for items in data1:
                    ticketids.append(items['TicketIDNumber'])
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
        error = "Flight cannot be rated"
        return render_template('customer_templates/customer_previous_flights.html', email=email, headings=headings, data=results, error = error)


@app.route('/view_my_future_flights')
def view_my_future_flights():
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
        ticketid = data[0].get("TicketIDNumber")
        query2 = 'SELECT FlightNumber FROM ticket WHERE TicketIDNumber = %s AND DepartureDateandTime >= %s'
        cursor.execute(query2,(ticketid, dt_string))
        data1 = cursor.fetchone()
        if data1:
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
        query2 = 'SELECT FlightNumber, TicketIDNumber FROM ticket WHERE DepartureDateandTime >= %s AND TicketIDNumber IN {}'.format(str(tupleticketids))
        cursor.execute(query2, dt_string)
        data1 = cursor.fetchall()
        if len(data1) == 1:
            ticketid = data1[0].get("TicketIDNumber")
            flightnumber = data1[0].get("FlightNumber")
            query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM flight WHERE FlightNumber = %s'
            cursor.execute(query3, flightnumber)
            results = cursor.fetchall()
            results[0].update({"TicketIDNumber": ticketid})
        elif len(data1) > 1:
            flightnumbers = []
            ticketids= []
            for items in data1:
                ticketids.append(items['TicketIDNumber'])
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
    return render_template('customer_templates/customer_future_flights.html', email=email, headings=headings, data=results)

@app.route('/view_my_previous_flights')
def view_my_previous_flights():
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
        ticketid = data[0].get("TicketIDNumber")
        query2 = 'SELECT FlightNumber FROM ticket WHERE TicketIDNumber = %s AND DepartureDateandTime < %s'
        cursor.execute(query2,(ticketid, dt_string))
        data1 = cursor.fetchone()
        if data1:
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
        query2 = 'SELECT FlightNumber, TicketIDNumber FROM ticket WHERE DepartureDateandTime < %s AND TicketIDNumber IN {}'.format(str(tupleticketids))
        cursor.execute(query2, dt_string)
        data1 = cursor.fetchall()
        if len(data1) == 1:
            ticketid = data1[0].get("TicketIDNumber")
            flightnumber = data1[0].get("FlightNumber")
            query3 = 'SELECT AirlineName, FlightNumber, DepartureDateandTime, ArrivalDateandTime, Status FROM flight WHERE FlightNumber = %s'
            cursor.execute(query3, flightnumber)
            results = cursor.fetchall()
            results[0].update({"TicketIDNumber": ticketid})
        elif len(data1) > 1:
            flightnumbers = []
            ticketids= []
            for items in data1:
                ticketids.append(items['TicketIDNumber'])
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
    return render_template('customer_templates/customer_previous_flights.html', email=email, headings=headings, data=results)


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
