# Air Ticket Reservation System

This is a basic implementation of an Air Ticket Reservation System developed using Flask, a web application framework for Python, and MySQL for the database backend.

## Prerequisites

- Python 3.x installed
- MySQL Server
- Apache Server (with phpMyAdmin recommended)

## Setup Instructions

Follow these steps to set up and run the project:

### 1. Database Setup

1. **Start your MySQL database server.** Ensure the MySQL service is running on your system.

2. **Start your Apache server.** This is needed for phpMyAdmin to manage your MySQL database via a web interface.

3. **Access phpMyAdmin:** Open your web browser and navigate to `127.0.0.1/phpMyAdmin`. You might need to use a different address if your Apache server is configured differently.

4. **Create a new database:** In phpMyAdmin, create a new database named `blog`.

5. **Import database schema for testing:** Download the `flask_for_class.zip` file (this is specific to the intro to database course) and unzip it. Import the `simple.sql` file (this is specific to the intro to database course) into the `blog` database through phpMyAdmin. This will create two tables: `user` and `blog_post`.

### 2. Application Setup

1. **Install required Python modules:** Open your terminal and ensure you are in the project directory. Install Flask and PyMySQL by running:

   ```bash
   pip install flask pymysql
   ```

2. **Initialize the application:** Run the `init1.py` file provided from course materials using the following command:

   ```bash
   python init1.py
   ```

   If you set a root password for your MySQL database, modify the `init1.py` file (this is specific to the intro to database course) accordingly:

   ```python
   conn = pymysql.connect(host='localhost',
                          port=3306,  # Change if your MySQL port is different
                          user='root',
                          password='your_root_password',  # Change to your MySQL root password
                          db='blog',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)
   ```

### 3. Running the Application

1. **Access the application:** Open a new tab in your browser and navigate to `127.0.0.1:5000`. You should see the web page with login and registration options.

2. **Explore the system:** Register a new user, log in, and explore the functionalities of the Air Ticket Reservation System. Observe the changes in the database tables as you interact with the system.
