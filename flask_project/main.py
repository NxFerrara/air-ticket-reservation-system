# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

# Initialize the app from Flask
app = Flask(__name__)

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=8889,
                       user='root',
                       password='root',
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
    return render_template('home_templates/index.html')


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
    cursor.execute(query, (email, password))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if data:
        # creates a session for the user
        # session is a built in
        session['email'] = email
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
    cursor.execute(query, (username, password))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if data:
        # creates a session for the user
        # session is a built in
        session['username'] = username
        return redirect(url_for('airline_staff_home'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('airline_staff_templates/airline_staff_login.html', error=error)


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


# Define route for user to search for flights
@app.route('/search_flights')
def search_flights():
    return render_template('home_templates/search_flights.html')


# Define route for querying for flights and results
@app.route('/search_flights_query', methods=['GET', 'POST'])
def search_flights_query():
    # grabs information from the forms
    source_city = request.form['Source City/Airport Name']
    destination_city = request.form['Destination City/Airport Name']
    departure_date = request.form['Departure Date']
    arrival_date = request.form['Arrival Date']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM flight'
    cursor.execute(query)
    # stores the results in a variable
    data = cursor.fetchall()
    error = None
    if data:
        return render_template('home_templates/search_flights.html')
    else:
        error = "No flights found for that search result"
        return render_template('home_templates/search_flights.html', error=error)


@app.route('/customer_home')
def customer_home():
    email = session['email']
    cursor = conn.cursor()

    # need to edit this query for customer home page once logged in
    query = 'SELECT * FROM purchase WHERE EmailAddress = %s ORDER BY PurchaseDateandTime DESC'
    cursor.execute(query, email)
    data1 = cursor.fetchall()
    for each in data1:
        print(each['TicketIDNumber'])
    cursor.close()
    return render_template('customer_templates/customer_home.html', email=email, posts=data1)


@app.route('/airline_staff_home')
def airline_staff_home():
    username = session['username']
    cursor = conn.cursor()

    # need to edit this query for airline staff home page once logged in
    query = 'SELECT * FROM ticket WHERE AirlineName = %s'
    cursor.execute(query, username)
    data1 = cursor.fetchall()
    for each in data1:
        print(each['TicketIDNumber'])
    cursor.close()
    return render_template('airline_staff_templates/airline_staff_home.html', username=username, posts=data1)


@app.route('/customer_logout')
def customer_logout():
    session.pop('email')
    return redirect('/')


@app.route('/airline_staff_logout')
def airline_staff_logout():
    session.pop('username')
    return redirect('/')


app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)


# @app.route('/post', methods=['GET', 'POST'])
# def post():
#     username = session['username']
#     cursor = conn.cursor()
#     blog = request.form['blog']
#     query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
#     cursor.execute(query, (blog, username))
#     conn.commit()
#     cursor.close()
#     return redirect(url_for('home'))
