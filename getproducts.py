import mysql.connector

# Connect to your MySQL database
db_connection = mysql.connector.connect(
    host='localhost',
    user='prashant',
    password='Prsnt@151993',
    database='test_db'
)

# Create a cursor object
cursor = db_connection.cursor()

cursor.execute("SELECT * from elt_clean_extraction where product_id = 1")

result = cursor.fetchall()


def readData():
    return "dsdsdsd"
